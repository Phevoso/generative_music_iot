#!/bin/sh

# A shell scirpt that executes send_to_pd.py with the required arguments.

ip_adress="mqtt.eclipseprojects.io"
mqtt_topic="sensors"
pd_host="localhost"
pd_port="3000"

python3 python/mqtt/send_to_pd.py -i $ip_adress -t $mqtt_topic --pd-host $pd_host
