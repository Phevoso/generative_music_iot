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
echo -e "\e[1;33mWARNING: This script only supports Debian-based Distros.\n\nPress any key to continue or ESC to exit...\033[0m"

readc key

case "$key" in
  "$(printf '%b' '\033')") 
  echo -e "\nExiting...\n";;
  *)  echo -e "\n\n\e[1;33mDownloading Purr-Data package file...\033[0m"
      wget https://download.opensuse.org/repositories/home:/aggraef:/purr-data-jgu/Debian_11/amd64/purr-data_2.17.0+git4948+0218c207-1_amd64.deb
      echo -e "\n\n\e[1;33mInstalling dependencies...\033[0m"
      sudo apt-get install -y gconf-service libavifile-0.7c2 libgconf-2-4 libmagick++-6.q16-8 libmagickcore-6.q16-6 libmpeg3-2 libquicktime2
      echo -e "\n\n\e[1;33mDownloading libjpeg62-turbo package file...\033[0m"
      wget http://ftp.de.debian.org/debian/pool/main/libj/libjpeg-turbo/libjpeg62-turbo_2.1.2-1+b1_amd64.deb
      echo -e "\n\n\e[1;33mInstalling libjpeg62-turbo package...\033[0m"
      sudo dpkg -i libjpeg62-turbo_2.1.2-1+b1_amd64.deb
      echo -e "\n\n\e[1;33mInstalling Purr-Data...\033[0m"
      sudo dpkg -i purr-data_2.17.0+git4948+0218c207-1_amd64.deb
      echo -e "\n\n\e[1;33mPerforming cleanup...\033[0m"
      sudo rm purr-data_2.17.0+git4948+0218c207-1_amd64.deb
      sudo rm libjpeg62-turbo_2.1.2-1+b1_amd64.deb
      echo -e "\e[1;32m\n\nAll Done!\n\033[0m";;
esac

