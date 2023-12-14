import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2

class DepthData(Node):
    def __init__(self):
        super().__init__('DepthData')

        self.sub_depth_dat = self.create_subscription(PointCloud2, '/camera/depth/points', self.depth_callback, 10)
        self.depth_points = PointCloud2()

    def depth_callback(self, data):
        if data != None:
            self.depth_points.header = data.header
            self.depth_points.height = data.height
            self.depth_points.width = data.width
            self.depth_points.header.stamp.sec = data.header.stamp.sec
            # self.get_logger().info("Sec: {}".format(self.depth_points.header.stamp.sec))

            self.depth_points.data = data.data
            # self.get_logger().info("Depth Points are {}".format(self.depth_points.data))
            i = 1
            points = []
            temp = []
            for num in self.depth_points.data:
                if i > 3:
                    points.append(temp)
                    temp = []
                    i = 1
                temp.append(num)
                i += 1
            self.get_logger().info("Depth Points are {}".format(p for p in points ))

            # for d in points:
            #     self.get_logger().info("Depth Points are {}".format(d))

def main(args=None):
    rclpy.init(args=args)
    depth_sub = DepthData()
    rclpy.spin(depth_sub)
    depth_sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()