###This project reads two DHT22 temperature and humidity sensors, and activates the buzzer when the sensor outputs exceed the values ​​we specify. Additionally, all values are sent to the InfluxDB (version 1) database.

import time
import Adafruit_DHT
from influxdb import InfluxDBClient
import RPi.GPIO as GPIO

# Sensor and buzzer configuration
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN_1 = 4  # First sensor GPIO pin
DHT_PIN_2 = 17 # Second sensor GPIO pin
BUZZER_PIN = 18

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# InfluxDB configuration for 1.x
influx_host = 'localhost'
influx_port = 8086
influx_dbname = 'sensor_data_DB'  # Your database name
influx_user = 'user_tg'  # If authentication is enabled, enter your username
influx_password = 'password_tg'  # If authentication is enabled, enter your password

# Create an InfluxDB client
client = InfluxDBClient(host=influx_host, port=influx_port, username=influx_user, password=influx_password, database=influx_dbname)

def read_sensor(sensor, pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        return None, None

def write_to_influxdb(sensor_id, temperature, humidity):
    json_body = [
        {
            "measurement": "environment",
            "tags": {
                "sensor": sensor_id,
                "location": "office"
            },
            "fields": {
                "temperature": temperature,
                "humidity": humidity
            }
        }
    ]
    client.write_points(json_body)

def check_conditions_and_alert(temperature, humidity):
    if temperature is not None and humidity is not None:
        if temperature > 30 or humidity > 70:
            print("Warning: High Temperature or Humidity!")
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)

try:
    while True:
        # Read data from the first sensor
        temp_1, hum_1 = read_sensor(DHT_SENSOR, DHT_PIN_1)
        if temp_1 is not None and hum_1 is not None:
            print(f"Sensor 1 -> Temperature: {temp_1:.2f} C  Humidity: {hum_1:.2f}%")
            write_to_influxdb("sensor_1", temp_1, hum_1)
            check_conditions_and_alert(temp_1, hum_1)
        else:
            print("Sensor 1 error.")

        # Read data from the second sensor
        temp_2, hum_2 = read_sensor(DHT_SENSOR, DHT_PIN_2)
        if temp_2 is not None and hum_2 is not None:
            print(f"Sensor 2 -> Temperature: {temp_2:.2f} C  Humidity: {hum_2:.2f}%")
            write_to_influxdb("sensor_2", temp_2, hum_2)
            check_conditions_and_alert(temp_2, hum_2)
        else:
            print("Sensor 2 error.")
        
        # Wait for 10 seconds
        time.sleep(60)

except KeyboardInterrupt:
    print("Program terminated.")

finally:
    GPIO.cleanup()
    client.close()
