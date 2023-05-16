from typing import List

import cv2
import mediapipe as mp
import face_recognition

from database_driver import ImageDatabase
from database_driver import ImageData
from database_driver import TextDatabase

from computer_vision.utility import Utility


class ImageProcessor:
    known_faces = list()

    def __init__(self):
        self.detected_faces = set()

        self.util = Utility()

        self.mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.6)
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True,
                                                            refine_landmarks=True,
                                                            min_detection_confidence=0.6,
                                                            min_tracking_confidence=0.6)

        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(self.mp_drawing.GREEN_COLOR, 3, 1)

        self.img_database_driver = ImageDatabase()
        self.csv_database_driver = TextDatabase()

        self.__green_color = (0, 255, 0)
        self.__red_color = (0, 0, 255)
        self.__orange_color = (0, 147, 238)

        ImageProcessor.known_faces = self.img_database_driver.load_known_images()

    def __del__(self):
        self.mp_face_detection.close()
        self.mp_face_mesh.close()

    def draw_facebox(self, frame: cv2.Mat, cam_name: str) -> cv2.Mat:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.mp_face_detection.process(rgb_frame)

        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        faces = ImageProcessor.__detect_faces(results, bgr_frame)

        recognized_faces = self.__recognize_faces(faces)

        name = ""

        for i, face in enumerate(recognized_faces):
            if face is not None:
                (top, right, bottom, left) = face['location']
                name = face['name'] if face['name'] is not None else 'Unknown'

                if name == "Unknown":
                    cv2.rectangle(bgr_frame, (left, top), (right, bottom), self.__red_color, 2)
                    cv2.putText(bgr_frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.__red_color, 2)
                elif name == "Detected":
                    cv2.rectangle(bgr_frame, (left, top), (right, bottom), self.__orange_color, 2)
                    cv2.putText(bgr_frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.__orange_color, 2)
                else:
                    cv2.rectangle(bgr_frame, (left, top), (right, bottom), self.__green_color, 2)
                    cv2.putText(bgr_frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.__green_color, 2)

        if name not in self.detected_faces and name != "":
            self.util.send_mail(bgr_frame, name, cam_name)
            self.util.say(name, cam_name)

            self.csv_database_driver.update_data(name, cam_name)

            self.detected_faces.add(name)

        return bgr_frame


    def draw_facemesh(self, frame: cv2.Mat):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.mp_face_mesh.process(frame)
        if results.multi_face_landmarks:
            height, width = frame.shape[0], frame.shape[1]
            for face_landmarks in results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    x = int(landmark.x * height)
                    y = int(landmark.y * width)
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        return frame
    def scan_face(self, frame: cv2.Mat):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.mp_face_detection.process(rgb_frame)

        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        faces = ImageProcessor.__detect_faces(results, bgr_frame)
        if len(faces) == 0:
            return None

        face = faces[0]
        if face is None:
            return None

        face_encoding = face_recognition.face_encodings(face['image'], [face['location']], model='small')
        if len(face_encoding) == 0:
            return None

        return [face['image'], face_encoding[0]]

    @staticmethod
    def __detect_faces(results, frame):
        extra_height = 20
        extra_weight = 10
        faces = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                height, width, _ = frame.shape

                y_min = int(bbox.ymin * height) - extra_height
                y_max = int((bbox.ymin + bbox.height) * height) + extra_height
                x_min = int(bbox.xmin * width) - extra_weight
                x_max = int((bbox.xmin + bbox.width) * width) + extra_weight

                face = {'location': (y_min, x_max, y_max, x_min), 'image': frame}
                faces.append(face)
        return faces

    @staticmethod
    def __get_all_encodings(image_data: List[ImageData]):
        img_encodings = []
        for i in image_data:
            img_encodings.append(i.image_encoding)

        return img_encodings

    @staticmethod
    def __recognize_faces(faces: list) -> list:
        recognized_faces = []
        for face in faces:
            if face is not None:
                location = face['location']
                encoding = face_recognition.face_encodings(face['image'], [location], model='large')

                if len(encoding) == 0:
                    recognized_faces.append({'location': location, 'name': "Detected"})
                    continue

                matches = face_recognition.compare_faces(ImageProcessor.__get_all_encodings(ImageProcessor.known_faces),
                                                         encoding[0],
                                                         tolerance=0.50)
                name = None
                if True in matches:
                    face_index = matches.index(True)
                    name = ImageProcessor.known_faces[face_index].image_name
                recognized_faces.append({'location': location, 'name': name})
            else:
                recognized_faces.append(None)
        return recognized_faces
