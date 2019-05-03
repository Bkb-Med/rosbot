#!/usr/bin/env python 

__author="boukbab mhamed"
__vesrion="1.0"
__licence="BSD"
import numpy as np
import rospy
import cv2
import os
import time

from sensor_msgs.msg import CompressedImage
#from sim_ws.msg import velocity
from publish_tuto.msg import velo

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import keras 
from keras.models import load_model
from keras.utils import CustomObjectScope
from keras.initializers import glorot_uniform
from keras import backend as K
import tensorflow as tf
with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
    model = load_model('model/model030419.model')
graph = tf.get_default_graph()


class recognizing_img(object):
    def __init__(self):
        self.class_names=["right","left","forward","backward"]
        self.state="initializing..."
        self.font=cv2.FONT_HERSHEY_SIMPLEX
        self.t1 = time.clock()
        #ros
        rospy.init_node('velocity_command')
        self.pub=rospy.Publisher('/topic_value',velo,queue_size=1)
	self.msgValue=velo()   
    def img_bridge(self,msg):
        try:
            np_arr = np.fromstring(msg.data, np.uint8)
	    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            # convert sensor_msgs/Image to OpenCV Image
            orig = cv2.flip(image_np,-1)
            
            
            #print "orig"+str(orig.shape)
            cv2.putText(orig,str(self.state),(20, 40), self.font, 1,(0,255,0),1,cv2.LINE_AA)
            cv2.putText(orig,"time:%.3f"%(time.clock()-self.t1),(20, 80), self.font, 1,(200,0,200),1,cv2.LINE_AA)
            
            img = cv2.resize( orig , None, fx=0.5, fy=0.5)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	    img=cv2.medianBlur(img,5)
            img=cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,9,5)#
            self.steer(img)
	    self.pub.publish(self.msgValue)
	    cv2.imshow('image', orig)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return
          
        except Exception as err:
            print (err)
    def controlingbot(self,data):
        if data.argmax(-1)==0:#+20
            self.state=self.class_names[0]
            self.msgValue.L=5
            self.msgValue.R=50#50
            # 1-- 0.6
        elif data.argmax(-1)==1:
            self.state=self.class_names[1]
            self.msgValue.L=43#40
            self.msgValue.R=5
        elif data.argmax(-1)==2:
            self.state=self.class_names[2]
            self.msgValue.L=50#50
            self.msgValue.R=50#50
        elif data.argmax(-1)==3:
            self.state=self.class_names[3]
            self.msgValue.L=-30
            self.msgValue.R=-30


    def steer(self,img):  
        global graph
        with graph.as_default():
            height,width =img.shape#
            img = img[int(height/2):height, :]
            img = img.reshape(1, int(height/2) * width).astype(np.float32)
            img=img/255.
            img=img.reshape(120,320,1) 
            self.controlingbot(model.predict(np.expand_dims(img, axis=0))[0])






        
if __name__ == '__main__':
    
    start=recognizing_img()
    print ("sending command...")
    rospy.Subscriber("/image/compressed", CompressedImage, start.img_bridge,queue_size = 3)
    while not rospy.is_shutdown():
        rospy.spin()




