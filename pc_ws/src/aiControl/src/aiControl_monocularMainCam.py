#!/usr/bin/env python 

__author__='boukbab mhamed'
__vesrion="1.0"
__licence="BSD"
import numpy as np
import rospy
import cv2
import os
import time,sys
import threading
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
    model = load_model('model/my_model.model')
graph = tf.get_default_graph()
############################################################################################################
img_proc=np.zeros([480,640,3],dtype=np.uint8)
sign_count=0
state="init..."
stop_thread=False
tick=0
flag=0
class NNcontrol(object):
    def __init__(self):
        self.steer_bot=Steerbot()
    def predicting(self,img_prid):  
        global graph,tick,flag
        img_prid= cv2.resize(img_prid , None, fx=0.5, fy=0.5)
        img_prid=cv2.cvtColor(img_prid ,cv2.COLOR_BGR2GRAY)
        
        with graph.as_default():
            height,width =img_prid.shape
            img_prid = img_prid[int(height/2):height, :]
            img_prid = img_prid.reshape(1, int(height/2) * width).astype(np.float32)
            img_prid=img_prid/255.
            img_prid=img_prid.reshape(120,320,1) 
            self.steer_bot.Updatingvalue(flag,tick)
            self.steer_bot.controlingbot(model.predict(np.expand_dims(img_prid, axis=0))[0])
class Steerbot(object):
    def __init__(self):
        self.flag_sign=0
        self.start_stoping=0
        self.class_names=["right","left","forward","backward"]
        rospy.init_node('velocity_command')
        self.pub=rospy.Publisher('/topic_value',velo,queue_size=1)
        self.msgValue=velo()   
    def Updatingvalue(self, flag,t1):
        self.flag_sign=flag
        self.start_stoping=t1
    def controlingbot(self,data):
        global state,flag,tick
        if (self.flag_sign==0):
            if data.argmax(-1)==0:
                state=self.class_names[0]
                self.msgValue.L=5
                self.msgValue.R=50
                self.pub.publish(self.msgValue)
                # 1-- 0.6
            elif data.argmax(-1)==1:
                state=self.class_names[1]
                self.msgValue.L=50
                self.msgValue.R=5
                self.pub.publish(self.msgValue)
            elif data.argmax(-1)==2:
                state=self.class_names[2]
                self.msgValue.L=35
                self.msgValue.R=35
                self.pub.publish(self.msgValue)
        elif(self.flag_sign==1):
            
            tickon= (cv2.getTickCount()- self.start_stoping)/cv2.getTickFrequency()
            print tickon
	    if (tickon<1):
		print "time before stoping"
		self.msgValue.L=35
                self.msgValue.R=35
                self.pub.publish(self.msgValue)
	    
            elif (tickon>5):
               flag,tick=0,0
	    else:
		   state="stoping"
         	   self.stop_car()
        
    def stop_car(self):
        self.msgValue.L=0
        self.msgValue.R=0
        self.pub.publish(self.msgValue)
class Imagebridge(object):
    def __init__(self):
        self.font=cv2.FONT_HERSHEY_SIMPLEX
        self.t1 = time.clock()
        self.nn_control=NNcontrol()
	
    def img_bridge(self,msg):
        global img_proc,state, stop_thread
        try:
            np_arr = np.fromstring(msg.data, np.uint8)
            image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            # convert sensor_msgs/Image to OpenCV Image
            orig = cv2.flip(image_np,-1)
            cv2.putText(orig,str(state),(20, 40), self.font, 1,(0,255,0),1,cv2.LINE_AA)
            cv2.putText(orig,"time:%.1f"%(time.clock()-self.t1),(20, 80), self.font, 1,(200,0,200),1,cv2.LINE_AA)
            cv2.imshow('image', orig)
            #
            img_proc = orig
            self.nn_control.predicting(img_proc)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_thread=True
                return 
        except Exception as err:
            print (err)
class Traficsign_detection(object):
    def __init__(self,img_sign):
        self.img_sign=img_sign
        
    def obj_detect(self,Cascade,recvalue,sf):
        #crop_img = img[y:y+h, x:x+w]
        global sign_count,flag,tick
        self.img_sign=cv2.cvtColor(self.img_sign, cv2.COLOR_BGR2GRAY)
        height,width=self.img_sign.shape
        self.img_sign=self.img_sign[:int(height/2), 330:]
        sign = Cascade.detectMultiScale(self.img_sign,scaleFactor=sf,minNeighbors=1)
        for (x, y, w, h) in sign:
		print w*h
                if (w*h==recvalue):
		    pass
                    #return True
	        else:
		    return False
                    
        
       
 
    
def fthread():
    
    try:
        image_processing=Imagebridge()
        trafic_sign_detection= threading.Thread(target=sthread)  
        
        rospy.Subscriber("/image/compressed", CompressedImage, image_processing.img_bridge,queue_size = 3)
        trafic_sign_detection.start() 
        print "starting second thread"
        while not rospy.is_shutdown():
            rospy.spin()               
    except Exception as err:
            print (err)
    
def sthread():
    global sign_count,img_proc,stop_thread,flag,tick
    while stop_thread==False:
        stop_cascade = cv2.CascadeClassifier('parking.xml')
        prking_cascade=cv2.CascadeClassifier('stop_sign.xml')
        #traficlight_cascade=cv2.CascadeClassifier('traficlight.xml')
        detect_sign=Traficsign_detection(img_proc)
	
        
        if (sign_count==0):
                if(detect_sign.obj_detect(stop_cascade,4761,1.6)):
			flag,tick= 1,cv2.getTickCount()
                        sign_count+=1
        elif(sign_count==1):
                if(detect_sign.obj_detect(prking_cascade,24649,1.6)):
			flag,tick= 1,cv2.getTickCount()
                        sign_count+=1
        elif(sign_count==2):
            pass
    return        
    
   
if __name__ == '__main__':
    print ("sending command...")
    fthread()
    print (" terminated")
    sys.exit(0)                
  # sthread()
     
     
   
    




