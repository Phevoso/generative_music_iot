# Installer Scripts

This directory contains helper scripts that install all package and library dependencies needed for this project.<br/><br/>

## Compatability
When it comes to the client system, the installer scripts currently only support Debian-based Linux Distros. All the dependencies are listed in a later section for manual installation.<br/><br/>

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
`install_purr_data.sh` can be used to install <a href="https://agraef.github.io/purr-data/">Purr Data</a> on the client system along with all its dependencies.<br/><br/>
Usage:
```shell
$ ./install_purr_data.sh
```
<br/>

# List of Dependencies | Manual Installation
Following is a list of all dependencies.
<br/>

## <u>Client</u>

Packages  
* mosquitto
* mosquitto-clients

Python Libraries
* <a href="https://pypi.org/project/paho-mqtt/">paho-mqtt</a>
* <a href="https://pypi.org/project/pymongo/">pymongo</a>

Python libraries can be installed all at once by using the `requirmnets.txt` file.

Usage:
```shell
$ pip install -r requirments.txt
```
<br/>

## <u>Raspberry Pi</u>
The sesnor Raspberry Pi requires the same packages and python libraries as the client in addition to:
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

## <u>Purr Data Linux Dependencies</u>
* gconf-service
* libavifile-0.7c2
* libgconf-2-4
* libjpeg62-turbo
* libmagick++-6.q16-8
* libmagickcore-6.q16-6
* libmpeg3-2
* libquicktime2
