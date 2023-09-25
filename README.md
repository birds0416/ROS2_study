# ROS2_study
ROS2를 공부하면서 만들어본 테스트 프로그램 저장소

## ros2_tf2_receive
Study to subscribe pose topic from slam_example.

Also implemented mqtt connection with mqtt broker in windows.

## pose_mqtt_server
Modification version from ros2_tf2_receive

ros2_tf2_receive package is just a node that subscribes topic '/pose' from the bt_navigator node.

This pose_mqtt_sever connects to a mqtt broker, its parameters can be changed from **config/params.yaml**.

After changing mqtt broker info in params.yaml, the workspace needs to be **colcon build** again.

**robot_navigator node 출처:** https://github.com/SteveMacenski/nav2_rosdevday_2021/tree/main/nav2_rosdevday_2021

#### The process of pose_mqtt_server is like the following:

MQTT Publisher -> MQTT Broker (wherever it is) -> MQTT Subscriber(ROS Node - PoseMQTT)

-> Convert to ROS2 msg (PoseStamped, PoseWithCovarianceStamped, etc..)

-> Publish the msg as topic **"/pose_from_mqtt"** -> robot_navigator Node subscribes this topic

-> robot_navigator Node apply the msg to robot's pose and also subscribes **"/pose"** topic to get the real-time robot pose.

-> PoseMQTT Node subscribes **"/pose"** topic and converts this to mqtt msg to send it back to the mqtt broker.

-> Eventually, changed robot's pose sent to mqtt broker updates the robot's pose in Unity 3D dimensional space.
