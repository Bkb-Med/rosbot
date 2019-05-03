
__author="boukbab mhamed"
__vesrion="1.0"
__licence="BSD"


# Python libs
import sys, time

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2

# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage



video_capture = cv2.VideoCapture(0)
video_capture.set(3,640)

video_capture.set(4,480)


class image_feature:

    def __init__(self):
       
        # topic where we publish
        self.image_pub = rospy.Publisher("/image/compressed",
            CompressedImage,queue_size = 3)
       

    def callback(self, img):
       

     
       #image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
        image_np = cv2.imdecode(img, cv2.IMREAD_COLOR) # OpenCV >= 3.0:
        
       

        #### Create CompressedIamge ####
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
        # Publish new image
        self.image_pub.publish(msg)
        
       
def main(args):
    '''Initializes and cleanup ros node'''
    ic = image_feature()
    rospy.init_node('compressed_Image', anonymous=True)
    while not rospy.is_shutdown():
	ret,frame=video_capture.read()
    	image_feature.callback(frame)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image compressed"
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
