#!/usr/bin/env python3
import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import cv2.aruco as aruco

class Detection(Node):
    def __init__(self):
        super().__init__('Aruco_detection')
        
        self.subscriber_ = self.create_subscription(Image,'/world_image', self.image_callback, 10) #world_image is the topic name I gave in bridge  file
        self.get_logger().info("Detection has been initialized.")
        
        self.bridge = CvBridge() #created an object self bridge and CvBridge is the class
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250) 
        self.parameters = aruco.DetectorParameters_create()

    def image_callback(self, msg):
        self.image = msg
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY) #to convert cv2 image in grayscale for aruco to detect it
        corners, ids, RejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
        print(corners)


        if ids is not None:
            cv_image = aruco.drawDetectedMarkers(cv_image, corners, ids)
            self.get_logger().info(f"Detected Aruco markers with IDs: {ids.flatten()}")
    
        for corner in corners:
            # center and radius of the marker
            corner = corner.reshape((4, 2))
            (top_left, top_right, bottom_right, bottom_left) = corner
            center_x = int((top_left[0] + bottom_right[0]) / 2.0)
            center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                
            # radius as half the diagonal of the bounding box
            width = math.sqrt((top_right[0] - top_left[0]) ** 2 + (top_right[1] - top_left[1]) ** 2)
            height = math.sqrt((bottom_left[0] - top_left[0]) ** 2 + (bottom_left[1] - top_left[1]) ** 2)
            radius = int(math.sqrt(width ** 2 + height ** 2) / 2.0)

            # sphere around the marker
            cv2.circle(cv_image, (center_x, center_y), radius, (0, 255, 0), 2)
            self.get_logger().info(f"Marker ID: {ids.flatten()[0]}, Center: ({center_x}, {center_y}), Radius: {radius}")
       
        cv2.imshow("kitty",cv_image) #for showing it on window
        cv2.waitKey(1)
   
        
def main(args=None):#We don't provide any argument to the script
    rclpy.init(args=args)  
    node = Detection()
    rclpy.spin(node)
    rclpy.shutdown() 
    print("c")
    exit()

if __name__ == '__main__':
    main()     