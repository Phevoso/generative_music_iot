# Generative Music using IoT Sensor Data.

## Description
This repo holds the code for my thesis presented in the Technologial Educational Institute of Crete.

The purpose of this thesis is a theoretical study and development of an integrated system responsible for recording data harvested from the environment with the use of sen- sors and Internet of Things technologies, as well as the development of a generative music application, dependent on environmental data. This thesis is divided into two sections, the first one is concerned with the study of programming techniques and the development process of an Internet of Things sensor network, and the second focuses on the application and study regarding generative music methods and digital signal processing.

## Services and Software
- This project uses the MQTT protocol to send and receive sensor data, in the repo you have the option to use either the open source [mosquitto MQTT](https://mosquitto.org) or the [AWS IoT-Core](https://aws.amazon.com/iot-core/) service.
- [MongoDB Altas](https://www.mongodb.com/cloud/atlas) is used as a database to store and retrieve data.
- Pure Data to create generative music. You can use [Pure Data Vanilla](https://puredata.info/downloads) or [Purr Data](https://agraef.github.io/purr-data/) .

### Prerequirements
- Follow the instructions at [install_scripts](https://github.com/Phevoso/generative_music_iot/blob/main/install_scripts/README.md) to install all the requirements.
You will also python installed version 3 and above.
- For IoT Core you will need an AWS account in order to add your own "things" (raspberry, laptop e.c.t) to the Iot C.
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

### Sensor connection with the raspberry pi

#### - BMP180 
![alt text](https://github.com/Phevoso/generative_music_iot/blob/main/images/bmp180_schematic.jpg?raw=true)
#### - DTH11 
![alt text](https://github.com/Phevoso/generative_music_iot/blob/main/images/dth11_schematic.jpg?raw=true)
#### - GY-30
![alt text](https://github.com/Phevoso/generative_music_iot/blob/main/images/gy-30_schematic.jpg?raw=true)

### Third-party libraries
- [TensorFlow Lite](https://github.com/tensorflow/tflite-micro) used for object detection with the camera module.

## Usage
You can either receive messages in real-time from the IoT-Core or use MongoDB to retrieve stored messages from your database.

-Inside the repository there are 3 bash scripts, each runs a python script that requires some arguments from the command-line.
Edit these scripts to pass your credentials, AWS certificates e.c.t 

- `_main.pd` Open the main PD-patch before you start sending messages to Pure Data,
 it will automaticly open a socket to listen to messages send from python. 
 If you want to use a custom port you should configure both PD and python, set a custom port from `_main.pd` GUI and from the respective input argument in `send_to_pd.py`

- `read_sensors_rpi.py` , Reads data from all sensors and publishes them to the MQTT IoT Core.

- `send_to_pd.py` Receives messages from the IoT-Core and uses a socket to pass them in Pure Data.

- `mongo_to_pd.py` Receives messages from Mongo-DB Altas database and uses a socket to pass them in Pure Data.

## Pd interface

<img src="https://github.com/Phevoso/generative_music_iot/blob/main/images/gui.PNG " width="1000">

### Dashboard
- Inside the `_main.pd` you can visualize the MQTT sensor data that are being received from the subscriber in the `dashboard`
- Control the output volume of the whole pd patch or it's instruments individually.
- Select a music scale.

### Instruments
- You can actually start generating music by hitting the `Start` button. 
- `Randomize` will set all parameters to a random value.
- Most of the instrument parameters are mapped on some kind of enviromental data but you can also tweek them in real-time.

### FX
- `Noise Gen` uses filtered noise to simulate weather soundscapes such as wind or rain.
- `Reverb` A reverb unit based onJon Dattorro's reverberator.
- `Delay` A simple feedback delay-line
- `VCF filter` Voltage Controlled Filter mainly used for the `vangex` instrument, which attempts to simulate the Blade Runner synths.









