import threading
import tkinter as tk
import time

import PIL.Image
from PIL import ImageTk

from computer_vision import IPCamReader
from computer_vision import ImageProcessor

from database_driver import ImageData
from database_driver import ImageDatabase


class ScanFaceWindow(tk.Toplevel):
    from user_interface.root_window import RootWindow

    def __init__(self, root: RootWindow, ipc_reader: IPCamReader):
        super().__init__(root)
        self.protocol("WM_DELETE_WINDOW", self.__on_close)

        self.ipc_reader = ipc_reader
        self.database_driver = ImageDatabase()
        self.image_processor = ImageProcessor()

        self.configure(bg="#E2D1F9")
        self.title("Scan Face")
        self.geometry("500x650")
        self.resizable(False, False)

        __image_frame = tk.Frame(self, width=500, height=500)
        __image_frame.pack(padx=10, pady=10, expand=True)
        __image_frame.pack_propagate(False)
        self.__image_label = tk.Label(__image_frame, bg="white")
        self.__image_label.pack(expand=True, fill="both")

        name_frame = tk.Frame(self, width=500, height=50, bg="#E2D1F9")
        name_frame.pack(padx=10, pady=10, expand=True)
        name_frame.pack_propagate(False)
        tk.Label(name_frame, text="Name:").pack()
        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack(padx=5)

        button_frame = tk.Frame(self, bg="#E2D1F9")
        button_frame.pack(padx=10, pady=10)

        tk.Label(button_frame, text=" ", bg="#E2D1F9").grid(row=0, column=0)

        tk.Button(button_frame, text="Cancel", command=lambda: self.destroy(), bg="red", fg="white").grid(row=0,
                                                                                                          column=1,
                                                                                                          padx=5)
        tk.Button(button_frame, text="Scan", command=lambda: self.__on_scan(), bg="green", fg="white").grid(row=0,
                                                                                                            column=2,
                                                                                                            padx=5)

        img_display_thread = threading.Thread(target=lambda: self.display_cam_image())
        img_display_thread.daemon = True
        img_display_thread.start()

    def display_cam_image(self):
        self.ipc_reader.isFaceMash = True
        while self.ipc_reader.isFaceMash:
            try:
                mat = self.ipc_reader.get_frame()
                frame = PIL.Image.fromarray(mat)

                photo = ImageTk.PhotoImage(frame)
                self.__image_label.configure(image=photo)
                self.__image_label.image = photo

            except:
                pass

            time.sleep(0.03)

    def __on_close(self):
        self.ipc_reader.isFaceMash = False
        self.destroy()

    def __on_scan(self):
        def process():
            self.ipc_reader.isFaceMash = False

            while True:
                mat = self.ipc_reader.get_frame()
                frame = PIL.Image.fromarray(mat)
                photo = ImageTk.PhotoImage(frame)
                self.__image_label.configure(image=photo)
                self.__image_label.image = photo

                face_name = self.name_entry.get()

                meta_data = self.image_processor.scan_face(mat)
                if meta_data is None:
                    print("meta_data is none")
                    continue

                face_img, face_encoding = meta_data
                face_data = ImageData(face_name, face_img, face_encoding)

                ImageProcessor.known_faces.append(face_data)
                self.database_driver.save_known_image(face_data)

                self.destroy()

        scanning_thread = threading.Thread(target=process)
        scanning_thread.daemon = True
        scanning_thread.start()
