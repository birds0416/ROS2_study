from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    package_name = 'unity_slam_example'
    package_dir = get_package_share_directory(package_name)

    config = os.path.join(
        package_dir,
        'config',
        'params.yaml'
    )

    return LaunchDescription([
        Node(
            package="ros2_tf2_receive",
            executable="tf2_receive",
            emulate_tty=True,
            parameters=[
                {"use_sim_time": True},
                {"is_stamped": True},
                config
            ]
        )
    ])