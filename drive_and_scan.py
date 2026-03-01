import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import numpy as np
import csv
import os
from datetime import datetime
import math

class FourWheelScanner(Node):
    def __init__(self):
        super().__init__('four_wheel_scanner')

        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)

        # Robot state
        self.robot_x   = 0.0
        self.robot_y   = 0.0
        self.robot_yaw = 0.0
        self.latest_scan = None

        # CSV setup
        self.csv_file = os.path.expanduser(
            '~/diff_robot_ws/lidar_data.csv')
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'room',
                'robot_x', 'robot_y', 'heading_deg',
                'front_m', 'front_left_m', 'front_right_m',
                'left_m', 'right_m',
                'back_m',
                'closest_dist_m', 'closest_angle_deg',
                'zone'
            ])

        self.scan_count = 0
        self.get_logger().info(
            '\n'
            '╔══════════════════════════════════════╗\n'
            '║   4-WHEEL ROBOT  LIDAR SCANNER       ║\n'
            '║   Drive with teleop to collect data  ║\n'
            '║   Data saved to: lidar_data.csv      ║\n'
            '╚══════════════════════════════════════╝'
        )

    def odom_callback(self, msg):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y**2 + q.z**2)
        self.robot_yaw = math.atan2(siny, cosy)

    def get_room(self, x, y):
        if   x < 0 and y < 0:  return 1
        elif x >= 0 and y < 0: return 2
        elif x < 0 and y >= 0: return 3
        else:                   return 4

    def get_zone(self, dist):
        if dist < 0.5:   return 'DANGER'
        elif dist < 1.0: return 'CAUTION'
        else:            return 'SAFE'

    def scan_callback(self, msg):
        ranges = np.array(msg.ranges)
        ranges = np.where(np.isfinite(ranges), ranges, msg.range_max)

        # ── Directional readings ──────────────────────────────────
        front       = float(np.min(ranges[0:15]))
        front_left  = float(ranges[45])
        front_right = float(ranges[315])
        left        = float(ranges[90])
        back        = float(ranges[180])
        right       = float(ranges[270])
        closest     = float(ranges.min())
        closest_ang = int(np.argmin(ranges))

        room    = self.get_room(self.robot_x, self.robot_y)
        zone    = self.get_zone(closest)
        heading = round(math.degrees(self.robot_yaw), 1)

        self.scan_count += 1

        ROOM_NAMES = {
            1: 'Room1-RED', 2: 'Room2-GREEN',
            3: 'Room3-BLUE', 4: 'Room4-YELLOW'
        }
        ZONE_ICON = {
            'DANGER': '🔴', 'CAUTION': '🟡', 'SAFE': '🟢'
        }

        # ── Terminal output ───────────────────────────────────────
        self.get_logger().info(
            f'\n'
            f'╔══════════════════════════════════════════════╗\n'
            f'║  SCAN #{self.scan_count:<6}  {ROOM_NAMES[room]:<28}║\n'
            f'║  📍 x={self.robot_x:6.2f}  y={self.robot_y:6.2f}'
            f'  heading={heading:6.1f}°       ║\n'
            f'╠══════════════════════════════════════════════╣\n'
            f'║  LIDAR DIRECTIONS:                           ║\n'
            f'║            ↑ Front      : {front:5.2f} m            ║\n'
            f'║  ↖ FrontLeft: {front_left:5.2f} m   '
            f'FrontRight ↗: {front_right:5.2f} m  ║\n'
            f'║  ←  Left    : {left:5.2f} m   '
            f'Right      →: {right:5.2f} m  ║\n'
            f'║            ↓ Back       : {back:5.2f} m            ║\n'
            f'╠══════════════════════════════════════════════╣\n'
            f'║  🎯 Closest : {closest:5.2f} m  @ {closest_ang:3d}°              ║\n'
            f'║  {ZONE_ICON[zone]} Zone    : {zone:<38}║\n'
            f'╚══════════════════════════════════════════════╝'
        )

        # ── Save to CSV ───────────────────────────────────────────
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                ts, room,
                round(self.robot_x, 3), round(self.robot_y, 3),
                heading,
                round(front, 3), round(front_left, 3),
                round(front_right, 3), round(left, 3),
                round(right, 3), round(back, 3),
                round(closest, 3), closest_ang, zone
            ])


def main(args=None):
    rclpy.init(args=args)
    node = FourWheelScanner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\n\n========== SESSION SUMMARY ==========')
        print(f'Total scans collected : {node.scan_count}')
        print(f'Final position        : x={node.robot_x:.2f} y={node.robot_y:.2f}')
        print(f'Data saved to         : {node.csv_file}')
        print('=====================================\n')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()