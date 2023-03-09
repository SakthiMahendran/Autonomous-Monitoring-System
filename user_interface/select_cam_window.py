import threading
import tkinter as tk
from user_interface.root_window import RootWindow


class SelectCamWindow(tk.Toplevel):
    def __init__(self, root: RootWindow):
        super().__init__()

        self.root_window = root
        self.selected_cam = None
        self.cameras = []

        self.configure(bg="#E2D1F9")
        self.title("Select Camera")
        self.geometry("300x300")
        self.resizable(False, False)

        self.__create_camera_list()
        self.__create_select_camera_button()

        self.__add_elements_to_camera_list()

    def __create_camera_list(self):
        camera_list_label = tk.Label(self, text="Cameras:")
        camera_list_label.pack(padx=5, pady=5)

        self.camera_listbox = tk.Listbox(self, height=10)
        self.camera_listbox.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

    def __create_select_camera_button(self):
        self.select_camera_button = tk.Button(self,
                                              text="Select",
                                              command=self.__on_select_btn_clicked,
                                              fg="white",
                                              bg="#317773",
                                              disabledforeground="black",
                                              )

        self.select_camera_button.pack(padx=5, pady=5)
        self.select_camera_button.configure(state=tk.DISABLED)

    def __add_elements_to_camera_list(self):
        self.cameras = list(self.root_window.cam_data.keys())

        if len(self.cameras) == 0:
            self.camera_listbox.insert(tk.END, "Add a camera before selecting")
            self.camera_listbox.configure(state=tk.DISABLED)
            self.select_camera_button.configure(state=tk.DISABLED)
            return

        for cam in self.cameras:
            self.camera_listbox.insert(tk.END, cam)

        self.camera_listbox.bind("<<ListboxSelect>>", lambda event: self.__on_select())

    def __on_select(self):
        self.select_camera_button.configure(state=tk.NORMAL)

    def __on_select_btn_clicked(self):
        selection_index = self.camera_listbox.curselection()[0]

        if selection_index != self.root_window.selected_cam_index:
            self.root_window.selected_cam_index = selection_index
            self.root_window.change_cam()

            self.image_thread = threading.Thread(target=self.root_window.display_cam_image)
            self.image_thread.daemon = True
            self.image_thread.start()

        self.destroy()
