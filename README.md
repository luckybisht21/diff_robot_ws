# 🤖 4-Wheel Differential Drive Robot with LiDAR — ROS2 Humble + Gazebo

A simulated 4-wheel differential drive robot with a 360° LiDAR sensor, built using **ROS2 Humble** and **Gazebo**. The robot navigates a multi-room arena, collects real-time LiDAR scan data, builds a live map using **SLAM Toolbox**, and exports sensor readings to Excel with algorithm analysis.

---

## 📸 Demo

> Gazebo simulation with LiDAR rays visible, RViz SLAM map building in real time as the robot drives through 4 rooms.

---

## 🗂️ Project Structure

```
diff_robot_ws/
└── src/
    └── diff_robot/
        ├── urdf/
        │   └── robot.urdf.xacro       # 4-wheel robot + LiDAR description
        ├── launch/
        │   └── sim.launch.py          # Gazebo + RViz + SLAM launch
        ├── worlds/
        │   └── test_world.world       # 4-room arena with colored objects
        ├── config/
        │   └── slam_view.rviz         # Pre-configured RViz layout
        ├── src/
        │   ├── drive_and_scan.py      # LiDAR data collector + terminal output
        │   ├── live_map.py            # Real-time matplotlib map
        │   └── data_extractor.py      # CSV report generator
        ├── CMakeLists.txt
        └── package.xml
```

---

## ✨ Features

- **4-Wheel Robot** — rear differential drive (2 powered wheels) + 2 passive front wheels
- **360° LiDAR** — 8m range, 360 samples/scan, Gaussian noise simulation
- **Multi-Room Arena** — 4 rooms with colored obstacles (red boxes, green cylinders, blue walls, yellow objects)
- **SLAM Mapping** — live occupancy grid map built as you drive using `slam_toolbox`
- **Real-Time Terminal Data** — live LiDAR readings (front, left, right, back, closest, zone) printed every scan
- **CSV Export** — all scan data saved automatically while driving
- **Excel Analysis** — 6 algorithms applied to LiDAR data exported to `.xlsx`
- **Live Matplotlib Map** — Python map window showing robot path + LiDAR point cloud by room

---

## 🧰 Prerequisites

### System
- Ubuntu 22.04
- ROS2 Humble
- Gazebo Classic (comes with ROS2 Humble desktop)

### Install dependencies

```bash
sudo apt update
sudo apt install -y \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-robot-state-publisher \
  ros-humble-xacro \
  ros-humble-teleop-twist-keyboard \
  ros-humble-rviz2 \
  ros-humble-slam-toolbox \
  ros-humble-nav2-map-server

pip install openpyxl pandas numpy matplotlib --break-system-packages
```

---

## 🚀 Installation

```bash
# Create workspace
mkdir -p ~/diff_robot_ws/src
cd ~/diff_robot_ws/src

# Clone repo
git clone https://github.com/YOUR_USERNAME/diff_robot.git

# Install ROS dependencies
cd ~/diff_robot_ws
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build --symlink-install
source install/setup.bash
```

---

## ▶️ Running the Simulation

### Terminal 1 — Launch Gazebo + RViz + SLAM
```bash
source ~/diff_robot_ws/install/setup.bash
ros2 launch diff_robot sim.launch.py
```

### Terminal 2 — Start LiDAR Data Collection
```bash
source ~/diff_robot_ws/install/setup.bash
python3 src/diff_robot/src/drive_and_scan.py
```

### Terminal 3 — Drive the Robot
```bash
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p use_sim_time:=true
```

### Terminal 4 (Optional) — Live Matplotlib Map
```bash
source ~/diff_robot_ws/install/setup.bash
python3 src/diff_robot/src/live_map.py
```

---

## 🕹️ Teleop Controls

| Key | Action |
|-----|--------|
| `i` | Move forward |
| `,` | Move backward |
| `j` | Rotate left |
| `l` | Rotate right |
| `k` | Stop |
| `q` / `z` | Speed up / slow down |

---

## 🏠 Arena Layout

```
(-6,6)_________________________(6,6)
  |          |  door  |          |
  |  ROOM 3  |        |  ROOM 4  |
  |  🔵 BLUE |        | 🟡 YELLOW|
  |..........door......|..........|
  |  ROOM 1  |        |  ROOM 2  |
  |  🔴 RED  |        | 🟢 GREEN |
  |          |  door  |          |
(-6,-6)________________________(6,-6)

  Robot spawns at (0,0) — center
```

Each room contains different shaped obstacles (boxes + cylinders) that the LiDAR detects.

---

## 📡 LiDAR Terminal Output

As you drive, the terminal prints live data every scan:

