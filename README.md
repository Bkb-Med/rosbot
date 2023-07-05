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

 *1-The streaming images that show the trajectory of the road should be gathered, after that launch python script Collectingdata.py, and record keystrokes  (left, right, forward) "annotations along with the images" this will save and compress alltogether the published images from the main cam into 7zip archive. thus this collected should be trained in pc with (high performance GPU) we choosed to train our data in google collab, please note that w'll recieve only compressed images because raw images will decrease the FPS since we use RPI B+, we intend to use NVIdia nano in the future projects. so after building all the packages (C++ files) launch img_copressed.py
 
*2-Train the data .

*3-..a second camera is added to detect road signs so launch the steerbot.py on the RPi ..

### Author 
* Boukbab mhamed

for additional information contact at :
```
boukbab.med@gmail.com
```
