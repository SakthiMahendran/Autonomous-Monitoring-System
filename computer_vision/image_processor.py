from typing import List

import cv2
import mediapipe as mp
import face_recognition

from database_driver.image_database import ImageDatabase
from database_driver.image_database import ImageData


class ImageProcessor:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.60)
        self.img_database_driver = ImageDatabase()
        self.known_faces = self.img_database_driver.load_known_images()

        self.__green_color = (0, 255, 0)
        self.__red_color = (0, 0, 255)
        self.__orange_color = (0, 147, 238)

    def process_image(self, frame: cv2.Mat) -> cv2.Mat:
        # Convert the input frame from BGR (OpenCV's default) to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect all the faces in the frame using the MediaPipe Face Detection model
        results = self.mp_face_detection.process(rgb_frame)

        # Convert the RGB frame to a BGR frame for OpenCV to display it properly
        bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        # Get the faces as numpy arrays
        faces = self.__detect_faces(results, bgr_frame)

        # Recognize the faces
        recognized_faces = self.__recognize_faces(faces)

        # Draw rectangles around the recognized faces and add the name as text above the rectangle
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
        return bgr_frame

    def __recognize_faces(self, faces: list) -> list:
        recognized_faces = []
        for face in faces:
            if face is not None:
                location = face['location']
                encoding = face_recognition.face_encodings(face['image'], [location], model='large')

                if len(encoding) == 0:
                    recognized_faces.append({'location': location, 'name': "Detected"})
                    continue

                matches = face_recognition.compare_faces(self.__get_all_encodings(self.known_faces), encoding[0])
                name = None
                if True in matches:
                    face_index = matches.index(True)
                    name = self.known_faces[face_index].image_name
                recognized_faces.append({'location': location, 'name': name})
            else:
                recognized_faces.append(None)
        return recognized_faces

    def __detect_faces(self, results, frame):
        increased_size = 25
        faces = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                height, width, _ = frame.shape

                y_min = int(bbox.ymin * height) - increased_size
                y_max = int((bbox.ymin + bbox.height) * height) + increased_size
                x_min = int(bbox.xmin * width)
                x_max = int((bbox.xmin + bbox.width) * width)

                face = {'location': (y_min, x_max, y_max, x_min), 'image': frame}
                faces.append(face)
        return faces

    def __get_all_encodings(self, image_data: List[ImageData]):
        img_encodings = []
        for i in image_data:
            img_encodings.append(i.image_encoding)

        return img_encodings
