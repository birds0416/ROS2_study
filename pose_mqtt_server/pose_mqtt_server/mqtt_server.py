import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default
from rclpy.qos import qos_profile_services_default

from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Pose, PoseWithCovarianceStamped, PoseWithCovariance
from tf2_ros import transform_listener

import paho.mqtt.client as mqtt
import json

class PoseMQTT(Node):
    def __init__(self):
        super().__init__('PoseMQTT')

        # MQTT settings
        # external broker
        # 2. 계정정보로 접속하는 MQTT
        # - 컨테이너 명 : iv_vision_test_broker
        # - 1883 port 주소 : mqtt://192.168.10.237:55008
        # - 계정 정보 : vision / vision!@123

        self.declare_parameter("~broker_ip_address", '')
        self.declare_parameter("~mqtt_sub_topic", '')
        self.declare_parameter("~mqtt_pub_topic", '')
        self.declare_parameter("~mqtt_username", '')
        self.declare_parameter("~mqtt_password", '')

        self.broker_address = self.get_parameter("~broker_ip_address").get_parameter_value().string_value
        self.MQTT_SUB_TOPIC = self.get_parameter("~mqtt_sub_topic").get_parameter_value().string_value
        self.MQTT_PUB_TOPIC = self.get_parameter("~mqtt_pub_topic").get_parameter_value().string_value
        self.MQTT_USERNAME = self.get_parameter("~mqtt_username").get_parameter_value().string_value
        self.MQTT_PASSWORD = self.get_parameter("~mqtt_password").get_parameter_value().string_value

        
        self.mqttclient = mqtt.Client("ros2mqtt")
        self.mqttclient.on_message = self.on_message
        self.mqttclient.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)

        self.mqttclient.connect(self.broker_address)
        self.mqttclient.subscribe(self.MQTT_SUB_TOPIC)

        self.mqttclient.loop_start()

        # ROS 2 publishers and subscribers
        self.pose_pub = self.create_publisher(PoseStamped, '/pose_from_mqtt', 10)
        self.pose_sub = self.create_subscription(PoseWithCovarianceStamped, 
                                                 '/pose', 
                                                 self.topic2mqtt_callback, 10)
        
        self.current_pose = PoseStamped()

        self.get_logger().info('ROS2 MQTT Broker:: START...')
        self.get_logger().info('ROS2 MQTT Broker:: broker_address = {}'.format(self.broker_address))
        self.get_logger().info('ROS2 MQTT Broker:: MQTT_PUB_TOPIC = {}'.format(self.MQTT_PUB_TOPIC))
        self.get_logger().info('ROS2 MQTT Broker:: MQTT_SUB_TOPIC = {}'.format(self.MQTT_SUB_TOPIC))

    def on_message(self, client, userdata, msg):
        # self.get_logger().info("mqtt message received on topic {}: {}".format(msg.topic, msg.payload.decode("utf-8")))
        msg = str(msg.payload.decode("utf-8"))
        msg_dict = json.loads(msg)

        if msg_dict is not None:
            pose_msg = PoseStamped()
            pose_msg.header.stamp = self.get_clock().now().to_msg()
            pose_msg.header.frame_id = 'robot_pose'

            pose_msg.pose.position.x = float(msg_dict['p_x'])
            pose_msg.pose.position.y = float(msg_dict['p_y'])
            pose_msg.pose.position.z = float(msg_dict['p_z'])

            pose_msg.pose.orientation.x = float(msg_dict['o_x'])
            pose_msg.pose.orientation.y = float(msg_dict['o_y'])
            pose_msg.pose.orientation.z = float(msg_dict['o_z'])
            pose_msg.pose.orientation.w = float(msg_dict['o_w'])

            self.current_pose = pose_msg

            self.pose_pub.publish(pose_msg)
            self.get_logger().info("Pose published to topic {}:\npose_x: {},\npose_y: {},\norie_w: {}".format('/pose_from_mqtt', 
                                                                             pose_msg.pose.position.x,
                                                                             pose_msg.pose.position.y,
                                                                             pose_msg.pose.orientation.w))

    def topic2mqtt_callback(self, data):
        if data != None:
            self.current_pose.pose.position.x = data.pose.pose.position.x
            self.current_pose.pose.position.y = data.pose.pose.position.y
            self.current_pose.pose.position.z = data.pose.pose.position.z

            self.current_pose.pose.orientation.x = data.pose.pose.orientation.x
            self.current_pose.pose.orientation.y = data.pose.pose.orientation.y
            self.current_pose.pose.orientation.z = data.pose.pose.orientation.z
            self.current_pose.pose.orientation.w = data.pose.pose.orientation.w

            Dictionary ={
                'x':str(self.current_pose.pose.position.x),
                'y':str(self.current_pose.pose.position.y),
                'z':str(self.current_pose.pose.position.z)}
            # self.get_logger().info('dict:: {0}'.format(json.dumps(Dictionary).encode()))
            self.mqttclient.publish(self.MQTT_PUB_TOPIC, json.dumps(Dictionary).encode(),qos=0, retain=False)
            self.get_logger().info("Robot Pose MQTT Sent : x = {}".format(self.current_pose.pose.position.x))
            self.get_logger().info("Robot Pose MQTT Sent : y = {}".format(self.current_pose.pose.position.y))
            self.get_logger().info("Robot Pose MQTT Sent : w = {}".format(self.current_pose.pose.orientation.w))

def main(args=None):
    rclpy.init(args=args)
    rpose_subscriber = PoseMQTT()
    rclpy.spin(rpose_subscriber)
    rpose_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()