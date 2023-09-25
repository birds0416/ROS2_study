from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    package_name = 'pose_mqtt_server'
    package_dir = get_package_share_directory(package_name)

    return LaunchDescription([
        Node(
            package=package_name,
            executable="robot_navigator",
            emulate_tty=True,
            parameters=[
                {"use_sim_time": True},
                {"is_stamped": True}
            ]
        )
    ])