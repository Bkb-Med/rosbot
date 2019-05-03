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
from publish_tuto.msg import velo
from sensor_msgs.msg import CompressedImage
#sim Vrep from sensor_msgs.msg import Image--from cv_bridge import CvBridge
#from sim_ws.msg import velocity
#from std_msgs.msg import Float32
#pygame


class Coll_TrainingData(object):
    def __init__(self,st_tick):
        self.input_size = 120*320
	#vrep 128*256
        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        #paygame
        self.saved_frame = 0
        self.total_frame = 0
        self.frame=0
        self.st_tick=st_tick
        #ros
        rospy.init_node('velocity_command')
        self.pub=rospy.Publisher('/topic_value',velo,queue_size=1)
        self.msgValue=velo()
        self.X = np.empty((0, self.input_size))
        self.y = np.empty((0, 4))

        
    def img_bridge(self,msg):
        try:
            
            np_arr = np.fromstring(msg.data, np.uint8)
            image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            ########=====sim Vrep=== # convert sensor_msgs/Image to OpenCV Image
            # bridge = CvBridge()
            # orig = bridge.imgmsg_to_cv2(msg, "bgr8")
            orig = cv2.flip(image_np,-1)
            
            orig = cv2.resize( orig , None, fx=0.5, fy=0.5)
        #print orig.shape
            img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
            cv2.imshow('image', img)
            self.collecting(img)
            self.pub.publish(self.msgValue)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return
          
        except Exception as err:
            print err

    def collecting(self,img):  
        
        
        height,width =img.shape
        roi = img[int(height/2):height, :]
        temp_array = roi.reshape(1, int(height/2) * width).astype(np.float32)
            
        self.frame += 1
        self.total_frame += 1

        for event in pg.event.get():
                key_input = pg.key.get_pressed()
                if event.type==pg.QUIT:
                     return
                if key_input[pg.K_UP]:
                    print "FORWARD at -1 [0010] "
                    #100
                    #self.publ.publish(-1)
                    #self.pubr.publish(-1)
                    self.msgValue.L=60
                    self.msgValue.R=60
                    self.X = np.vstack((self.X, temp_array))
                    self.y = np.vstack((self.y, self.k[2]))
                    self.saved_frame += 1
                elif key_input[pg.K_DOWN]:
                    print "BACKWARD at 1 [0001]"
                    #-100
                    #self.publ.publish(1)
                    #self.pubr.publish(1)
                    self.msgValue.L=-20
                    self.msgValue.R=-20
                    self.X = np.vstack((self.X, temp_array))
                    self.y = np.vstack((self.y, self.k[3]))
                    self.saved_frame += 1
                elif  key_input[pg.K_RIGHT]:
                    print "RIGHT at -0.7 -1 [1000]"
                    #100-50
                    #self.publ.publish(-0.6)
                    #self.pubr.publish(-1)
                    self.msgValue.R=50
                    self.msgValue.L=5
                    self.X = np.vstack((self.X, temp_array))
                    self.y = np.vstack((self.y, self.k[0]))
                    self.saved_frame += 1
                elif  key_input[pg.K_LEFT]:
                    print "LEFT at -1 -0.7 [0100]"
                    #self.publ.publish(-1)
                    #self.pubr.publish(-0.6)
                    self.msgValue.R=5
                    self.msgValue.L=50
                    self.X = np.vstack((self.X, temp_array))
                    self.y = np.vstack((self.y, self.k[1]))
                    self.saved_frame += 1
                elif  key_input[pg.K_RSHIFT] :
                    print "STOP"
                    #self.publ.publish(0)
                    #self.pubr.publish(0)
                    self.msgValue.L=0
                    self.msgValue.R=0
                    file_name = str(int(time.time()))
                    directory = "data_collected"
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    try:
                        np.savez(directory + '/' + file_name + '.npz', train=self.X, train_labels=self.y)
                    except IOError as e:
                        print(e)
                    end = cv2.getTickCount()
            # calculate streaming duration
                    print("Streaming duration: , %.2fs" % ((end - self.st_tick) / cv2.getTickFrequency()))

                    print(self.X.shape)
                    print(self.y.shape)
                    print("Total frame: ", self.total_frame)
                    print("Saved frame: ", self.saved_frame)
                    print("Dropped frame: ", self.total_frame - self.saved_frame)
	       
       

if __name__ == '__main__':
    pg.init()
    scr=pg.display.set_mode((480,240))
    st_tick=cv2.getTickCount()
    start=Coll_TrainingData(st_tick)
    print "sending command..."
#simulation v-rep /image,Image
    rospy.Subscriber("/image/compressed", CompressedImage, start.img_bridge,queue_size = 3)
    print("Start collecting images...")
    pg.display.update()
    rospy.spin()
   


