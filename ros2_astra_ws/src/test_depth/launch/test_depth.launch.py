import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'test_depth'
    package_dir = get_package_share_directory(package_name)

    return LaunchDescription({

        IncludeLaunchDescription(
            XMLLaunchDescriptionSource(
                os.path.join(get_package_share_directory('astra_camera'), 'launch/astro_pro_plus.launch.xml')
            ),
        ),

        Node(
            package=package_name,
            executable='depth_data',
            emulate_tty=True,
            parameters=[
                {"use_sim_time": True},
                {"is_stamped": True},
            ]
        )
    })