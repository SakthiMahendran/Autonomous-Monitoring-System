import cv2

from dataclasses import dataclass
from PIL.Image import Image


@dataclass
class ImageData:
    image_name: str
    image: cv2.Mat
