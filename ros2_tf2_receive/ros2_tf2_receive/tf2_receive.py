import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped, Pose, PoseWithCovarianceStamped, PoseWithCovariance
from tf2_ros import transform_listener

import paho.mqtt.client as mqtt
import json

class RobotPose_sub(Node):
    def __init__(self):
        super().__init__('RobotPose_sub')

        self.node_name = 'RobotPose_subscriber'

        # Pose subscribe settings
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/pose',
            self.pose_callback,
            10
        )
        self.subscription

        self.pose = PoseStamped()
        
        # mqtt settings
        self.sleep_rate = 0.025
        self.rate = 10
        self.r = self.create_rate(self.rate)
        self.broker_address= self.declare_parameter("~broker_ip_address", '192.168.10.212').value
        self.MQTT_PUB_TOPIC = self.declare_parameter("~mqtt_pub_topic", 'window/cmd_vel').value
        self.mqttclient = mqtt.Client("ros2mqtt") 
        self.mqttclient.connect(self.broker_address) 
    
    def pose_callback(self, data):

        self.pose.pose.position.x = data.pose.pose.position.x
        self.pose.pose.position.y = data.pose.pose.position.y
        self.pose.pose.position.z = data.pose.pose.position.z

        self.pose.pose.orientation.x = data.pose.pose.orientation.x
        self.pose.pose.orientation.y = data.pose.pose.orientation.y
        self.pose.pose.orientation.z = data.pose.pose.orientation.z
        self.pose.pose.orientation.w = data.pose.pose.orientation.w

        self.get_logger().info("Robot Pose Position x = {}".format(self.pose.pose.position.x))
        self.get_logger().info("Robot Pose Position y = {}".format(self.pose.pose.position.y))
        self.get_logger().info("Robot Pose Position z = {}".format(self.pose.pose.position.z))
        
        self.get_logger().info("Robot Pose Orientation x = {}".format(self.pose.pose.orientation.x))
        self.get_logger().info("Robot Pose Orientation y = {}".format(self.pose.pose.orientation.y))
        self.get_logger().info("Robot Pose Orientation z = {}".format(self.pose.pose.orientation.z))
        self.get_logger().info("Robot Pose Orientation w = {}".format(self.pose.pose.orientation.w))

        if data != None:
            Dictionary ={
                'x':str(self.pose.pose.position.x),
                'y':str(self.pose.pose.position.y),
                'z':str(self.pose.pose.position.z)}
            self.get_logger().info('dict:: {0}'.format(json.dumps(Dictionary).encode()))
            self.mqttclient.publish(self.MQTT_PUB_TOPIC, json.dumps(Dictionary).encode(),qos=0, retain=False)

def main(args=None):
    rclpy.init(args=None)
    rpose_subscriber = RobotPose_sub()
    rclpy.spin(rpose_subscriber)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


# class RelayRos2Mqtt(Node):
#     def __init__(self):
#         super().__init__('relay_ros2_mqtt')
        
#         self.sleep_rate = 0.025
#         self.rate = 10
#         self.r = self.create_rate(self.rate)
#         self.broker_address= self.declare_parameter("~broker_ip_address", '192.168.10.212').value
#         self.MQTT_PUB_TOPIC = self.declare_parameter("~mqtt_pub_topic", 'window/cmd_vel').value
#         self.ROS_TWIST_SUB_TOPIC = self.declare_parameter("~twist_sub_topic", 'test/MQTT').value
#         self.mqttclient = mqtt.Client("ros2mqtt") 
#         self.mqttclient.connect(self.broker_address) 
#         self.mqttclient.subscribe(self.ROS_TWIST_SUB_TOPIC)

#         self.get_logger().info('relay_ros2_mqtt:: started...')
#         self.get_logger().info(f'relay_ros2_mqtt:: broker_address = {self.broker_address}')
#         # self.get_logger().info(f'relay_ros2_mqtt:: MQTT_PUB_TOPIC = {self.MQTT_PUB_TOPIC}')
#         self.get_logger().info(f'relay_ros2_mqtt:: ROS_TWIST_SUB_TOPIC = {self.ROS_TWIST_SUB_TOPIC}')

#         self.mqttclient.on_message = self.on_message

#         # self.create_subscription(
#         #     Twist,
#         #     self.ROS_TWIST_SUB_TOPIC,
#         #     # self.publish_to_mqtt,
#         #     self.subscribe_and_print,
#         #     qos_profile=qos_profile_system_default)
        
#     def publish_to_mqtt(self, tmsg):
#         pass
#         # if tmsg.linear.x != 0 or tmsg.angular.z:
#         #     Dictionary ={'x':str(tmsg.linear.x), 'z':str(tmsg.angular.z)}
#         #     self.get_logger().info('dict:: {0}'.format(json.dumps(Dictionary).encode()))
            
#         #     self.mqttclient.publish(self.MQTT_PUB_TOPIC,json.dumps(Dictionary).encode(),qos=0, retain=False)

#     def on_message(self, client, userdata, message):
#         # print("message received ", str(message.payload.decode("utf-8")))
#         # print("message topic = ", message.topic)
#         # print("message qos = ", message.qos)
#         # print("message retain  flag = ", message.retain)
#         # print()

#         self.get_logger().info(f'relay_ros2_mqtt:: message received = {str(message.payload.decode("utf-8"))}')


# def main(args=None):
#     rclpy.init(args=args)
#     try:
#         relay_ros2_mqtt = RelayRos2Mqtt()
#         rclpy.spin(relay_ros2_mqtt)
#     except rclpy.exceptions.ROSInterruptException:
#         pass

#     relay_ros2_mqtt.destroy_node()
#     rclpy.shutdown()