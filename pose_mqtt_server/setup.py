from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'pose_mqtt_server'
share_dir = os.path.join('share', package_name)

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join(share_dir, 'launch'), glob('launch/*.launch.py')),
        (os.path.join(share_dir, 'config'), glob('config/*.yaml'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='cornersdev',
    maintainer_email='cornersdev@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mqtt_server = pose_mqtt_server.mqtt_server:main',
            'robot_navigator = pose_mqtt_server.robot_navigator:main'
        ],
    },
)
