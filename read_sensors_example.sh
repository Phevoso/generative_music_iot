#!/bin/sh

# A simple shell script to run read_sensors_rpi.py script with arguments.
# You can use it to run the script on raspberry on-boot.
# Select if you want tostore sensor data in MongoDB by setting use_mongodb to true.
# If you do so, replace mongo_client_key with your own personal key.
# To learn more visit https://www.mongodb.com/docs/atlas/configure-api-access/.
# After you set-up an account you will also need to create a database and collections for
# sensor data as demonstrated in the python scirpt. Feel free to alter them to fit your needs.

ip_adress="mqtt.eclipseprojects.io"
mqtt_topic="sensors"

python3 /home/pi/generative_music_iot/python/mqtt/read_sensors_rpi.py -i $ip_adress -t $mqtt_topic &