#!/bin/bash

sudo clear
echo -e "\e[1;33mWARNING: If you're using this script on the client side, it currently only supports Debian-based distros.\nPackage and Library dependenices are listed in this directory's README if you want to install them manually.\033[0m"
echo -e "\n\nInstallers Available\n==========================\n1 = Raspberry Pi\n2 = Debian-Based Client PC\n==========================\n\n"
read -p "Choose a device to install dependecies on: " choice

if [ $choice == 1 ] ; then
    echo -e "\n\e[1;33mInstalling Dependencies for Raspberry Pi...\033[0m"
elif [ $choice == 2 ]; then
    echo -e "\n\e[1;33mInstalling Dependencies for Debian Client...\033[0m"
else
    echo -e "\n\033[0;31mError: \"${choice}\", No such coice.\n\033[0m"
    exit 2
fi

echo "Installing mosquitto and mosquitto-clients packages..."

wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key

sudo apt-get -y update
sudo rm mosquitto-repo.gpg.key
sudo apt-get -y install mosquitto mosquitto-clients

echo -e "\n\n\e[1;33mMaking backup of current Mosquitto configuration file...\e[1;33m"
sudo mv /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf_backup
echo -e "\n\n\e[1;33mGenerating Mosquitto configuration file...\033[0m"
sudo echo -e "pid_file /run/mosquitto/mosquitto.pid\npersistence true\npersistence_location /var/lib/mosquitto/\nallow_anonymous true\nlistener 1883 0.0.0.0\nlog_dest file /var/log/mosquitto/mosquitto.log\ninclude_dir /etc/mosquitto/conf.d" > mosquitto.conf
sudo cp mosquitto.conf /etc/mosquitto/
sudo rm mosquitto.conf

echo -e "\n\n\e[1;33mRestarting service...\033[0m"
sudo systemctl restart mosquitto

echo -e "\n\n\e[1;33mDone.\033[0m"

echo -e "\n\n\e[1;33mInstalling Python Libraries\033[0m"

pip install paho-mqtt pymongo

if [ $choice == 1 ]; then
    echo -e "\n\n\e[1;33mInstalling Raspberry Pi-Specific dependencies...\033[0m"
    pip install Adafruit-BMP Adafruit-DHT smbus
fi

echo -e "\e[1;32m\n\nAll Done!\n\033[0m"
