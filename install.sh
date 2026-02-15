#!/bin/bash

#Photon laser tag install script
#Script will install java and java sql driver and other needed items to run the game

echo "Starting installation"

echo "Updating package lists" 
sudo apt-get update

echo "Installing Java JDK"
sudo apt-get install -y default-jdk

echo "Creating lib directory"
mkdir -p lib

echo "Downloading PostgreSQL Java driver"
curl -o lib/postgresql-42.7.1.jar https://jdbc.postgresql.org/download/postgresql-42.7.1.jar


echo "Installation complete!"
echo ""
echo "To compile the project, run:"
echo "  javac -cp \".:lib/*\" *.java"
echo ""
echo "To run the project, run:"
echo "  java -cp \".:lib/*\" LaserTagMain"
