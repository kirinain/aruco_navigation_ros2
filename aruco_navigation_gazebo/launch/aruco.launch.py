import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    #Changes in the navigation of  robot
    mr_robot = Node(package='aruco_navigation_gazebo',
				executable='aruco_navigation.py',
				name='mr_robot',
			    output='screen',
    )

    #For detection of aruco marker
    aruco_detect = Node(package='aruco_navigation_gazebo',
				executable='aruco_detection.py',
				name='mr_robot',
			    output='screen',
    )
    
    return LaunchDescription([
        mr_robot,
        aruco_detect
        ])