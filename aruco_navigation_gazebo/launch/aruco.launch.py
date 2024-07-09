import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_mr_robot_desc = get_package_share_directory('mr_robot_description')
    pkg_aruco_nav = get_package_share_directory('aruco_navigation_gazebo')

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