from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'test_depth'
share_dir = os.path.join('share', package_name)

package_name = 'test_depth'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
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
            "depth_data = test_depth.depth_data:main"
        ],
    },
)
