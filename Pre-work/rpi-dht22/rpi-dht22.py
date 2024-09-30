###This project reads two DHT22 temperature and humidity sensor

import Adafruit_DHT
import time

# Define the sensor type
DHT_SENSOR = Adafruit_DHT.DHT22

# Define the sensor pins
DHT_PIN_1 = 4  # GPIO4
DHT_PIN_2 = 17  # GPIO17

def read_sensor(sensor, pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        return humidity, temperature
    else:
        return None, None

while True:
    # Read data from Sensor 1
    humidity_1, temperature_1 = read_sensor(DHT_SENSOR, DHT_PIN_1)
    # Read data from Sensor 2
    humidity_2, temperature_2 = read_sensor(DHT_SENSOR, DHT_PIN_2)

    # Print data to the terminal
    if humidity_1 is not None and temperature_1 is not None:
        print(f'Sensor 1 - Temperature: {temperature_1:.1f}C  Humidity: {humidity_1:.1f}%')
    else:
        print('Sensor 1 - Failed to retrieve data')

    if humidity_2 is not None and temperature_2 is not None:
        print(f'Sensor 2 - Temperature: {temperature_2:.1f}C  Humidity: {humidity_2:.1f}%')
    else:
        print('Sensor 2 - Failed to retrieve data')

    # Wait for 10 seconds
    time.sleep(10)
