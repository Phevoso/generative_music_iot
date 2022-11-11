#!/bin/sh

# A shell scirpt that executes send_to_pd.py
# insert the raspberry pi I.P adress

ip_adress="192.168.1.12"
client_name="broker.hivemq.com"
mqtt_topic="sensors-pi"
username = "testUser"
password = "1234"
pd_host="localhost"
pd_port="3000"

python3 send_to_pd.py -i $ip_adress -c $client_name -t $mqtt_topic -u $username -p $password --pd-host $pd_host &