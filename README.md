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

 *1-First thing you to do befor training your data is that you have to gather your images that show your trajectory of your road  so launch python script Collectingdata.py for that purpose which is recording keystrokes (left, right, forward)and images from raspbery pi 3 B+ that is publishing a compressed images because raw images provide too low FPS so for that and after building  all packages launch img_copressed.py
 
*2-Train your data .

*3-To control the robot i used arduino uno and adafruit sheild i just added those things to learn about serial data , you can connect your RPI directly to your controller like L298D ...a second camera is added to detect road signs so launch the steerbot .py on the RPi ..

### Author 
* Boukbab mhamed

for additional information contact at :
```
boukbab.med@gmail.com
```
