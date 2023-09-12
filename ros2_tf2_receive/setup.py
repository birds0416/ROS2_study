import os
from setuptools import find_packages, setup
from glob import glob

package_name = 'ros2_tf2_receive'
share_dir = os.path.join('share', package_name)

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join(share_dir, 'launch'), glob('launch/*.launch.py'))
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
            'tf2_receive = ros2_tf2_receive.tf2_receive:main'
        ],
    },
)
