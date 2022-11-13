# This script uses the Message Broker to receive messages from an MQTT connection.
# subscribes to a topic, and then passes the received messages though sockets in Pure Data.

import json
import socket
import pprint
import paho.mqtt.client as mqtt
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


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    payload = msg.payload
    # Convert incoming json string to python dict
    json_dict = json.loads(str(payload.decode('utf-8')))
    #Send it to Pure Data
    sensorDataToPd(json_dict)

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

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


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.connect(server_info.ip_adress, 1883, 60)
mqttc.subscribe(server_info.topic)

mqttc.loop_forever()