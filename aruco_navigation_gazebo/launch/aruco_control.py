import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Detection node
    aruco_detector = Node(
        package='aruco_navigation_gazebo',
        executable='aruco_detection.py',
        name='aruco_detection',
        output='screen'
    )

    # Move straight (controller) node
    move_straight = Node(
        package='aruco_navigation_gazebo',
        executable='move_straight.py',
        output='screen'
    )

    return LaunchDescription([
        aruco_detector,
        move_straight
    ])
