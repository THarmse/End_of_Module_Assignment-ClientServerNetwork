#!/bin/bash

cd /opt/liverpool || exit 1  # exit if the directory does not exist

# Check if pip is installed; if not, install it
if ! command -v pip3 &> /dev/null
then
    # Download the pip installation script
    sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    # Install pip using the downloaded script
    sudo python3 get-pip.py
    # Remove the downloaded script
    sudo rm get-pip.py
fi

# Install Python dependencies from requirements.txt.
sudo pip3 install -r requirements.txt
