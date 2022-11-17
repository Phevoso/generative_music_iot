# A script that reads sensor data from the Raspberry Pi
# then publishes the data to MQTT and stores them in MongoDB-Atlas.

import paho.mqtt.client as mqtt
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import smbus
import pymongo
from pymongo import MongoClient
import time
import datetime
import json
import pprint
from connection_arguments import *


#Initialize parser with common arguments
local_parser = get_generic_parser()

#Add Script specific arguments
local_parser.add_argument('--interval', '-in', type=int, default=1, help="Specify interval at which sensor data is published.")
local_parser.add_argument('--stagger', '-s', type=int, help="Stagger publish of data between sensors by a specified amount of sconds.")

#Parse info required for the mqtt connection and specific to this sensor
server_info = local_parser.parse_args()

#Connet to MQTT
mqttc = mqtt.Client()
mqttc.connect(server_info.ip_adress, 1883)

if server_info.use_mongodb:
    #Connect to mongoDB
    mongoClient = MongoClient(server_info.mongo_client_key)
    # Define mongoDB database
    db=mongoClient.SensorData
    # Define collections for each sensor
    bmpCollection = db.BMP_sensor
    dthCollection=db.temp_hum
    gy30Collection=db.light_lvl

# ----- Read Sensor Data -----

# Define some constants from the datasheet
DEVICE     = 0x23 # Default device I2C address
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
time.sleep(1)

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

def readBMP180Data():
    sensor = BMP085.BMP085()
    post = []
    temp = float(sensor.read_temperature())
    press = float(sensor.read_pressure())
    alt = float(sensor.read_altitude())
    sealvl = float(sensor.read_sealevel_pressure())
    utc_time = str(datetime.datetime.utcnow())

    post = { 
        "Sensor Name":"BMP180",
        "Temperature": temp,
        "Atmospheric Pressure": press,
        "Altitude": alt,
        "SeaLevel Pressure": sealvl,
        "Time": utc_time 
    }
    return post

def readDTHData():
    utc_time = str(datetime.datetime.now().time())
    utc_time = utc_time.replace(":", ' ')
    humidity, temperature = Adafruit_DHT.read_retry(11,4)

    if (str(temperature) == "None"):
        temperature = 25
    elif(str(humidity) == "None"):
        humidity = 30    
    post = {
        "Sensor Name":"DTH",
        "Temperature":temperature,
        "Humidity": humidity,
        "Time": str(utc_time)
    }  
    return post

def readGY30Data():
    lightLevel= float(readLight())
    print("Light Level : " + format(lightLevel,'.2f') + " lx")
    utc_time = str(datetime.datetime.utcnow())
    
    post = {
        "Sensor Name":"GY30",
        "Lightness Level": float(lightLevel),
        "Time": str(utc_time)
    }
    return post

# ----- Publish Sensor Data -----

sensorNames = ["BMP180", "DTH", "GY30"]

while True:

    #Read sensor data and convert it to JSON
    
    #BMP180
    bmpData = readBMP180Data()
    pprint.pprint(bmpData)
    bmp_data_json = json.dumps(bmpData)     
    
    #DTH
    dthData = readDTHData()
    pprint.pprint(dthData)
    dth_data_json = json.dumps(dthData) 

    #GY30
    gy30Data = readGY30Data()
    pprint.pprint(gy30Data)
    gy30_data_json = json.dumps(gy30Data)

    #Store in MngoDB
    if server_info.use_mongodb:
        bmpCollection.insert_one(bmpData)
        dthCollection.insert_one(dthData)
        gy30Collection.insert_one(gy30Data)

    # Publish messages to MQTT
    mqttc.publish(server_info.topic, str(bmp_data_json))
    time.sleep(server_info.stagger) if server_info.stagger != 'None' else None        

    mqttc.publish(server_info.topic, str(dth_data_json))
    time.sleep(server_info.stagger) if server_info.stagger != 'None' else None

    mqttc.publish(server_info.topic, str(gy30_data_json))       
                
    time.sleep(server_info.interval)   