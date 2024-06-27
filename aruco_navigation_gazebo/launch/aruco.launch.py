from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([
        # Node(
        #     package='ros2_pkg',
        #     namespace='cpp',
        #     executable='ros2_pkg_hello_publisher',
        #     name='ros2_pkg_hello_publisher_node',
        #     output='screen',
        # ),
        Node(
            package='launch',
            namespace='sdf',
            executable='world.sdf',
            name='world _node'
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_node',
            output='screen')
        # ),
        # Node(
        #     package='ros2_pkg',
        #     namespace='py',
        #     executable='hello_subscriber_node.py',
        #     name='ros2_pkg_hello_subscriber_node',
        #     output='screen',
        # ),
        # Node(
        #     package='ros2_pkg',
        #     executable='ros2_pkg_server',
        #     name='ros2_pkg_server',
        #     output='screen',
        # )        
    ])