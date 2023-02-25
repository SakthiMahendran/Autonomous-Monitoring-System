import tkinter as tk
from PIL import Image, ImageTk
from user_interface.add_cam_window import AddCamWindow


class RootWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("900x650")
        self.resizable(False, False)
        self.title("Autonomous Monitoring System")

        self.__render_image_label()
        self.__render_scan_facebtn()
        self.__render_add_cambtn()
        self.__render_changecambtn()

    def __render_image_label(self):
        image = Image.open("assets/no_cam.jpg")
        photo = ImageTk.PhotoImage(image)
        self.__imgLabel = tk.Label(self, image=photo)
        self.__imgLabel.image = photo
        self.__imgLabel.place(relx=0.5, rely=0.2, anchor='center')

    def __render_scan_facebtn(self):
        self.__scanFaceBtn = tk.Button(self, text='Scan Face')
        self.__scanFaceBtn.place(relx=0.35, rely=0.85)

    def __render_add_cambtn(self):
        self.__addCamBtn = tk.Button(self, text='Add New Camera', command=lambda: AddCamWindow(self))
        self.__addCamBtn.place(relx=0.44, rely=0.85)

    def __render_changecambtn(self):
        self.__camList = tk.Button(self, text='Change Camera')
        self.__camList.place(relx=0.58, rely=0.85)

    def show_and_run(self):
        self.mainloop()