```
╔══════════════════════════════════════════════╗
║  SCAN #42     Room1-RED                      ║
║  📍 x= -2.34  y= -1.87  heading=  45.2°     ║
╠══════════════════════════════════════════════╣
║  LIDAR DIRECTIONS:                           ║
║            ↑ Front      :  0.82 m            ║
║  ↖ FrontLeft:  1.20 m   FrontRight ↗:  0.95 m  ║
║  ←  Left    :  2.10 m   Right      →:  1.45 m  ║
║            ↓ Back       :  3.20 m            ║
╠══════════════════════════════════════════════╣
║  🎯 Closest :  0.82 m  @   0°               ║
║  🟡 Zone    : CAUTION                        ║
╚══════════════════════════════════════════════╝
```

### Zone Classification

| Zone | Distance | Meaning |
|------|----------|---------|
| 🔴 DANGER | < 0.5 m | Object very close |
| 🟡 CAUTION | 0.5 – 1.0 m | Object nearby |
| 🟢 SAFE | ≥ 1.0 m | Clear path |

---

## 📊 Data Export

### CSV
All scan data is automatically saved while driving:
```
~/diff_robot_ws/lidar_data.csv
```

Columns: `timestamp, room, robot_x, robot_y, heading_deg, front_m, front_left_m, front_right_m, left_m, right_m, back_m, closest_dist_m, closest_angle_deg, zone`

### Excel Analysis
Run after your session to generate a full Excel report:
```bash
python3 src/diff_robot/src/data_extractor.py
```

The `.xlsx` file contains 5 sheets:

| Sheet | Contents |
|-------|----------|
| 📡 Raw LiDAR Data | All scan rows, color-coded by room |
| 📊 Room Statistics | Min/Max/Avg per room via Excel formulas |
| 🧮 Algorithm Analysis | 6 algorithms applied to every scan |
| 📈 Algorithm Summary | Per-room comparison + bar/line charts |
| ℹ️ How To Use | Guide to the workbook |

### Algorithms Applied

| Algorithm | Description |
|-----------|-------------|
| **A — Threshold Filter** | Flags scans where closest distance < 0.8 m |
| **B — Moving Average** | Smooths readings over a 5-scan rolling window |
| **C — Z-Score** | Detects statistical outliers beyond ±2 std deviations |
| **D — Gradient** | Detects sudden distance changes > 0.3 m (object edges) |
| **E — Normalize** | Scales all readings 0–1 for cross-room comparison |
| **F — Danger Zone** | Classifies each scan as DANGER / CAUTION / SAFE |

---

## 🗺️ SLAM Map

The simulation uses `slam_toolbox` to build a live occupancy grid map in RViz:

```
Grey  = Unknown space (not yet explored)
White = Free space (robot has driven here)
Black = Walls and objects detected by LiDAR
```

### Save the map after exploring
```bash
ros2 run nav2_map_server map_saver_cli -f ~/diff_robot_ws/my_arena_map
```

This saves:
- `my_arena_map.pgm` — image of the complete map
- `my_arena_map.yaml` — map metadata

---

## 📡 ROS2 Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/scan` | `sensor_msgs/LaserScan` | LiDAR 360° scan data |
| `/odom` | `nav_msgs/Odometry` | Robot position and velocity |
| `/cmd_vel` | `geometry_msgs/Twist` | Velocity commands |
| `/map` | `nav_msgs/OccupancyGrid` | SLAM occupancy grid |
| `/tf` | `tf2_msgs/TFMessage` | Transform tree |

---

## 🤖 Robot Specifications

| Parameter | Value |
|-----------|-------|
| Drive Type | 4-wheel, rear differential |
| Chassis Size | 0.4 × 0.3 × 0.1 m |
| Wheel Radius | 0.06 m |
| Wheel Separation | 0.34 m |
| LiDAR Range | 0.15 – 8.0 m |
| LiDAR Samples | 360 per scan |
| LiDAR Update Rate | 30 Hz |

---

## 🛠️ Built With

- [ROS2 Humble](https://docs.ros.org/en/humble/) — Robot Operating System
- [Gazebo Classic](https://classic.gazebosim.org/) — Physics simulation
- [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox) — Mapping
- [RViz2](https://github.com/ros2/rviz) — Visualization
- [OpenPyXL](https://openpyxl.readthedocs.io/) — Excel export
- [Matplotlib](https://matplotlib.org/) — Live map visualization

---

## 📄 License

MIT License — feel free to use and modify.

---

## 🙋 Author

Lucky Bisht
- GitHub: https://github.com/luckybisht21

---

> Built as a learning project for ROS2 robotics, LiDAR sensing, SLAM mapping, and sensor data analysis.
