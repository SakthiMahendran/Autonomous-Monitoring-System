import threading
import tkinter as tk
import time

import PIL.Image
from PIL import ImageTk

from computer_vision.ip_cam_reader import IPCamReader
from computer_vision.image_processor import ImageProcessor

from database_driver.image_data import ImageData
from database_driver.image_database import ImageDatabase


class ScanFaceWindow(tk.Toplevel):
    from user_interface.root_window import RootWindow

    def __init__(self, root: RootWindow, ipc_reader: IPCamReader):
        super().__init__(root)

        self.ipc_reader = ipc_reader
        self.database_driver = ImageDatabase()
        self.image_processor = ImageProcessor()

        self.title("Scan Face")
        self.geometry("500x650")
        self.resizable(False, False)

        # create a frame for the image and label
        __image_frame = tk.Frame(self, width=500, height=500)
        __image_frame.pack(padx=10, pady=10, expand=True)
        __image_frame.pack_propagate(False)  # prevent the frame from resizing
        self.__image_label = tk.Label(__image_frame, bg="white")
        self.__image_label.pack(expand=True, fill="both")

        # create a frame for the name entry
        name_frame = tk.Frame(self, width=500, height=50)
        name_frame.pack(padx=10, pady=10, expand=True)
        name_frame.pack_propagate(False)  # prevent the frame from resizing
        tk.Label(name_frame, text="Name:").pack(side="left")
        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack(side="left", padx=5)

        # create a frame for the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Add a space between the buttons
        tk.Label(button_frame, text=" ").grid(row=0, column=0)

        # Change the color of the buttons
        tk.Button(button_frame, text="Cancel", command=self.destroy, bg="red", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Scan", command=self.__on_scan,bg="green", fg="white").grid(row=0, column=2, padx=5)

        img_display_thread = threading.Thread(target=lambda: self.display_cam_image())
        img_display_thread.daemon = True
        img_display_thread.start()

    def display_cam_image(self):
        self.ipc_reader.isFaceMash = True
        while self.ipc_reader.isFaceMash:
            mat = self.ipc_reader.get_frame()
            frame = PIL.Image.fromarray(mat)

            photo = ImageTk.PhotoImage(frame)
            self.__image_label.configure(image=photo)
            self.__image_label.image = photo

            time.sleep(0.03)

    def __on_scan(self):
        self.ipc_reader.isFaceMash = False

        while True:
            mat = self.ipc_reader.get_frame()
            frame = PIL.Image.fromarray(mat)
            photo = ImageTk.PhotoImage(frame)
            self.__image_label.configure(image=photo)
            self.__image_label.image = photo

            face_name = self.name_entry.get()
            face_img = self.image_processor.get_face(self.ipc_reader.get_frame())
            if face_img is None:
                print("face_img is none")
                continue

            face_encoding = self.image_processor.get_encoding(face_img)
            if face_encoding is None:
                print("face_encoding is none")
                continue

            face_data = ImageData(face_name, face_img, face_encoding)

            ImageProcessor.known_faces.append(face_data)
            self.database_driver.save_known_image(face_data)

            self.destroy()
