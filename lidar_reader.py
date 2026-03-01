import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np

class LidarReader(Node):
    def __init__(self):
        super().__init__('lidar_reader')
        self.sub = self.create_subscription(LaserScan, '/scan', self.callback, 10)

    def callback(self, msg):
        ranges = np.array(msg.ranges)
        valid = ranges[np.isfinite(ranges) & (ranges > msg.range_min)]

        if len(valid) > 0:
            self.get_logger().info(
                f"Min dist: {valid.min():.2f}m | "
                f"Max dist: {valid.max():.2f}m | "
                f"Front: {ranges[0]:.2f}m | "
                f"Left: {ranges[90]:.2f}m | "
                f"Right: {ranges[270]:.2f}m"
            )

def main():
    rclpy.init()
    node = LidarReader()
    rclpy.spin(node)

if __name__ == '__main__':
    main()