#!/bin/bash

#Photon laser tag install script
#Script will install python and other needed items to run the game

echo "Starting installation"

# Update package lists
echo "Updating package lists"
sudo apt-get update

# Install Python3 and pip
echo "Installing Python3, pip and postgreSQL driver"
sudo apt-get install -y python3 python3-pip python3-psycopg2

# Install pygame for GUI
echo "Installing pygame for GUI"
pip3 install pygame --break-system-packages

echo ""
echo "Installation complete!"
echo ""
echo "To run the project:"
echo "python3 main.py"


