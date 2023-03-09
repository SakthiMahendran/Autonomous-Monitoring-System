import os
import csv
from datetime import datetime


class CsvDatabase:
    CSV_DATABASE_PATH = "database/csv/"

    def __init__(self):
        # Create the directory if it does not exist
        if not os.path.exists(self.CSV_DATABASE_PATH):
            os.makedirs(self.CSV_DATABASE_PATH)

        # Define the file path and field names
        file_path = os.path.join(self.CSV_DATABASE_PATH, "data.csv")
        field_names = ["Name", "CameraName", "TimeStamp"]

        # Create the file if it does not exist
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=field_names)
                writer.writeheader()

    def update_data(self, name: str, cam_name: str, timestamp=None):
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = os.path.join(self.CSV_DATABASE_PATH, "data.csv")
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, cam_name, timestamp])
