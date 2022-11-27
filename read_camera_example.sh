#!/bin/sh

ip_adress="mqtt.eclipseprojects.io"
mqtt_topic="sensors"

python3 TFLite/lite/examples/object_detection/raspberry_pi/detect.py -i $ip_adress -t $mqtt_topic &