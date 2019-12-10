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

 *1-First, you should gather images that show the trajectory of your road  ,after that launch python script Collectingdata.py, to  record keystrokes (left, right, forward)and published images .note that you'll recieve only compressed images because raw images will decrease the FPS .so after building  all packages launch img_copressed.py
 
*2-Train your data .

*3-..a second camera is added to detect road signs so launch the steerbot .py on the RPi ..

### Author 
* Boukbab mhamed

for additional information contact at :
```
boukbab.med@gmail.com
```
