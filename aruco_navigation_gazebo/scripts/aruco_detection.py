#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from cv2 import aruco
import math
import imutils
from custom_message.msg import ArucoVals

class ArucoDetector(Node):
    def __init__(self):
        super().__init__('aruco_detector')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        self.publisher_ = self.create_publisher(ArucoVals, 'aruco_data', 10)
        self.bridge = CvBridge()
        self.center = None
        self.markerID1 = None
        self.radius1 = None
        self.T = 0
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
        self.arucoParams = cv2.aruco.DetectorParameters()

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        det_result = self.aruco_detection(image)
        if det_result is not None:
            aruco_msg = ArucoVals()
            aruco_msg.x = float(det_result[1][0])
            aruco_msg.y = float(det_result[1][1])
            aruco_msg.radius = float(det_result[2]) if det_result[2] is not None else -1.0
            aruco_msg.id = int(det_result[3]) if det_result[3] is not None else -1
            self.publisher_.publish(aruco_msg)
        cv2.imshow("Aruco Detection", det_result[0])
        cv2.waitKey(1)

    def aruco_detection(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = imutils.resize(image, width=1000)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(image, self.arucoDict, parameters=self.arucoParams)

        if len(corners) > 0:
            ids = ids.flatten()
            for (markerCorner, markerID) in zip(corners, ids):
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))

                radius = int(math.sqrt(
                    (int(topRight[0]) - int(bottomLeft[0])) ** 2 + (int(topRight[1]) - int(bottomLeft[1])) ** 2) / 2)
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(image, (cX, cY), radius, (255, 255, 0), 3)

                cv2.putText(image, "Aruco Marker ID = " + str(markerID),
                            (topLeft[0] + 13, topLeft[1] - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 2)

                self.center = (((topLeft[0] + bottomRight[0]) / 2.0), ((topLeft[1] + bottomRight[1]) / 2.0))
                self.markerID1 = markerID
                self.radius1 = radius

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            exit()

        return [image, self.center, self.radius1, self.markerID1, image]

def main(args=None):
    rclpy.init(args=args)
    aruco_detector = ArucoDetector()
    rclpy.spin(aruco_detector)
    aruco_detector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
