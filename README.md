# 🤖 4-Wheel Differential Drive Robot with LiDAR SLAM

### ROS2 Humble · Gazebo Classic · SLAM Toolbox · Python

[![ROS2](https://img.shields.io/badge/ROS2-Humble-blue?style=for-the-badge&logo=ros)](https://docs.ros.org/en/humble/)
[![Gazebo](https://img.shields.io/badge/Gazebo-Classic-orange?style=for-the-badge)](https://classic.gazebosim.org/)
[![Python](https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-E95420?style=for-the-badge&logo=ubuntu)](https://ubuntu.com/)

---

> A fully simulated **4-wheel differential drive robot** with a 360° LiDAR sensor that navigates a custom multi-room arena, builds a live SLAM map, streams real-time sensor data to the terminal, and exports all readings to an Excel workbook with 6 analysis algorithms.

---

## 📽️ Demo Video

[![Watch Demo](https://img.shields.io/badge/%E2%96%B6%20Watch%20Demo-YouTube-red?style=for-the-badge&logo=youtube)](https://youtu.be/-FZfNeMrx5M)
> *Robot driving through all 4 rooms — LiDAR rays visible in Gazebo, SLAM map building live in RViz, terminal printing real-time distance readings*

---

## ✨ Features

| Feature                | Details                                                               |
| ---------------------- | --------------------------------------------------------------------- |
| 🚗 **4-Wheel Robot**    | Rear differential drive (2 powered) + 2 passive front wheels          |
| 📡 **360° LiDAR**       | 8 m range · 360 samples/scan · 30 Hz · Gaussian noise model           |
| 🏠 **Multi-Room Arena** | 4 rooms · coloured obstacles (boxes + cylinders) · doorways           |
| 🗺️ **SLAM Mapping**    | Live occupancy grid via `slam_toolbox` — map builds as you drive      |
| 🖥️ **Live Terminal**   | Real-time directional readings · closest object · zone classification |
| 📊 **Excel Analysis**   | 6 algorithms across all scan data · colour-coded · per-room charts    |
| 🗺️ **Matplotlib Map**  | Live Python map showing robot path + LiDAR point cloud by room        |
| 💾 **CSV Export**       | All scan data auto-saved with timestamp, room, position, heading      |

---

## 🏠 Arena Layout

```
(-6,6) _________________________ (6,6)
      |         | door |         |
      |  ROOM 3 |      |  ROOM 4 |
      |  🔵 BLUE|      |🟡 YELLOW|
      |_________door___|_________|
      |  ROOM 1 |      |  ROOM 2 |
      |  🔴 RED |      | 🟢 GREEN|
      |         | door |         |
(-6,-6)_________________________(6,-6)
                  ↑
            Robot spawns here (0,0)
```

Each room has uniquely shaped and coloured obstacles that the LiDAR detects differently — making each room's scan data distinct and identifiable.

---

## 📡 Live Terminal Output

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

| Zone      | Threshold | Meaning                            |
| --------- | --------- | ----------------------------------- |
| 🔴 DANGER  | < 0.5 m   | Obstacle very close — stop or turn |
| 🟡 CAUTION | < 1.0 m   | Obstacle nearby — slow down        |
| 🟢 SAFE    | ≥ 1.0 m   | Clear path ahead                   |

---

## 📊 Excel Analysis Pipeline

Run `data_extractor.py` after your session to generate a full `.xlsx` report:

| Sheet                | Contents                                         |
| --------------------- | -------------------------------------------------- |
| 📡 Raw LiDAR Data     | All scan rows colour-coded by room               |
| 📊 Room Statistics    | Min / Max / Avg per room via live Excel formulas |
| 🧮 Algorithm Analysis | 6 algorithms applied to every single scan row    |
| 📈 Algorithm Summary  | Per-room comparison + bar and line charts        |
| ℹ️ How To Use        | Workbook guide                                   |

### 6 Algorithms Applied

| # | Algorithm              | What it does                                        |
| --- | ---------------------- | ----------------------------------------------------- |
| A | **Threshold Filter**   | Flags scans where closest object < 0.8 m            |
| B | **Moving Average**     | Smooths noisy readings over a 5-scan rolling window |
| C | **Z-Score Outlier**    | Detects abnormal readings beyond ±2 std deviations  |
| D | **Gradient Detection** | Finds object edges — sudden distance change > 0.3 m |
| E | **Min-Max Normalise**  | Scales all readings 0–1 for cross-room comparison   |
| F | **Danger Zone**        | Classifies every scan as DANGER / CAUTION / SAFE    |

---

## 🤖 Robot Specifications

| Parameter         | Value                      |
| ------------------ | ---------------------------- |
| Drive Type         | 4-wheel, rear differential |
| Chassis Size       | 0.4 × 0.3 × 0.1 m          |
| Wheel Radius       | 0.06 m                     |
| Wheel Separation   | 0.34 m                     |
| LiDAR Range        | 0.15 – 8.0 m               |
| LiDAR Samples      | 360 per scan               |
| LiDAR Update Rate  | 30 Hz                      |
| Noise Model        | Gaussian (σ = 0.01 m)      |

---

## 📡 ROS2 Topics

| Topic                              | Message Type             | Description                 |
| ------------------------------------ | -------------------------- | ------------------------------ |
| `/scan`                            | `sensor_msgs/LaserScan`  | 360° LiDAR scan data        |
| `/odom`                            | `nav_msgs/Odometry`      | Robot position and velocity |
| `/cmd_vel`                         | `geometry_msgs/Twist`    | Velocity commands           |
| `/map`                             | `nav_msgs/OccupancyGrid` | SLAM occupancy grid         |
| `/tf`                              | `tf2_msgs/TFMessage`     | Transform tree              |
| `/slam_toolbox/scan_visualization` | `sensor_msgs/LaserScan`  | SLAM processed scan         |

---

## 🗂️ Project Structure

```
diff_robot_ws/
└── src/
    └── diff_robot/
        ├── urdf/
        │   └── robot.urdf.xacro       # 4-wheel robot + LiDAR URDF
        ├── launch/
        │   └── sim.launch.py          # Gazebo + RViz + SLAM all-in-one
        ├── worlds/
        │   └── test_world.world       # 4-room arena world file
        ├── config/
        │   └── slam_view.rviz         # Pre-configured RViz layout
        ├── src/
        │   ├── drive_and_scan.py      # LiDAR data collector + terminal output
        │   ├── live_map.py            # Real-time matplotlib map
        │   └── data_extractor.py      # Post-session CSV → Excel report
        ├── CMakeLists.txt
        └── package.xml
```

---

## 🧰 Prerequisites

- **OS:** Ubuntu 22.04
- **ROS2:** Humble Hawksbill
- **Simulator:** Gazebo Classic

---

## ⚡ Quick Start

### 1 — Install dependencies

```bash
sudo apt update && sudo apt install -y \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-robot-state-publisher \
  ros-humble-xacro \
  ros-humble-teleop-twist-keyboard \
  ros-humble-rviz2 \
  ros-humble-slam-toolbox \
  ros-humble-nav2-map-server

pip install openpyxl pandas numpy matplotlib --break-system-packages
```

### 2 — Clone and build

```bash
mkdir -p ~/diff_robot_ws/src && cd ~/diff_robot_ws/src
git clone https://github.com/luckybisht21/diff_robott_ws.git
cd ~/diff_robot_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

### 3 — Launch simulation

```bash
# Terminal 1 — Gazebo + RViz + SLAM
source ~/diff_robot_ws/install/setup.bash
ros2 launch diff_robot sim.launch.py

# Terminal 2 — Live LiDAR terminal data + CSV logging
source ~/diff_robot_ws/install/setup.bash
python3 src/diff_robot/src/drive_and_scan.py

# Terminal 3 — Drive the robot
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -p use_sim_time:=true

# Terminal 4 (optional) — Live Python map
source ~/diff_robot_ws/install/setup.bash
python3 src/diff_robot/src/live_map.py
```

---

## 🕹️ Keyboard Controls

```
u  i  o
j  k  l       i = forward      , = backward
m  ,  .       j = turn left    l = turn right
              k = STOP

q / z  →  increase / decrease speed
```

---

## 🗺️ SLAM Map Guide

As you explore the arena the RViz map fills in:

```
■ Dark grey  =  Unknown (not yet explored)
□ White      =  Free space (robot has been here)
■ Black      =  Wall or obstacle detected by LiDAR
```

### Save the finished map

```bash
ros2 run nav2_map_server map_saver_cli -f ~/diff_robot_ws/my_arena_map
# Saves: my_arena_map.pgm  +  my_arena_map.yaml
```

---

## 📈 Generate Excel Report

After driving through the rooms, press `Ctrl+C` in Terminal 2, then:

```bash
python3 src/diff_robot/src/data_extractor.py
```

Opens `LiDAR_Analysis.xlsx` with all 5 sheets and charts ready.

---

## 🛠️ Built With

| Tool                                                          | Purpose                           |
| ---------------------------------------------------------------- | ------------------------------------ |
| [ROS2 Humble](https://docs.ros.org/en/humble/)                | Robot middleware and topic system |
| [Gazebo Classic](https://classic.gazebosim.org/)              | Physics-based robot simulation    |
| [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox) | Real-time occupancy grid mapping  |
| [RViz2](https://github.com/ros2/rviz)                         | 3D sensor data visualisation      |
| [OpenPyXL](https://openpyxl.readthedocs.io/)                  | Excel report generation           |
| [Matplotlib](https://matplotlib.org/) — Live map              | Python live map visualisation     |

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙋 Author

**Lucky Bisht**

- 🐙 GitHub: [@luckybisht21](https://github.com/luckybisht21)
- 📧 luckybisht0094@gmail.com
- 🎓 B.Tech Automation & Robotics — GGSIPU Delhi (2023–2027)

---

⭐ **Star this repo if it helped you!** ⭐

*Built for learning ROS2 robotics, LiDAR sensing, SLAM mapping, and sensor data analysis.*
