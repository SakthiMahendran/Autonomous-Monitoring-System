import cv2
from PIL import Image

class IPCamReader:
    def __init__(self, camURL:str) -> None:
        self.cam = cv2.VideoCapture(camURL)

    def readImage(self) -> Image.Image:
        res, mat = self.cam.read()

        if not res:
            return None

        mat = cv2.resize(mat, (500, 500))
        mat = self.__bgr2rgb(mat)

        return self.__mat2img(mat)
            
    def __bgr2rgb(self, mat:cv2.Mat) -> cv2.Mat:
        return cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
    
    def __mat2img(self, mat:cv2.Mat) -> Image.Image:
        return Image.fromarray(mat)