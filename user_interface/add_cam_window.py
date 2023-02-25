import tkinter as tk


class AddCamWindow:
    def __init__(self, root: tk.Tk):
        self.root_window = root

        self.__add_cam_window = tk.Toplevel(root)
        self.__add_cam_window.title("Add Camera")
        self.__add_cam_window.geometry("300x300")
        self.__add_cam_window.resizable(False, False)

        self.__create_camera_name_field()
        self.__create_username_field()
        self.__create_password_field()
        self.__create_protocol_field()
        self.__create_url_field()
        self.__create_port_field()
        self.__create_add_camera_button()

        self.__add_cam_window.mainloop()

    def __create_camera_name_field(self):
        camera_name_label = tk.Label(self.__add_cam_window, text="Camera Name:")
        camera_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.camera_name_entry = tk.Entry(self.__add_cam_window)
        self.camera_name_entry.grid(row=0, column=1, padx=5, pady=5)

    def __create_username_field(self):
        username_label = tk.Label(self.__add_cam_window, text="Username:")
        username_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.__add_cam_window)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

    def __create_password_field(self):
        password_label = tk.Label(self.__add_cam_window, text="Password:")
        password_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.__add_cam_window, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

    def __create_protocol_field(self):
        protocol_label = tk.Label(self.__add_cam_window, text="Protocol:")
        protocol_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.protocol_entry = tk.Entry(self.__add_cam_window)
        self.protocol_entry.grid(row=3, column=1, padx=5, pady=5)

    def __create_url_field(self):
        url_label = tk.Label(self.__add_cam_window, text="URL:")
        url_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.url_entry = tk.Entry(self.__add_cam_window)
        self.url_entry.grid(row=4, column=1, padx=5, pady=5)

    def __create_port_field(self):
        port_label = tk.Label(self.__add_cam_window, text="Port:")
        port_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.port_entry = tk.Entry(self.__add_cam_window)
        self.port_entry.grid(row=5, column=1, padx=5, pady=5)

    def __create_add_camera_button(self):
        add_camera_button = tk.Button(self.__add_cam_window, text="Add Camera", command=lambda: self.__add_camera_action())
        add_camera_button.grid(row=6, column=1, padx=5, pady=5, sticky="n")

    def __add_camera_action(self):
        print(self.camera_name_entry.get())
