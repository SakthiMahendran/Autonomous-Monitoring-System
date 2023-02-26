import cv2
import mediapipe as mp


class ImageProcessor:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5)

    def detect_faces(self, frame: cv2.Mat) -> cv2.Mat:
        # Convert the input frame from BGR (OpenCV's default) to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect all the faces in the frame using the MediaPipe Face Detection model
        results = self.mp_face_detection.process(rgb_frame)

        # Draw a rectangle around each face in the frame
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                height, width, _ = frame.shape
                xmin = int(bbox.xmin * width)
                ymin = int(bbox.ymin * height)
                xmax = int((bbox.xmin + bbox.width) * width)
                ymax = int((bbox.ymin + bbox.height) * height)
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        return frame
