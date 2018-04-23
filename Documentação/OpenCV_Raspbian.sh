#!/bin/bash

clear 
SUDO=''
if [ "$EUID" -ne 0 ]
    then
        echo "É necessário que esse scrip execute como Root"
        sudo -s
fi

echo "Install the required build-tools (some might already be installed on your system)."
echo "If one of the packages cannot be found, try a newer version number (e.g. libdb5.4-dev instead of libdb5.3-dev)."
apt-get update
apt-get upgrade
apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev

echo "Download and install Python 3.6. When downloading the source code, select the most recent release of Python 3.6,"
echo "available on the official site. Adjust the file names accordingly."
echo "https://www.python.org/ftp/python/3.6.5/"
wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz
tar xf Python-3.6.5.tar.xz
cd Python-3.6.5
./configure
make
sudo make altinstall

echo "Optionally: Delete the source code and uninstall the previously installed packages. When uninstalling the packages, make"
echo "sure you only remove those that were not previously installed on your system. Also, remember to adjust version numbers if necesarry"
rm -r Python-3.6.5
rm Python-3.6.5.tar.xz
apt-get --purge remove build-essential tk-dev
apt-get --purge remove libncurses5-dev libncursesw5-dev libreadline6-dev
apt-get --purge remove libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
apt-get --purge remove libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
apt-get autoremove
apt-get clean

clear