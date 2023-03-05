import threading
import tkinter as tk
import time

from PIL import ImageTk

from computer_vision.ip_cam_reader import IPCamReader


class ScanFaceWindow(tk.Toplevel):
    from user_interface.root_window import RootWindow

    def __init__(self, root: RootWindow, ipc_reader: IPCamReader):
        super().__init__(root)

        self.ipc_reader = ipc_reader

        self.title("Scan Face")
        self.geometry("500x600")
        self.resizable(False, False)

        # create a frame for the image and label
        __image_frame = tk.Frame(self, width=500, height=500)
        __image_frame.pack(padx=10, pady=10, expand=True)
        __image_frame.pack_propagate(False)  # prevent the frame from resizing
        self.__image_label = tk.Label(__image_frame, bg="white")
        self.__image_label.pack(expand=True, fill="both")

        # create a frame for the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Add a space between the buttons
        tk.Label(button_frame, text=" ").grid(row=0, column=0)

        # Change the color of the buttons
        tk.Button(button_frame, text="Cancel", command=self.destroy, bg="red", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Scan", bg="green", fg="white").grid(row=0, column=2, padx=5)

        img_display_thread = threading.Thread(target=lambda: self.display_cam_image())
        img_display_thread.daemon = True
        img_display_thread.start()

    def display_cam_image(self):
        while True:
            frame = self.ipc_reader.get_frame()

            photo = ImageTk.PhotoImage(frame)
            self.__image_label.configure(image=photo)
            self.__image_label.image = photo

            time.sleep(0.03)
