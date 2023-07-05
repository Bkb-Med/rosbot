# rosbot:

Self driving rc car using ROS ,CNN { keras and tensorflow as backend} , Rpi3 B+ and arduino UNO.

![](Screenshot%20from%202019-05-03%2015-45-01.png)

### Prerequisites
```
Ubuntu 16.04-
Ros kinetic
tensorflow 1.12.0
keras 2.2.4
openCV 3.3.1-dev "you should build opencv from source if you want to train your haarcascade xml "
pygame 1.9.4
numpy 1.15.4
```
simulation :
```
Vrep 3.5
```
## Getting Started

*1-To gather the streaming images that show the trajectory of the road, you should run the Python script called 'Collectingdata.py' and use the following keystrokes (left, right, forward) for the purpose of data annotations. This script will save and compress all the published images from the main camera, along with the annotations, into a 7zip archive. The collected data should then be trained on a PC with a high-performance GPU. We have chosen to train our data in Google Colab. Please note that we will receive only compressed images because using raw images would decrease the frames per second (FPS) since we are using RPI B+. In future projects, we intend to use the NVidia Nano. After building all the required packages (C++ files), you can launch 'img_compressed.py'."
 
*2-Train the data .

*3-..a second camera is added to detect the road signs so launch the steerbot.py on the RPi ..

### Author 
* Boukbab mhamed

for additional information contact at :
```
boukbab.med@gmail.com
```
