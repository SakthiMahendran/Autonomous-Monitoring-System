import cv2
import numpy

from dataclasses import dataclass


@dataclass
class ImageData:
    image_name: str
    image: cv2.Mat
    image_encoding: numpy.ndarray
