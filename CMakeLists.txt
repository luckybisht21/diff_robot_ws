cmake_minimum_required(VERSION 3.8)
project(diff_robot)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

# Install directories
install(DIRECTORY urdf launch worlds config
  DESTINATION share/${PROJECT_NAME}
)

# Install ALL Python scripts
install(PROGRAMS
  src/lidar_reader.py
  src/drive_and_scan.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()