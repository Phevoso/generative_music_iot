# A script that reads sensor data from the Raspberry Pi
# then publishes the data to MQTT and stores them in MongoDB-Atlas.

import paho.mqtt.client as mqtt
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import smbus
import pymongo
from pymongo import MongoClient
import logging
import time
import datetime
import argparse
import json
import pprint
from connection_arguments import *

#Parse info required for the mqtt connection and specific to this sensor
server_info = parse_args()

#Connet to MQTT
mqttc = mqtt.Client(server_info.client_name)
mqttc.username_pw_set(server_info.username, server_info.password)
mqttc.connect(server_info.ip_adress, 1883)

#Connect to mongoDB
mongoClient = MongoClient(server_info.mongo_client_key)
db=mongoClient.SensorData

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


#BMP180
bmpCollection = db.BMP_sensor

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

#DTH 
dthCollection=db.temp_hum

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

#GY-30
gy30Collection=db.light_lvl

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

sensorNames = ["BMP180", "DTH", "GY30"]

while True:

    for sensor in sensorNames:
        if sensor == sensorNames[0]:
            #Read sensor data and convert it to JSON
            bmpData = readBMP180Data()
            pprint.pprint(bmpData)
            messageJSON = json.dumps(bmpData)

            # Publish message to MQTT
            mqttc.publish(server_info.topic, str(messageJSON))

            #Publish JSON to MongoDB
            bmpCollection.insert_one(bmpData)

        elif sensor == sensorNames[1]:

            dthData = readDTHData()
            pprint.pprint(dthData)
            messageJSON = json.dumps(dthData)

            mqttc.publish(server_info.topic, str(messageJSON))

            dthCollection.insert_one(dthData)

        elif sensor == sensorNames[2]:

            gy30Data = readGY30Data()
            pprint.pprint(gy30Data)
            messageJSON = json.dumps(gy30Data)

            mqttc.publish(server_info.topic, str(messageJSON))
            
            gy30Collection.insert_one(gy30Data)
        time.sleep(1)   