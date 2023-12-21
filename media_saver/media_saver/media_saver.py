import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image

from cv_bridge import CvBridge
import cv2

class MediaSaver(Node):
    def __init__(self):
        super().__init__('MediaSaver')

        self.sub_img_saver = self.create_subscription(Image, 'save_img', self.img_callback, 10)
        self.sub_img_empty_saver = self.create_subscription(Image, 'save_img_empty', self.img_empty_callback, 10)

    def img_callback(self, msg):
        bridge = CvBridge()
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        stamp = msg.header.stamp.sec
        self.get_logger().info("stamp: {}".format(msg.header.stamp))

        # cv2.imwrite('./evt_imgs/event_img_{}.jpg'.format(stamp), cv_img)
        # self.get_logger().info("Event Image {} Save SUCCESS".format('event_img_{}.jpg'.format(stamp)))

    def img_empty_callback(self, msg):
        bridge = CvBridge()
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        stamp = msg.header.stamp.sec
        self.get_logger().info("stamp: {}".format(msg.header.stamp))

        # cv2.imwrite('./evt_imgs/event_img_empty_{}.jpg'.format(stamp), cv_img)
        # self.get_logger().info("Event Image {} Save SUCCESS".format('event_img_empty_{}.jpg'.format(stamp)))

def main(args=None):
    rclpy.init(args=args)
    mediasave = MediaSaver()
    rclpy.spin(mediasave)
    mediasave.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()