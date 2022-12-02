# Installer Scripts

This directory contains helper scripts that install all package and library dependencies needed for this project.<br/><br/>

## Compatability
When it comes to the IoT server system, the installer scripts currently only support Debian-based Linux Distros. All the dependencies are listed in a later section for manual installation.<br/><br/>

Python 3.9 or higher is recommended for this project.<br/><br/>

# Usage
## Dependencies Script
`install_dependencies.sh` in each respective subdirectory can be used to install the required packages and python libraries each device needs.<br/><br/>
Usage:
```shell
$ ./install_dependencies.sh
```
<br/>

## Purr Data Script
`install_purr_data.sh` can be used to install <a href="https://agraef.github.io/purr-data/">Purr Data</a> on the IoT server along with all its dependencies.<br/><br/>
Usage:
```shell
$ ./install_purr_data.sh
```
<br/>

# List of Dependencies | Manual Installation
Following is a list of all dependencies.
<br/>

## <u>IoT server</u>

Packages  
* mosquitto
* mosquitto-clients

Python Libraries
* <a href="https://pypi.org/project/paho-mqtt/">paho-mqtt</a>
* <a href="https://pypi.org/project/pymongo/">pymongo</a>

Python libraries can be installed all at once by using the `requirments.txt` file.

Usage:
```shell
$ pip install -r requirments.txt
```
<br/>

## <u>Raspberry Pi</u> | <u>Sensors</u>
The Raspberry Pi running the sesnors requires the same packages and python libraries as the IoT server in addition to:
<br/>

Additional Python Libraries
* <a href="https://pypi.org/project/Adafruit-BMP/">Adafruit-BMP</a>
* <a href="https://pypi.org/project/Adafruit-DHT/">Adafruit-DHT</a>
* <a href="https://pypi.org/project/smbus/">smbus</a>

Python libraries can be installed all at once by using the `requirmnets_sensors.txt` file.

Usage:
```shell
$ pip install -r requirments_sensors.txt
```
<br/>

## <u>Raspberry Pi</u> | <u>Camera</u>
The Camera Raspberry Pi requires the same packages and python libraries as the IoT server in addition to:
<br/>

Additional Packages
* python3-opencv

<br/>

Additional Python Libraries
* <a href="https://pypi.org/project/argparse/">argparse</a>
* <a href="https://pypi.org/project/numpy/">numpy</a>
* <a href="https://pypi.org/project/opencv-python/">opencv-python</a>
* <a href="https://pypi.org/project/tflite-support/">tflite-support</a>
* <a href="https://pypi.org/project/protobuf/">protobuf</a>

Python libraries can be installed all at once by using the `requirments_camera.txt` file.

Usage:
```shell
$ pip install -r requirments_camera.txt
```

## Enabling the camera on the Raspberry Pi
Camera support can be enabled from the raspi-config menu by running:

```shell
$ sudo raspi-config
```

<br/>

## <u>Purr Data Linux Dependencies</u>
* gconf-service
* libavifile-0.7c2
* libgconf-2-4
* libjpeg62-turbo
* libmagick++-6.q16-8
* libmagickcore-6.q16-6
* libmpeg3-2
* libquicktime2
