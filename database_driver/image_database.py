import os
import pickle
from typing import List

from database_driver.image_data import ImageData


class ImageDatabase:
    IMAGE_DATABASE_PATH = "database/images/"

    def __init__(self):
        self._create_directories()

    def save_known_image(self, img_data: ImageData):
        file_path = os.path.join(self.IMAGE_DATABASE_PATH, "known", f"{img_data.image_name}.jpr")
        with open(file_path, "wb") as f:
            pickle.dump(img_data, f)

    def load_known_images(self) -> List[ImageData]:
        known_path = os.path.join(self.IMAGE_DATABASE_PATH, "known")
        known_images = []
        for file_name in os.listdir(known_path):
            if file_name.endswith(".jpr"):
                file_path = os.path.join(known_path, file_name)
                with open(file_path, "rb") as f:
                    known_images.append(pickle.load(f))
        return known_images

    def save_unknown_images(self, img_data: ImageData):
        file_path = os.path.join(self.IMAGE_DATABASE_PATH, "unknown", f"{img_data.image_name}.jpr")
        with open(file_path, "wb") as f:
            pickle.dump(img_data, f)

    def load_unknown_images(self) -> List[ImageData]:
        unknown_path = os.path.join(self.IMAGE_DATABASE_PATH, "unknown")
        unknown_images = []
        for file_name in os.listdir(unknown_path):
            if file_name.endswith(".jpr"):
                file_path = os.path.join(unknown_path, file_name)
                with open(file_path, "rb") as f:
                    unknown_images.append(pickle.load(f))
        return unknown_images

    def _create_directories(self):
        if not os.path.isdir(self.IMAGE_DATABASE_PATH):
            os.makedirs(self.IMAGE_DATABASE_PATH)

        known_path = os.path.join(self.IMAGE_DATABASE_PATH, "known")
        if not os.path.isdir(known_path):
            os.makedirs(known_path)

        unknown_path = os.path.join(self.IMAGE_DATABASE_PATH, "unknown")
        if not os.path.isdir(unknown_path):
            os.makedirs(unknown_path)
