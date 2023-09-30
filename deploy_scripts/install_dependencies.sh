#!/bin/bash

cd "$PWD" || exit 1  # exit if the directory does not exist

# Check if pip is installed; if not, install it
if ! command -v pip &> /dev/null
then
    sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python3 get-pip.py
    sudo rm get-pip.py
fi

# Install Python dependencies
sudo pip install -r requirements.txt
