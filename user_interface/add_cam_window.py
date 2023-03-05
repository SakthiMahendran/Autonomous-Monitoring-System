import tkinter as tk
from user_interface.root_window import RootWindow


class AddCamWindow(tk.Toplevel):
    def __init__(self, root: RootWindow):
        super().__init__(root)
        self.root_window = root

        self.title("Add Camera")
        self.geometry("300x350")
        self.resizable(False, False)

        self.__create_camera_name_field()
        self.__create_username_field()
        self.__create_password_field()
        self.__create_protocol_field()
        self.__create_url_field()
        self.__create_port_field()
        self.__create_stream_field()
        self.__create_add_camera_button()

        self.mainloop()

    def __create_camera_name_field(self):
        camera_name_label = tk.Label(self, text="Camera Name:")
        camera_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.camera_name_entry = tk.Entry(self)
        self.camera_name_entry.grid(row=0, column=1, padx=5, pady=5)

    def __create_username_field(self):
        username_label = tk.Label(self, text="Username:")
        username_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

    def __create_password_field(self):
        password_label = tk.Label(self, text="Password:")
        password_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

    def __create_protocol_field(self):
        protocol_label = tk.Label(self, text="Protocol:")
        protocol_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.protocol_entry = tk.Entry(self)
        self.protocol_entry.grid(row=3, column=1, padx=5, pady=5)

    def __create_url_field(self):
        ip_label = tk.Label(self, text="IP Address:")
        ip_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.ip_entry = tk.Entry(self)
        self.ip_entry.grid(row=4, column=1, padx=5, pady=5)

    def __create_port_field(self):
        port_label = tk.Label(self, text="Port:")
        port_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.port_entry = tk.Entry(self)
        self.port_entry.grid(row=5, column=1, padx=5, pady=5)

    def __create_stream_field(self):
        stream_label = tk.Label(self, text="Stream:")
        stream_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.stream_entry = tk.Entry(self)
        self.stream_entry.grid(row=6, column=1, padx=5, pady=5)

    def __create_add_camera_button(self):
        add_camera_button = tk.Button(self, text="Add Camera", command=self.__add_camera_action)
        add_camera_button.grid(row=7, column=1, padx=5, pady=5, sticky="n")

    def __add_camera_action(self):
        cam_name = self.camera_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        protocol = self.protocol_entry.get()
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        stream = self.stream_entry.get()

        self.root_window.add_cam(cam_name, username, password, protocol, ip, port, stream)
