import tkinter as tk
import time

import PIL.Image
from PIL import Image, ImageTk

from computer_vision import IPCamManager


class RootWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.is_change_cam = False
        self.cam_data = dict()
        self.selected_cam_index = -1
        self.cam_manager = IPCamManager()

        self.geometry("800x600")
        self.resizable(False, False)
        self.title("Autonomous Monitoring System")
        self.config(bg="#E2D1F9")

        icon_file = "assets/icon.ico"
        icon = ImageTk.PhotoImage(Image.open(icon_file))
        self.iconphoto(True, icon)

        self.__render_image_label()
        self.__render_scan_facebtn()
        self.__render_add_cambtn()
        self.__render_selectcambtn()

    def __render_image_label(self):
        image = Image.open("assets/no_cam.jpg")
        photo = ImageTk.PhotoImage(image)
        self.__imgLabel = tk.Label(self, image=photo, bg="black", width=510, height=510)
        self.__imgLabel.image = photo
        self.__imgLabel.place(relx=0.5, rely=0.4, anchor='center')

    def __render_scan_facebtn(self):
        from user_interface.scan_face_window import ScanFaceWindow
        self.__scanFaceBtn = tk.Button(self, text='Scan Face', bg="#317773", fg="white", command=lambda: ScanFaceWindow(self, self.cam_manager.get_cam(self.selected_cam_index)))
        self.__scanFaceBtn.place(relx=0.35, rely=0.85)

    def __render_add_cambtn(self):
        from user_interface.add_cam_window import AddCamWindow

        self.__addCamBtn = tk.Button(self, text='Add New Camera', bg="#317773", fg="white", command=lambda: AddCamWindow(self))
        self.__addCamBtn.place(relx=0.44, rely=0.85)

    def __render_selectcambtn(self):
        self.__camList = tk.Button(self, text='Select Camera', bg="#317773", fg="white", command=lambda: self.__show_select_window())
        self.__camList.place(relx=0.58, rely=0.85)

    def __show_select_window(self):
        from user_interface.select_cam_window import SelectCamWindow

        selected_cam = list(self.cam_data.keys())

        if not selected_cam:
            SelectCamWindow(self)
        else:
            SelectCamWindow(self)

    def add_cam(self, camname: str, username: str, password: str, protocol: str, ip: str, port: str, stream: str):
        if username == "" or password == "":
            cam_url = f"{protocol}://{ip}:{port}/{stream}"
        else:
            cam_url = f"{protocol}://{username}:{password}@{ip}:{protocol}/{stream}"

        if not self.cam_manager.set_cam(camname, cam_url):
            return

        self.cam_data[camname] = cam_url

    def change_cam(self):
        print("Camera changed to", self.selected_cam_index)

    def display_cam_image(self):

        while True:
            mat = self.cam_manager.get_cam(self.selected_cam_index).get_frame()
            frame = PIL.Image.fromarray(mat)

            photo = ImageTk.PhotoImage(frame)
            self.__imgLabel.configure(image=photo)
            self.__imgLabel.image = photo

            time.sleep(0.03)

    def show_and_run(self):
        self.mainloop()
