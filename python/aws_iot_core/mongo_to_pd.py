# A script that connects to MongoDB-Altas database and retrieves sensor data
# then passes them into Pure Data.
import socket
import datetime
import pymongo
import numpy as np
from pymongo import MongoClient
import urllib.parse
import os
import time
import pprint
import pprint
import argparse

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key", action="store", required=True, dest="key", 
                    help="Provide the mongoDB client key to store sensor data",)  
parser.add_argument("--host", default= "localhost", action="store", dest="host", 
                    help="Host to connect , default is localhost",)
parser.add_argument("-p", "--port", default=3000, action="store", dest="port", 
                    help="TCP port to open communication with Pure Data",)

# Using globals to simplify sample code
args = parser.parse_args()

#Get MongoDB Client key
mongoClientKey = args.key
host = args.host
port = int(args.port)

#This script will run for num_posts.
value = input("Enter the number of posts to retrieve.:\n")
num_posts = int(value)

# Set up client for MongoDB
mongoClient = MongoClient(mongoClientKey)

#Acess the data base
db = mongoClient.SensorData

#Acess BMP_180 data
coll_BMP = db.BMP_sensor
num_BMP = coll_BMP.estimated_document_count()
print(num_BMP)

#Acess GY-30 data
coll_light = db.light_lvl
num_GY30 = coll_light.estimated_document_count()

#Acess cameraPi data
coll_Cam = db.camera_pi
num_cam = coll_Cam.estimated_document_count()

#Acess DH11 data
coll_tempHum = db.temp_hum
num_tempHum = coll_tempHum.estimated_document_count()
print(num_tempHum)


# Create Arrays with Sensor Data

#--- BMP180 Array
my_id = coll_BMP.find()[num_posts]['_id']
bmp_data = coll_BMP.find({ '_id': {'$lt': my_id}}).sort([('_id', -1)])  # before
# after = coll_BMP.find({ '_id': {'$gt': my_id}}).sort('_id').limit(3)  # after
bmp_data_array = list(bmp_data)

#--- DH11 Array
my_id = coll_tempHum.find()[num_posts]['_id']
dh_data = coll_tempHum.find({ '_id': {'$lt': my_id}}).sort([('_id', -1)])  # before
dh_data_array = list(dh_data)

#--- GY-30 Array
my_id = coll_light.find()[num_posts]['_id']
gy30_data = coll_light.find({ '_id': {'$lt': my_id}}).sort([('_id', -1)])  # before
gy30_data_array = list(gy30_data)

#--- Camera Array
my_id = coll_Cam.find()[num_posts]['_id']
cam_data = coll_Cam.find({ '_id': {'$lt': my_id}}).sort([('_id', -1)])  # before
cam_data_array = list(cam_data)

totalNumPosts = num_BMP + num_cam + num_GY30 + num_tempHum

sensorNames = ["BMP180","DHT","GY30", "CameraPi"]


def getBMPCommandToPd(count):
    #Gather all data
    temperature = str(bmp_data_array[count].get('Temperature'))
    atm_pressure = str(bmp_data_array[count].get('Atmospheric Pressure'))
    altitude = str(bmp_data_array[count].get('Altitude'))
    sealevel_pressure = str(bmp_data_array[count].get('SeaLevel Pressure'))
    separator = " " # A whitespace character.
    print(sensorNames[0],": ",temperature, atm_pressure, altitude, sealevel_pressure)

    #Construct a string return it
    command = str(sensorNames[0]+ separator+
    temperature+separator+
    atm_pressure+separator+
    altitude+separator+
    sealevel_pressure+separator+";")
    #Return the command to send in Pure Data
    return command

def getDH11CommandToPd(count):
    humidity = str(dh_data_array[count].get('Humidity'))
    temperature = str(dh_data_array[count].get('Temperature'))
    time = str(dh_data_array[count].get('Time')).replace(":", ' ')
    print(sensorNames[1],": ", humidity, temperature, time)  

    #Construct a string return it
    command = sensorNames[1]+ " "+humidity + " " + temperature + " " + time + ";"
    return command

def getGY30CommandToPd(count):
    lightness = str(gy30_data_array[count].get('Lightness Level'))
    print(sensorNames[2],": ", lightness)
    #Construct a string return it
    command = sensorNames[2]+ " "+lightness + ";"
    return command

def getCameraCommandToPd(count):
    object_id = str(cam_data_array[count].get('Object_ID'))
    center = str(cam_data_array[count].get('Centroid'))
    center = center.replace("[", '')
    center  = center.replace("]", '')
    print(sensorNames[3], object_id, center)

    #Construct the command and return it
    command = sensorNames[3]+ " "+object_id+ " " + center+ ";"
    return command


# Open socket to send data to PD
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to host
s.connect((host, port))

# Start iterating 
count = 0
while count < num_posts:
    for coll_name in db.list_collection_names():

        if coll_name == "BMP_sensor":
            bmp_command = getBMPCommandToPd(count)
            s.send(bmp_command.encode())
            time.sleep(0.5)
        elif coll_name == "temp_hum":
            dh11_command = getDH11CommandToPd(count)
            s.send(dh11_command.encode())
            time.sleep(0.5)
        elif coll_name == "light_lvl":
            gy30_command = getGY30CommandToPd(count)
            s.send(gy30_command.encode())
            time.sleep(0.5)
        elif coll_name == "camera_pi":
            camera_command = getCameraCommandToPd(count)
            s.send(camera_command.encode())
            time.sleep(0.5)
    count += 1
    time.sleep(0.1)






