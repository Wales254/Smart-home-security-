import random

try:
    import RPi.GPIO as GPIO
    import Adafruit_DHT
    raspberry_pi = True
except ImportError:
    raspberry_pi = False  # Running on Windows

# Fake values for Windows Testing
def fake_sensor_value():
    return random.choice([0, 1])

def get_sensor_data():
    if raspberry_pi:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.IN)  # Gas sensor
        GPIO.setup(2, GPIO.IN)   # Fire sensor
        sensor = Adafruit_DHT.DHT11
        humidity, temperature = Adafruit_DHT.read_retry(sensor, 3)  # DHT11 on GPIO 3

        gas_detected = GPIO.input(21) == 0
        fire_detected = GPIO.input(2) == 0
    else:
        # Fake sensor values for Windows testing
        temperature, humidity = 25, 50
        gas_detected, fire_detected = fake_sensor_value(), fake_sensor_value()

    return temperature, humidity, gas_detected, fire_detected

# Test the sensor readings
if __name__ == "__main__":
    print(get_sensor_data())
