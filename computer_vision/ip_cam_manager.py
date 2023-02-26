from threading import Thread

from computer_vision.ip_cam_reader import IPCamReader


class IPCamManager:
    def __init__(self):
        self.__ip_cams = []

    def set_cam(self, cam_name: str, cam_url: str) -> bool:
        ip_cam_reader = IPCamReader.connect_with_cam(cam_name, cam_url)

        if ip_cam_reader is None:
            return False

        process_thread = Thread(target=ip_cam_reader.start_processing)
        process_thread.daemon = True
        process_thread.start()
        self.__ip_cams.append(ip_cam_reader)

        return True

    def get_cam(self, index: int) -> IPCamReader:
        return self.__ip_cams[index]
