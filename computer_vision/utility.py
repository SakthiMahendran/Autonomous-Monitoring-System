import threading
from email.mime.text import MIMEText

import cv2
import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class Utility:
    user_name = "autonomousmonitoringsystem"
    password = "xgzxwbenvazgtaau"

    from_addr = "autonomousmonitoringsystem@gmail.com"
    to_addr = "kingsakthi2005@gmail.com"

    @staticmethod
    def send_mail(face: cv2.Mat, face_name: str, cam_name: str):
        def process():
            time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            subject = f"Face Detected"
            message = MIMEMultipart()
            message['From'] = Utility.from_addr
            message['To'] = Utility.to_addr
            message['Subject'] = subject

            # Convert the OpenCV image to bytes
            _, img_encoded = cv2.imencode('.jpg', face)
            img_bytes = img_encoded.tobytes()

            # Attach the image to the email message
            image = MIMEImage(img_bytes)
            image.add_header('Content-Disposition', 'attachment', filename=f"{face_name}_{time_now}.jpg")
            message.attach(image)

            # Add a body to the email message
            body = f"Hi,\n\nA face has been detected on {cam_name} camera at {time_now} and identified as {face_name}.\n\nPlease check the attached image for details.\n\nThanks"
            text = MIMEText(body)
            message.attach(text)

            # Send the email
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = Utility.user_name
            smtp_password = Utility.password
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(message['From'], message['To'], message.as_string())

            print("Mail Sent")

        mail_thread = threading.Thread(target=process)
        mail_thread.daemon = True
        mail_thread.start()
