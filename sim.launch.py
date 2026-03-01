import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    pkg = get_package_share_directory('diff_robot')

    # Process URDF
    xacro_file = os.path.join(pkg, 'urdf', 'robot.urdf.xacro')
    robot_description = xacro.process_file(xacro_file).toxml()

    # Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={
            'world': os.path.join(pkg, 'worlds', 'test_world.world')
        }.items()
    )

    # Robot state publisher
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # Spawn robot
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'diff_robot',
            '-x', '0', '-y', '0', '-z', '0.1'
        ],
        output='screen'
    )

    # SLAM Toolbox — builds map from LiDAR automatically
    slam = Node(
    package='slam_toolbox',
    executable='async_slam_toolbox_node',
    name='slam_toolbox',
    parameters=[{
        'use_sim_time': True,
        'odom_frame': 'odom',
        'map_frame': 'map',
        'base_frame': 'base_link',
        'scan_topic': '/scan',
        'mode': 'mapping',
        'resolution': 0.05,
        'max_laser_range': 8.0,
        'minimum_travel_distance': 0.001,   # ← very small
        'minimum_travel_heading': 0.001,    # ← very small
        'map_update_interval': 0.1,         # ← update every 0.1 sec
        'transform_timeout': 0.5,           # ← ADD THIS
        'tf_buffer_duration': 30.0,         # ← ADD THIS
        'stack_size_to_use': 40000000,      # ← ADD THIS
    }],
        output='screen'
    )

    # RViz with slam config
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg, 'config', 'slam_view.rviz')],
        output='screen'
    )

    return LaunchDescription([gazebo, rsp, spawn, slam, rviz])