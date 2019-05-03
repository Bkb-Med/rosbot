#! /usr/bin/env python 

__author="boukbab mhamed"
__vesrion="1.0"
__licence="BSD"
import pygame as pg
import rospy

from publish_tuto.msg import velo

#pygame
blue = (0,0,255)
green = (0,255,0)
pink = (255,200,200)
pleft=0
pright=0
pg.init()
screen = pg.display.set_mode((480,240))
screen.fill(pink)
myfont = pg.font.SysFont("monospace", 80)
font = pg.font.SysFont("monospace", 20)
text=""
#ros
rospy.init_node('publish_topic')
pub=rospy.Publisher('/topic_value',velo,queue_size=1)
rate=rospy.Rate(100)
msgValue=velo()



def evento():
    global text,pleft,pright
    for event in pg.event.get():
        if event.type==pg.QUIT:
           return
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                text="FORWARD"
                pleft=100
                pright=100
                screen.fill(pink)
            elif event.key == pg.K_DOWN:
                text="BACKWARD"
                pleft=-100
                pright=-100
                screen.fill(pink)
            elif event.key == pg.K_RIGHT:
                text="RIGHT"
                pleft=100
                pright=20
                screen.fill(pink)
            elif event.key == pg.K_LEFT:
                text="LEFT"
                pleft=20
                pright=100
                screen.fill(pink)
            elif event.key == pg.K_RSHIFT :
                text="STOP"
                pleft=0
                pright=0
                screen.fill(pink) 
    label = myfont.render(text, 1, blue)
    lblvalue=font.render("Left :: "+str(pleft)+" Right :: "+ str(pright), 2, blue)
    screen.blit(lblvalue, (20, 100))
    screen.blit(label, (20, 20))
    pg.display.update()
    #msg
    msgValue.L=pleft
    msgValue.R=pright







print "sending command.."
while not rospy.is_shutdown():
   
    evento()
    pub.publish(msgValue)
    rate.sleep()
