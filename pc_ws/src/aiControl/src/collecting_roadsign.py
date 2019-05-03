#!/usr/bin/env python 

__author="boukbab mhamed"
__vesrion="1.0"
__licence="BSD"
import pygame as pg
import rospy
import time
import cv2
import numpy as np
import os

from sensor_msgs.msg import CompressedImage
#sim Vrep from sensor_msgs.msg import Image--from cv_bridge import CvBridge
#from sim_ws.msg import velocity
#from std_msgs.msg import Float32
#pygame


class Coll_TrainingData(object):
    def __init__(self):
        
        self.frame=0
        
        rospy.init_node('velocity_command')
       
        
    def img_bridge(self,msg):
        try:
            
	    np_arr = np.fromstring(msg.data, np.uint8)
	    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

           ########=====sim Vrep=== # convert sensor_msgs/Image to OpenCV Image
           # bridge = CvBridge()
           # orig = bridge.imgmsg_to_cv2(msg, "bgr8")
            orig = cv2.flip(image_np,-1)
            
            
	    cv2.imshow('image', orig)
            self.collecting(orig)
	
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return
          
        except Exception as err:
            print err

    def collecting(self,img):  
        
        
        
        self.frame += 1
       

        for event in pg.event.get():
                key_input = pg.key.get_pressed()
                if event.type==pg.QUIT:
                     return
                
                elif  key_input[pg.K_RSHIFT] :
                    print "tik"
                    self.frame += 1
		    print  "frame numbre :: " + str(self.frame)
                    
                    directory = "roadsign_collected"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    try:
                        cv2.imwrite(directory+'/'+'sign_00'+str(self.frame)+'.jpg',img)
                    except IOError as e:
                        print(e)
                   
           
	       
       

if __name__ == '__main__':
    pg.init()
    scr=pg.display.set_mode((480,240))
    
    start=Coll_TrainingData()
    print "sending command..."
#simulation v-rep /image,Image
    rospy.Subscriber("/image/compressed", CompressedImage, start.img_bridge,queue_size = 3)
    print("Start collecting images...")
    pg.display.update()
    rospy.spin()
   


