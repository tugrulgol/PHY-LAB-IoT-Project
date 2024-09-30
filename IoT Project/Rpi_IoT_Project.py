import Adafruit_DHT
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import time

# GPIO Pin Configurations
DHT_SENSOR1 = Adafruit_DHT.DHT22
DHT_PIN1 = 4  # GPIO 4
DHT_SENSOR2 = Adafruit_DHT.DHT22
DHT_PIN2 = 17  # GPIO 17
BUZZER_PIN = 22  # GPIO 22

# MQTT Configuration
MQTT_BROKER = "localhost"  # MQTT Broker adresi
MQTT_PORT = 1883  # MQTT portu
MQTT_TOPIC_TEMPERATURE1 = "sensor1/temperature"
MQTT_TOPIC_HUMIDITY1 = "sensor1/humidity"
MQTT_TOPIC_TEMPERATURE2 = "sensor2/temperature"
MQTT_TOPIC_HUMIDITY2 = "sensor2/humidity"
MQTT_TOPIC_ALERT = "sensor/alert"

# InfluxDB configuration for 1.x
influx_host = 'localhost'
influx_port = 8086
influx_dbname = 'sensor_data_DB'  # Your database name
influx_user = 'user_tg'  # If authentication is enabled, enter your username
influx_password = 'password_tg'  # If authentication is enabled, enter your password

# Create an InfluxDB client
influxdb_client = InfluxDBClient(host=influx_host, port=influx_port, username=influx_user, password=influx_password, database=influx_dbname)

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# MQTT Client Setup
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def publish_data(topic, message):
    client.publish(topic, message)

def buzz_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def buzz_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    
## Write InfluxDB
def write_to_influxdb(sensor_id, temperature, humidity):
    json_body = [
        {
            "measurement": "environment",
            "tags": {
                "sensor": sensor_id,
                "location": "ISU-PHY-LAB"
            },
            "fields": {
                "temperature": temperature,
                "humidity": humidity
            }
        }
    ]
    influxdb_client.write_points(json_body)

try:
    while True:
        humidity1, temperature1 = Adafruit_DHT.read_retry(DHT_SENSOR1, DHT_PIN1)
        humidity2, temperature2 = Adafruit_DHT.read_retry(DHT_SENSOR2, DHT_PIN2)
        
        if humidity1 is not None and temperature1 is not None:
            temperature1 = round(temperature1, 4)
            humidity1 = round(humidity1, 4)
            publish_data(MQTT_TOPIC_TEMPERATURE1, f"{temperature1} C")
            publish_data(MQTT_TOPIC_HUMIDITY1, f"{humidity1} %")
            
            # Write the values to InfluxDB
            write_to_influxdb("sensor1", temperature1, humidity1)
        else:
            publish_data(MQTT_TOPIC_ALERT, "Sensor 1 Error")
        
        if humidity2 is not None and temperature2 is not None:
            temperature2 = round(temperature2, 4)
            humidity2 = round(humidity2, 4)
            publish_data(MQTT_TOPIC_TEMPERATURE2, f"{temperature2} C")
            publish_data(MQTT_TOPIC_HUMIDITY2, f"{humidity2} %")
            
            # Write the values to InfluxDB
            write_to_influxdb("sensor2", temperature2, humidity2)
        else:
            publish_data(MQTT_TOPIC_ALERT, "Sensor 2 Error")

        # Check thresholds
        if (humidity1 and temperature1 and (temperature1 > 30 or humidity1 > 70)) or \
           (humidity2 and temperature2 and (temperature2 > 30 or humidity2 > 70)):
            publish_data(MQTT_TOPIC_ALERT, "Threshold Exceeded")
            buzz_on()
        else:
            buzz_off()

        time.sleep(10)

except KeyboardInterrupt:
    GPIO.cleanup()
    client.close()
