import PIL.Image
import cv2

from computer_vision import ImageProcessor


class IPCamReader:

    def __init__(self, video_stream: cv2.VideoCapture, cam_name: str, cam_url: str):
        self.video_stream = video_stream
        self.cam_name = cam_name
        self.cam_url = cam_url
        self.current_frame = cv2.Mat
        self.isFaceMash = False

    def __del__(self):
        self.video_stream.release()

    def start_processing(self):
        img_processor = ImageProcessor()
        processed_frames = []

        def process(frame: cv2.Mat):
            frame = cv2.resize(frame, (500, 500))

            if self.isFaceMash:
                frame = img_processor.draw_facemesh(frame)
            else:
                frame = img_processor.draw_facebox(frame, self.cam_name)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.__set_frame(frame)

        while self.video_stream.isOpened():
            res, frame = self.video_stream.read()
            if not res:
                continue

            process(frame)

    def __set_frame(self, mat: cv2.Mat):
        self.current_frame = mat

    def get_frame(self) -> PIL.Image.Image:
        return self.current_frame.copy()

    @staticmethod
    def connect_with_cam(cam_name: str, cam_url: str):
        video_stream = cv2.VideoCapture(cam_url)

        if video_stream.isOpened():
            return IPCamReader(video_stream, cam_name, cam_url)

        return None
