import os
import csv
import sqlite3
from datetime import datetime


class TextDatabase:
    CSV_DATABASE_PATH = "database/csv/"
    SQLITE_DATABASE_PATH = "database/sqlite/"
    CSV_FILE_NAME = "data.csv"
    SQLITE_DB_NAME = "data.db"

    def __init__(self):
        # Create the directories if they do not exist
        if not os.path.exists(self.CSV_DATABASE_PATH):
            os.makedirs(self.CSV_DATABASE_PATH)
        if not os.path.exists(self.SQLITE_DATABASE_PATH):
            os.makedirs(self.SQLITE_DATABASE_PATH)

        # Define the CSV file path and field names
        csv_file_path = os.path.join(self.CSV_DATABASE_PATH, self.CSV_FILE_NAME)
        field_names = ["Name", "CameraName", "TimeStamp"]

        # Create the CSV file if it does not exist
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=field_names)
                writer.writeheader()

        # Define the SQLite database path and table schema
        sqlite_db_path = os.path.join(self.SQLITE_DATABASE_PATH, self.SQLITE_DB_NAME)
        self.sqlite_conn = sqlite3.connect(sqlite_db_path)
        self.sqlite_conn.execute('''CREATE TABLE IF NOT EXISTS data
                                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Name           TEXT    NOT NULL,
                                CameraName     TEXT    NOT NULL,
                                TimeStamp      TEXT    NOT NULL);''')

    def update_data(self, name: str, cam_name: str, timestamp=None):
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update the CSV file
        csv_file_path = os.path.join(self.CSV_DATABASE_PATH, self.CSV_FILE_NAME)
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, cam_name, timestamp])

        # Update the SQLite database
        self.sqlite_conn.execute("INSERT INTO data (Name, CameraName, TimeStamp) \
            VALUES (?, ?, ?)", (name, cam_name, timestamp))
        self.sqlite_conn.commit()
