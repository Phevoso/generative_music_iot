# Generative Music using IoT Sensor Data.

## Description
This repo holds an IoT installation that converts MQTT messages from sensor data to generative music using Pure Data.

![alt text](https://github.com/Phevoso/Generative-Music-with-IOT/blob/develop/images/iot_diagram.svg?raw=true)

## Services and Software
- This project uses the [AWS IoT-Core](https://aws.amazon.com/iot-core/) to publish/subscribe MQTT messages.
- [MongoDB Altas](https://www.mongodb.com/cloud/atlas) as a database to store and retrieve data.
- Pure Data to create generative music. You can use [Pure Data Vanilla](https://puredata.info/downloads) or [Purr Data](https://agraef.github.io/purr-data/) .

### Prerequirements
- You will need an AWS account in order to add your own "things" (raspberry, laptop e.c.t) to the Iot C.
The certificates and keys provided by the AWS-IoT are required to run the scripts and connect successfully.
To set an account and get started, follow the [Developer's Guide](https://docs.aws.amazon.com/iot/latest/developerguide/iot-gs.html)
- To get started with MongoDB Altas follow this guide [here](https://docs.atlas.mongodb.com/getting-started/).


## Hardware
- [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) (for sensors)
- [Raspberry Pi 4 Model B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) (surveillance camera)


### Sensors Used
|  Sensor Name   |          Description           |        Measured Data    |
| ---------- | ------------------------------- | -------------------------- |
| [BMP180](https://www.adafruit.com/product/1603) | Barometric Pressure Sensor | Temperature, Altitude, Atmospheric Pressure |
| [DT11](https://www.adafruit.com/product/386)    | Basic Temperature Sensor   | Temperature , Humidity                      |
| [GY-30](http://wiki.sunfounder.cc/index.php?title=GY-30_Digital_Light_Intensity_Measuring_Module)    | Ambient Light Sensor   | Light Level (lux) |
| [Pi Camera Module](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)   | Any camera module should do | Number of objects detected, (X,Y)coordinates |

### Third-party libraries
- [TensorFlow Lite](https://github.com/tensorflow/tflite-micro) used for object detection with the camera module.

## Usage
You can either receive messages in real-time from the IoT-Core or use MongoDB to retrieve stored messages from your database.

-Inside the repository there are 3 bash scripts, each runs a python script that requires some arguments from the command-line.
Edit these scripts to pass your credentials, AWS certificates e.c.t 

- `_main.pd` Open the main PD-patch before you start sending messages to Pure Data,
 it will automaticly open a socket to listen to messages send from python. 
 If you want to use a custom port you should configure both PD and python, set a custom port from `_main.pd` GUI and from the respective input argument in `sendToPureData.py`

- `readSensorData.py` , Reads data from all sensors and publishes them to the MQTT IoT Core.

- `sendToPureData.py` Receives messages from the IoT-Core and uses a socket to pass them in Pure Data.

- `mongoToPureData.py` Receives messages from Mongo-DB Altas database and uses a socket to pass them in Pure Data.


