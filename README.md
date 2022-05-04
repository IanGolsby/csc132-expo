# Gas Sensor Array

### Sensory Module for Enhancement of Life and Livelihood (SMELL)

## Description: CSC132 Project -- wearable sensor array for detecting hazardous gasses

## Team name: Team Name

### Group Members:
- Ian Golsby
- Lael Hamilton

Requirements: Flask, Raspberry Pi, Various Sensors, and some other computer

The codebase is seperated into two main directories:
  RPi_Side and Server_HQ
  

RPi_Side contains the files for a local flask server, sensor testing, a socket client, and files used to run these processess.
Server_HQ contains the files for a local flask server, a socket server, and the files used to launch said servers.

  -Server_HQ's purpose is to be able to keep track of the gas detecting Raspberry Pi
  
  
#### How to start on Pi
1.) From the RPi_Side directory, run the "runMain.py" file
  -runMain.py starts the local flask server and, in a different thread, runs the sensor_testing.py file
  -Everything should automatically start
  
### How to Start on HQ server
1.) From the Server_HQ directory, run the "runMain.py" file
  -runMain.py starts the local flask server and, in a different thread, runs the startSocket.py file
  -Everything should automatically start

--Note: Make sure to keep files in the same directories as found on the github repo 
