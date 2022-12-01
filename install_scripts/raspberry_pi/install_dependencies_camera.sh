#!/bin/bash

readc()
{
    if [ -t 0 ]; then
        saved_tty_settings=$(stty -g)
        stty -echo -icanon min 1 time 0
    fi
    eval "$1="
    while
        c=$(dd bs=1 count=1 2> /dev/null; echo .)
        c=${c%.}

        [ -n "$c" ] &&
            eval "$1=\${$1}"'$c
        [ "$(($(printf %s "${'"$1"'}" | wc -m)))" -eq 0 ]'; do
        continue
    done
    if [ -t 0 ]
    then
        stty "$saved_tty_settings"
    fi
}

sudo clear
echo -e "\e[1;33mWARNING: This script installs all package and python library dependencies for this project.\nYou should be using this on the Raspberry Pi running the camera.\n\nAdditionally, the camera functionality of the Raspberry Pi must be enabled.\n(You can enable the camera functionality by using \"sudo raspi-config\")\n\nPackage and Library dependenices are listed in the install_scripts directory's README if you want to install them manually.\n\nPress any key to continue or ESC to exit...\033[0m"

readc key

case "$key" in
  "$(printf '%b' '\033')")
  echo -e "\nExiting...\n";;
  *)

        echo -e "\n\e[1;33mInitiliazing Git Submodules...\033[0m"
        git submodule update --init --recursive

        if [[ "$(python3 --version 2>&1)" == *"not found"* ]]; then
            echo -e "\n\n\e[1;31mError: Python 3 not found!\n\nPyton 3.9 or higher is recommended for this project.\033[0m"
            exit
        fi

        echo -e "\n\e[1;33mInstalling Dependencies for Raspberry Pi...\033[0m"

        echo -e "\n\n\e[1;33mInstalling mosquitto and mosquitto-clients packages...\033[0m"

        #wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
        #sudo apt-key add mosquitto-repo.gpg.key

        sudo apt-get -y update
        #sudo rm mosquitto-repo.gpg.key
        sudo apt-get -y install mosquitto mosquitto-clients

        echo -e "\n\n\e[1;33mInstalling opencv package...\e[1;33m"
        sudo apt-get install -y python3-opencv

        echo -e "\n\n\e[1;33mMaking backup of current Mosquitto configuration file...\e[1;33m"
        sudo mv /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf_backup
        echo -e "\n\n\e[1;33mGenerating Mosquitto configuration file...\033[0m"
        sudo echo -e "pid_file /run/mosquitto/mosquitto.pid\npersistence true\npersistence_location /var/lib/mosquitto/\nallow_anonymous true\nlistener 1883 0.0.0.0\nlog_dest file /var/log/mosquitto/mosquitto.log\ninclude_dir /etc/mosquitto/conf.d" > mosquitto.conf
        sudo cp mosquitto.conf /etc/mosquitto/
        sudo rm mosquitto.conf

        echo -e "\n\n\e[1;33mRestarting service...\033[0m"
        sudo systemctl restart mosquitto

        echo -e "\n\n\e[1;33mDone.\033[0m"

        if [[ "$(pip --version 2>&1)" == *"not found"* ]]; then
            echo -e "\n\n\e[1;33mPython 3.x found but not pip!\n\nInstalling python3-pip on system....\033[0m"
            sudo apt-get -y install python3-pip
        fi

        echo -e "\n\n\e[1;33mInstalling Python Libraries\033[0m"

        pip install paho-mqtt pymongo

        echo -e "\n\n\e[1;33mUpdating PIP...\033[0m"
        python3 -m pip install pip --upgrade
        
        echo -e "\n\n\e[1;33mInstalling Raspberry Pi-Specific dependencies...\033[0m"
        pip install argparse numpy opencv-python tflite-support protobuf        

        echo -e "\n\n\e[1;33mDownloading TF Models...\033[0m"
        curl -L 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/object_detection/rpi/lite-model_efficientdet_lite0_detection_metadata_1.tflite' -o ../../TFLite/lite/examples/object_detection/raspberry_pi/efficientdet_lite0.tflite
        curl -L 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/object_detection/rpi/efficientdet_lite0_edgetpu_metadata.tflite' -o ../../TFLite/lite/examples/object_detection/raspberry_pi/efficientdet_lite0_edgetpu.tflite


        echo -e "\e[1;32m\n\nAll Done!\n\033[0m";;
esac