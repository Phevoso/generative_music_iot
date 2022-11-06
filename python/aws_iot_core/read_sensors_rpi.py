
# A script that reads sensor data from the Raspberry Pi
# then publishes the data AWS-IoT-Core and stores them in MongoDB-Atlas.


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import smbus
import numpy as np
import pymongo
from pymongo import MongoClient
import logging
import time
import datetime
import argparse
import json
import pprint
import pandas as pd

AllowedActions = ['publish']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="sensorPub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="home", help="Targeted topic")
parser.add_argument("-m", "--mode", action="store", dest="mode", default="publish",
                    help="Operation modes: %s"%str(AllowedActions))
parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                    help="Message to publish")
parser.add_argument("-d", "--dbMongo", action="store", required=True, dest="dbMongo", 
                    help="Provide the mongoDB client key to store sensor data",)

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
port = args.port
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.mode not in AllowedActions:
    parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
    exit(2)

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
    port = 443
if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

#Connect to AWS IoT Core
myMQTTClient = AWSIoTMQTTClient("rpi-sensor") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint(host, port)
myMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
print ('Initiating Realtime Data Transfer From Raspberry Pi...')
myMQTTClient.connect()

#Read Sensor Data

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

#Prepare mongoDB
#Connect to mongoDB
mongoClient = MongoClient(str(args.dbMongo))
db=mongoClient.SensorData

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

            #Publish JSON to IoT Core
            myMQTTClient.publish(topic,messageJSON, 1)

            #Publish JSON to MongoDB
            bmpCollection.insert_one(bmpData)

        elif sensor == sensorNames[1]:

            dthData = readDTHData()
            pprint.pprint(dthData)
            messageJSON = json.dumps(dthData)

            myMQTTClient.publish(topic,messageJSON, 1)

            dthCollection.insert_one(dthData)

        elif sensor == sensorNames[2]:

            gy30Data = readGY30Data()
            pprint.pprint(gy30Data)
            messageJSON = json.dumps(gy30Data)

            myMQTTClient.publish(topic,messageJSON, 1)
            
            gy30Collection.insert_one(gy30Data)
        time.sleep(1)   