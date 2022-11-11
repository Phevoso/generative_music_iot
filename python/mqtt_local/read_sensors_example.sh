#!/bin/sh

# A simple shell script to run read_sensors_rpi.py script with arguments.
# You can use it to run the script on raspberry on-boot.
# Replace mongo_client_key with your own personal key. To learn more see https://www.mongodb.com/docs/atlas/configure-api-access/

ip_adress="localhost"
client_name="broker.hivemq.com"
mqtt_topic="sensors"
username = "testUser"
password = "1234"
mongo_client_key="insert personal client key"

python3 /home/pi/generative_music_iot/python/mqtt_local/read_sensors_rpi.py -i $ip_adress -c $client_name -t $mqtt_topic -m $mongo_client_key -u $username -p $password &