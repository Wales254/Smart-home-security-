import cv2
import time
import datetime
import imutils
from email_alerts import send_email
from sensor_data import get_sensor_data

def motion_detection():
    video_capture = cv2.VideoCapture(0)  # Open default camera
    time.sleep(2)
    first_frame = None  # Initialize the first frame

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("❌ Camera not detected!")
            break
        
        greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21, 21), 0)
        
        if first_frame is None:
            first_frame = gaussian_frame
            continue

        frame_delta = cv2.absdiff(first_frame, gaussian_frame)
        thresh = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]
        dilate_image = cv2.dilate(thresh, None, iterations=2)

        cnts, _ = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            if cv2.contourArea(c) > 800:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                print("🚨 Intruder Detected! Sending Alert...")
                send_email("Intruder Detected!", "Motion detected at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                time.sleep(2)  # Prevents email spamming
                
        temperature, humidity, gas_detected, fire_detected = get_sensor_data()
        status_text = f"Temp: {temperature}C | Humidity: {humidity}% | Gas: {'Yes' if gas_detected else 'No'} | Fire: {'Yes' if fire_detected else 'No'}"

        cv2.putText(frame, status_text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow("Security Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    motion_detection()
