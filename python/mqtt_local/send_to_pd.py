import time
import os
import paho.mqtt.client as mqtt
import json
import socket
import pprint
from connection_arguments import *

#Parse info required for the mqtt connection and specific to this sensor
server_info = parse_args()

#Pure Data info
pd_host = server_info.pd_host
pd_port = int(server_info.pd_port)

# Open socket to send data to PD
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to host
s.connect((pd_host, pd_port))

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode('utf-8')))

    # Convert incoming json string to python dict
    json_dict = json.loads(str(message.decode('utf-8')))

    #Send it to Pure Data
    sensorDataToPd(json_dict)


def sensorDataToPd(message=''):
    #Print the received JSON
    pprint.pprint(message)
    #Create the pdsend command  
    message = extractSensorData(message)
    message+=";"
    s.send(message.encode())

def extractSensorData(message):
    SensorName = message.get('Sensor Name')
    messageToPd = ""

    if SensorName == "BMP180":

        temperature = str(message.get('Temperature'))
        atmosphericPresure = str(message.get('Atmospheric Pressure'))
        alitude = str(message.get('Altitude'))
        seaLevelPressure = str(message.get('SeaLevel Pressure'))
        messageToPd  = SensorName+" "+ temperature+ " "+atmosphericPresure +" "+ alitude + " "+seaLevelPressure

    elif SensorName == "DTH":

        temp= str(message.get('Temperature'))
        humidity= str(message.get('Humidity'))
        utc_time = str(message.get('Time'))
        messageToPd = SensorName+" "+temp+" "+humidity + " " + utc_time

    elif SensorName == "GY30":

        lightLevel= str(message.get('Lightness Level'))
        messageToPd = SensorName+" "+lightLevel

    elif SensorName == "CameraPi":

        coordinates = str(message.get("Coordinates"))
        coordinates = coordinates.replace("[", '')
        coordinates  = coordinates.replace("]", '')
        coordinates  = coordinates.replace(",", '')
        score = message.get("Score")
        label = message.get("Label")
        messageToPd = SensorName+" "+coordinates+" "+label+" "+score

    return messageToPd

# Harvesting Data from the Mqtt Server
print("creating new mqtt client instance")
client = mqtt.Client(server_info.client_name)

print("connecting to broker")
client.connect(server_info.ip_adress, 1883)

print("Subscribing to topic", server_info.topic)
client.subscribe(server_info.topic)

client.on_message=on_message
client.loop_start()

while True:
        print(".") #while no data is send , print this
        time.sleep(3)