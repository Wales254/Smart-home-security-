# // Don't forget to hit SUBSCRIBE, LIKE, COMMENT, and LEARN! It's good to learn :)

# Imports
import smtplib
import cv2
import time
import datetime
import imutils
from time import sleep
import sys

# Email Variables
SMTP_SERVER = 'smtp.gmail.com'  # Email Server (don't change!)
SMTP_PORT = 587  # Server Port (don't change!)
GMAIL_USERNAME = 'wesongasydney2@gmail.com'  # Change to your Gmail account
GMAIL_PASSWORD = 'WalsH254@#254'  # Change to your Gmail App Password
sendTo = 'sydneynyongesa2@gmail.com'

class Emailer:
    def sendmail(self, recipient, subject, content):
        # Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)

        # Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        # Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

        # Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit()

sender = Emailer()

def motion_detection():
    # Simulating GPIO inputs (Fake Sensor Values for Windows Testing)
    def fake_sensor_value():
        return 1  # 1 = No issue, 0 = Detected (fire, gas, etc.)

    video_capture = cv2.VideoCapture(0)  # Open default camera
    time.sleep(2)

    first_frame = None  # Instantiate the first frame

    while True:
        frame = video_capture.read()[1]  # Read video frame
        text = 'No Intruder'

        greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21, 21), 0)
        blur_frame = cv2.blur(gaussian_frame, (5, 5))
        greyscale_image = blur_frame

        if first_frame is None:
            first_frame = greyscale_image
        else:
            pass

        frame = imutils.resize(frame, width=500)
        frame_delta = cv2.absdiff(first_frame, greyscale_image)
        thresh = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]
        dilate_image = cv2.dilate(thresh, None, iterations=2)

        cnt = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        for c in cnt:
            if cv2.contourArea(c) > 800:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = 'Intruder'

                # Send email notification
                emailSubject = "Intruder Detected!"
                emailContent = "An intruder was detected at: " + time.ctime()
                sender.sendmail(sendTo, emailSubject, emailContent)
                print("Email Sent")
                break
                sleep(2)
            else:
                pass

        # Simulated Sensor Readings (Fake Values)
        fire_sensor = fake_sensor_value()  # 1 = No fire, 0 = Fire detected
        gas_sensor = fake_sensor_value()  # 1 = No gas, 0 = Gas detected
        temperature = 25  # Fake Temperature
        humidity = 50  # Fake Humidity

        if fire_sensor:
            text += ' No Fire Detected'
        else:
            text += ' Fire Detected!'

        if gas_sensor:
            text += ' No Gas Detected'
        else:
            text += ' Gas Leak Detected!'

        print(f'Temp={temperature}°C  Humidity={humidity}%')

        cv2.putText(frame, '{+} Room Status: %s' % (text),
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)

        cv2.imshow('Security Feed', frame)
        cv2.imshow('Threshold(foreground mask)', dilate_image)
        cv2.imshow('Frame_delta', frame_delta)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    motion_detection()
