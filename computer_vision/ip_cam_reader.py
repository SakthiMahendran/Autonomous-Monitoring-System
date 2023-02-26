import PIL.Image
import cv2


class IPCamReader:

    def __init__(self, video_stream: cv2.VideoCapture, cam_name: str, cam_url: str):
        self.video_stream = video_stream
        self.cam_name = cam_name
        self.cam_url = cam_url
        self.current_frame = PIL.Image.Image

    def start_processing(self):
        while True:
            res, frame = self.video_stream.read()
            frame = cv2.resize(frame, (500, 500))

            if res:
                self.set_frame(frame)

    def set_frame(self, mat: cv2.Mat):
        rgb_image = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(rgb_image)
        self.current_frame = image.copy()

    def get_frame(self) -> PIL.Image.Image:
        return self.current_frame.copy()

    @staticmethod
    def connect_with_cam(cam_name: str, cam_url: str):
        video_stream = cv2.VideoCapture(cam_url)

        if video_stream.isOpened():
            return IPCamReader(video_stream, cam_name, cam_url)

        return None