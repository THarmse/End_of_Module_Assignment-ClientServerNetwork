#!/bin/bash

# Debugging: Print the current directory.
echo "Current directory is $(pwd)"

# Create and navigate to /opt/liverpool if it doesn't exist
if [ ! -d "/opt/liverpool" ]; then
  echo "/opt/liverpool does not exist. Creating..."
  sudo mkdir -p /opt/liverpool
fi

cd /opt/liverpool || { echo "Error changing directory to /opt/liverpool"; exit 1; }

# Check if pip3 is installed; if not, install it.
if ! command -v pip3 &> /dev/null; then
  echo "pip3 is not installed. Installing..."
  sudo curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  sudo python3 get-pip.py
  sudo rm get-pip.py
fi

# Install Python dependencies from requirements.txt.
sudo pip3 install -r requirements.txt
