#! /usr/bin/env python 

__author="boukbab mhamed"
__vesrion="1.0"
__licence="BSD"
from __future__ import print_function, division, absolute_import

import time

import rospy
from publish_tuto.msg import velo


from robust_serial import write_order, Order, write_i8, write_i16, read_i8, read_order
from robust_serial.utils import open_serial_port


prev_datal=0
prev_datar=0

def callback(data):
        #Callback function of subscribed topic. 

    global prev_datal,prev_datar
    # Equivalent to write_i8(serial_file, Order.MOTOR.value)
    


    if data.L != prev_datal or data.R != prev_datar :
        write_order(serial_file, Order.MOTOR1)
        write_i8(serial_file,  int(data.L) )
        write_order(serial_file, Order.MOTOR2)
        write_i8(serial_file,  int(data.R) )  	
        prev_datal=data.L
        prev_datar=data.R




if __name__ == '__main__':
    try:
        serial_file = open_serial_port(baudrate=115200, timeout=None)
    except Exception as e:
        raise e
    rospy.init_node('cmd_Motor', anonymous=True)
    is_connected = False
    # Initialize communication with Arduino
    while not is_connected:
        print("Waiting for arduino...")
        write_order(serial_file, Order.HELLO)
        bytes_array = bytearray(serial_file.read(1))
        if not bytes_array:
            time.sleep(2)
            continue
        byte = bytes_array[0]
        if byte in [Order.HELLO.value, Order.ALREADY_CONNECTED.value]:
            is_connected = True

    print("Connected to Arduino")


    subscriber = rospy.Subscriber("topic_value",
           velo , callback,  queue_size = 3)

    print ("Sending data motor...")
    
        
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shutting down ROS cmd ")
        
   
        
