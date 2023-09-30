#!/bin/bash

# Print the current directory for debugging purposes.
echo "Current directory is $PWD"

# Define the deployment directory.
deploy_dir="/opt/liverpool"

# Check if the deployment directory exists; if not, create it.
if [ ! -d "$deploy_dir" ]; then
    echo "$deploy_dir does not exist. Creating..."
    mkdir -p "$deploy_dir"
fi

# Change to the deployment directory.
cd "$deploy_dir" || { echo "Could not navigate to $deploy_dir. Exiting."; exit 1; }

# Check if requirements.txt exists in the deployment directory; if not, exit.
if [ ! -f "$deploy_dir/requirements.txt" ]; then
    echo "requirements.txt does not exist in $deploy_dir."
    exit 1
else
    # Debugging: Output the content of requirements.txt
    echo "Content of requirements.txt:"
    cat requirements.txt
fi

# Install Python packages.
sudo pip3 install -r requirements.txt
