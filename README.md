
# 3D Vision Project README.md Update

This repo is a fork of the original kinova-ros repo. Here we added and changed some things for our 3D Vision course project. Below, before the original content of this readme (starting at "Table of Contents"), we added some notes on what is needed to make the repo work for our application.


# Original README.md 


# Table of Contents 
- [3D Vision Project README.md Update](#3d-vision-project-readmemd-update)
- [Original README.md](#original-readmemd)
- [Table of Contents](#table-of-contents)
- [Important](#important)
- [Supported versions](#supported-versions)
- [Kinova-ROS](#kinova-ros)
  - [Installation](#installation)
  - [File System](#file-system)
  - [How to use the stack](#how-to-use-the-stack)
    - [Launch driver](#launch-driver)
    - [Joint position control](#joint-position-control)
    - [Cartesian position control](#cartesian-position-control)
      - [New in release 1.2.0](#new-in-release-120)
    - [Finger position control](#finger-position-control)
    - [Velocity Control for joint space and Cartesian space](#velocity-control-for-joint-space-and-cartesian-space)
    - [ROS service commands](#ros-service-commands)
    - [Cartesian Admittance mode](#cartesian-admittance-mode)
    - [Re-calibrate torque sensors](#re-calibrate-torque-sensors)
      - [New in release 1.2.0](#new-in-release-120-1)
    - [Support for 7 dof spherical wrist robot](#support-for-7-dof-spherical-wrist-robot)
      - [New in release 1.2.0](#new-in-release-120-2)
        - [Inverse Kinematics for 7 dof robot](#inverse-kinematics-for-7-dof-robot)
        - [Move robot in Null space](#move-robot-in-null-space)
    - [Torque control](#torque-control)
      - [New in release 1.2.0](#new-in-release-120-3)
        - [Gravity compensation](#gravity-compensation)
        - [Torque inactivity](#torque-inactivity)
  - [Ethernet connection](#ethernet-connection)
      - [New in release 1.2.0](#new-in-release-120-4)
  - [Parameters](#parameters)
      - [New in release 1.2.0](#new-in-release-120-5)
        - [General parameters](#general-parameters)
        - [Ethernet connection parameters](#ethernet-connection-parameters)
        - [Torque control parameters](#torque-control-parameters)
  - [rqt GUI for robot status](#rqt-gui-for-robot-status)
  - [Gazebo](#gazebo)
  - [MoveIt!](#moveit)
  - [New in this release](#new-in-this-release)
      - [New in release 1.2.1](#new-in-release-121)
      - [New in release 1.2.0](#new-in-release-120-6)
  - [Notes and Limitations](#notes-and-limitations)
  - [Report a Bug](#report-a-bug)


# Important

This repository contains source code and configuration files to support the Jaco, Jaco2 and Mico arms in ROS.

This repository doesn't support the Gen3 arm in ROS. Have a look at the [ros_kortex repository](https://github.com/Kinovarobotics/ros_kortex) for Gen3 ROS support!

# Supported versions
The master branch has been tested with ROS Noetic.

For older ROS version, checkout on corresponding branch : 

- [melodic-devel](https://github.com/Kinovarobotics/kinova-ros/tree/melodic-devel) for ROS Melodic and Ubuntu 18.04 support. 
- [kinetic-devel](https://github.com/Kinovarobotics/kinova-ros/tree/kinetic-devel) for ROS Kinetic and Ubuntu 16.04 support, but the branch is no longer maintained (the melodic-devel branch might work for this configuration). 
- [indigo-devel](https://github.com/Kinovarobotics/kinova-ros/tree/indigo-devel) for ROS Indigo and Ubuntu 14.04 support, but the branch is no longer maintained. 

# Kinova-ROS

The `kinova-ros` stack provides a ROS interface for the Kinova Robotics JACO, JACO2 and MICO robotic manipulator arms. Besides wide support of Kinova products, there are many bug fixes, improvements and new features as well. The stack is developed above the Kinova C++ API functions, which communicate with the DSP inside robot base. 

## Installation
To make kinova-ros part of your workspace, follow these steps (assuming your workspace is setup following the standard conventions):
```
cd ~/catkin_ws/src
git clone -b <branch-name> git@github.com:Kinovarobotics/kinova-ros.git kinova-ros
cd ~/catkin_ws
catkin_make
```
Another way to build your workspace would be to use the newer `catkin build`, which is part of the `catkin_tools` package:
```
# using apt-get
sudo apt-get install python-catkin-tools
# using pip
sudo pip install -U catkin_tools
```
Then, you add kinova-ros to your workspace and build it
```
cd ~/catkin_ws/src
git clone -b <branch-name> git@github.com:Kinovarobotics/kinova-ros.git kinova-ros
cd ~/catkin_ws
catkin build
```
More about the `catkin_tools` package in the [official documentation](https://catkin-tools.readthedocs.io/en/latest/index.html)

**Note :** To access the arm via usb copy the udev rule file `10-kinova-arm.rules` from `~/catkin_ws/src/kinova-ros/kinova_driver/udev` to `/etc/udev/rules.d/`:
```
sudo cp kinova_driver/udev/10-kinova-arm.rules /etc/udev/rules.d/
```

## File System
 - `kinova_bringup`: launch file to start kinova_driver and apply some configurations.
 - `kinova_control`: files used by Gazebo.
 - `kinova_demo`: python scripts for actionlibs in joint space and cartesian space.
 - `kinova_description`: robot urdf models and meshes are stored here.
 - `kinova_docs`: kinova_comm reference html files generated by doxygen. The comments are based on the reference of Kinova C++ API, and some additional information is provided. The documents of Kinova C++ API are automatically installed while installing Kinova SDK from the [Kinova website](http://www.kinovarobotics.com/service-robotics/products/software/)
 - `kinova_driver`: most essential files to run kinova-ros stack. Under the include folder, Kinova C++ API headers are defined in ../indlude/kinova, and ROS package header files are in kinova_driver folder. kinova_api source file is a wrap of Kinova C++ API, and kinova_comm builds up the fundamental functions. Some advanced accesses regarding to force/torque control are only provided in kinova_api. Most parameters and topics are created in kinova_arm. A general architecture from low level up could be:
    `DSP --> communicate --> Kinova C++ API --> wrapped --> kinova_api --> kinova_comm 
    --> {kinova_arm; kinova_fingers_action; kinova_joint_angles_action; ...} --> kinova_arm_driver.` **It is not recommended to modify kinova_comm and any level below it.** 
 - `kinova_gazebo`: ros package to launch a Gazebo simulation.
 - `kinova_moveit`: Everything related to Moveit! is stored here.
 - `kinova_msgs`: all the messages, servers and actionlib format are defined here.

## How to use the stack

### Launch driver
`kinova_robot.launch` in kinova_bringup folder launches the essential drivers and configurations for kinova robots. `kinova_robot.launch` has multiple arguments:

**kinova_robotType** specifies which robot type is used. For better supporting wider range of robot configurations,  *robot type* is defined by a `char[8]`, in the format of: `[{j|m|r|c}{1|2}{s|n}{4|6|7}{s|a}{2|3}{0}{0}]`. 
- *Robot category* `{j|m|r|c}` refers to *jaco*, *mico*, *roco* and *customized*
- *version* is `{1|2}` for now
- *wrist type* `{s|n}` can be spherical or *non-spherical*
- *Degree of Freedom* is possible to be `{4|6|7}`
- *robot mode* `{s|a}` can be in *service* or *assistive*
- *robot hand* `{2|3}` may equipped with *2 fingers* or *3 fingers* gripper. 
- The last two positions are *undefined* and *reserved* for further features.

**eg**: `j2n6s300` (default value) refers to *jaco v2 6DOF service 3 fingers*. Please be aware that not all options are valided for different robot types.

To avoid redundancy urdf for assistive models has been deleted. Please use the service 's' option instead.
For Mico 1 and 2 use the tag 'm1' for both.
For Jaco 1 and 2 use the tag 'j2' for both.

**kinova_robotName** and **kinova_robotSerial** were added to allow multiple robots under a ros master.
For applications like **moveIt!** set kinova_robotName to your prefix for the robot in the URDF. 
For example you can launch two jaco robots by using the following - 

```
roslaunch kinova_bringup kinova_robot.launch kinova_robotType:=j2n6s300 kinova_robotName:=left kinova_robotSerial:=PJ00000001030703130
roslaunch kinova_bringup kinova_robot.launch kinova_robotType:=j2n6s300 kinova_robotName:=right kinova_robotSerial:=PJ00000001030703133
```

These parameters are optional and can be dropped off when only one robot is connected.

**use_urdf** specifies whether the kinematic solution is provided by the URDF model. This is recommended and is the default option.

When `use_urdf:=true` (default value), the kinematic solution is automatically solved by the URDF model. 
The robot can be virtually presented in Rviz and the frames in Rviz are located at each of the joints. 
To visulize the robot in Rviz, run `$ rosrun rviz rviz`, and select **root** as the world frame. 
The robot model will synchronize the motion with the real robot.

If `use_urdf:=false`, the kinematic solution is the same as the DSP code inside the robot. 
Node `kinova_tf_updater` will be activated to publish frames, and the frames are defined 
according the classic D-H convention(frame may not located at joints). Even you are not able to visualize
the robot properly in Rviz, you would be able to observe the D-H frames in Rviz.

**eg**: `roslaunch kinova_bringup kinova_robot.launch kinova_robotType:=j2n6s300 use_urdf:=true`

If the robot is not able to move after boot, please try to home the arm by either pressing **home** button on the joystick or calling rosservice in the **ROS service commands** below.
```
rosservice call /'${kinova_robotType}'_driver/in/home_arm
```

### Joint position control
Joint position control can be realized by calling KinovaComm::setJointAngles() in customized node, or you may simply call the node `joints_action_client.py` in the kinova_demo package. This function takes three parameters : `kinova_robotType` (eg. j2n6s300), `unit {degree | radian}` and `value` (angles for each joint). The function takes the option `-r` that will tell the robot if the angle values are relative or absolute. It also has the options `-v` for more verbose output and `-h` for help. The following code will drive the 6th joint of a 6DOF Jaco2 robot to rotate +10 degree (not to 10 degree), and print additional information about the joint position.

**eg**: `rosrun kinova_demo joints_action_client.py -v -r j2n6s300 degree -- 0 0 0 0 0 10`

Joint position can be observed by echoing two topics:

`/'${kinova_robotType}_driver'/out/joint_angles` (in degree) and 

`/'${kinova_robotType}_driver'/out/joint_state` (in radians including finger information)

 **eg**: `rostopic echo -c /j2n6s300_driver/out/joint_state` will print out joint names (rad), position, velocity (rad/s) and effort (Nm) information.

Another way to control joint position is to use interactive markers in Rviz. Please follow the steps below to active interactive control:
  1. launch the drivers: `roslaunch kinova_bringup kinova_robot.launch kinova_robotType:=j2n6s300`
  2. start the node of interactive conrol: `rosrun kinova_driver kinova_interactive_control j2n6s300`
  3. open Rviz: `rosrun rviz rviz`
  4. in RViz (in the display section) change **Global Options** -> **Fixed Frame** to `world`
  5. add robot's model with **Add** -> **RobotModel** (in rviz folder)
  6. add interactive markers with **Add** -> **InteractiveMarkers** (in rviz folder)
  7. change **InteractiveMarkers** -> **Updated Topic** to `/j2n6s300_interactive_control_Cart/update`

  - A ring should appear around each joint, you can move the robot by movings those rings.

### Cartesian position control

Cartesian position control can be realized by calling KinovaComm::setCartesianPosition() in customized node. Alternatively, you may simply call the node pose_action_client.py in the kinova_demo package. This function takes three parameters : `kinova_robotType` (eg. j2n6s300), `unit {mq | mdeg | mrad}` (which refers to meter&Quaternion, meter&degree and meter&radian) and `pose_value`. The last argument, `pose_value`, is the position (in coordonates x,y,z) followed by the orientation (either 3 or 4 values based on unit). The unit of position is always meter, and the unit of orientation is different. Degree and radian are in relation to Euler Angles in XYZ order. Please be aware that the length of parameters are different when using Quaternion and Euler Angles. The function takes the option `-r` that will tell the robot if the angle values are relative or absolute. It also has the options `-v` for more verbose output and `-h` for help. The following code will drive a Jaco2 robot to move along +x axis for 1cm and rotate the hand for +10 degree along hand axis.

**eg**: `rosrun kinova_demo pose_action_client.py -v -r j2n6s300 mdeg -- 0.01 0 0 0 0 10`

The Cartesian coordinate of robot root frame is defined by the following rules:
- origin is the intersection point of the bottom plane of the base and cylinder center line.    
- +x axis is directing to the left when facing the base panel (where power switch and cable socket locate).
- +y axis is towards to user when facing the base panel.
- +z axis is upwards when robot is standing on a flat surface.

The kinova_tool_pose_action (action server called by `pose_action_client.py`) will send Cartesian position commands to the robot and the inverse kinematics will be handled within the robot. **Important** The inverse kinematics algorithm that is implemented within Kinova robots is programmed to automatically avoid singularities and self-collisions. To perform those avoidance, the algorithm will restrict access to some parts of the robot's workspace. It may happen that the Cartesian pose goal you send cannot be reached by the robot, although it belongs to the robot's workspace. For more details on why this can happen, and what can you do to avoid this situation, please see the Q & A in [issue #149](https://github.com/Kinovarobotics/kinova-ros/issues/149). As a rule of thumb, if you are not able to reach the pose you are commanding in `pose_action_client.py` by moving your Kinova robot with the Kinova joystick, the robot will not be able to reach this same pose with the action server either. If you do not want to use the robot's IK solver, you can always use MoveIt instead. 

The current Cartesian position is published via topic: `/'${kinova_robotType}_driver'/out/tool_pose`

In addition, the wrench of end-effector is published via topic: `/'${kinova_robotType}_driver'/out/tool_wrench`

Again, you can also use interactive markers in Rviz for Cartesian position :
  1. launch the drivers: `roslaunch kinova_bringup kinova_robot.launch kinova_robotType:=j2n6s300`
  2. start the node of interactive conrol: `rosrun kinova_driver kinova_interactive_control j2n6s300`
  3. open Rviz: `rosrun rviz rviz`
  4. in RViz (in the display section) change **Global Options** -> **Fixed Frame** to `world`
  5. add robot's model with **Add** -> **RobotModel** (in rviz folder)
  6. add interactive markers with **Add** -> **InteractiveMarkers** (in rviz folder)
  7. change **InteractiveMarkers** -> **Updated Topic** to `/j2n6s300_interactive_control_Cart/update`

  - A cubic with 3 axis (translation) and 3 rings(rotation) should appear at the end-effector, you can move the robot by dragging the axis or rings.

#### New in release 1.2.0
Executing multiple Cartesian waypoints without stopping  
The action client executes one goal at a time. In case the user wants to give multiple waypoints to the robot without stopping at every waypoint, the service `AddPoseToCartesianTrajectories` can be used. 
This service adds the commanded poses to a buffer that that maintained by the robot. The robot executes the poses in this buffer in the order that they are added, without stopping between poses.

The service `ClearTrajectories` can be used to clear the trajectory buffer in the base.

### Finger position control
Cartesian position control can be realized by calling KinovaComm::setFingerPositions() in customized node. Alternatively, you may simply call the node `fingers_action_client.py` in the kinova_demo package. This function takes three parameters : `kinova_robotType` (eg. j2n6s300), `unit {turn | mm | percent}` and `finger_value`. The finger is essentially controlled by `turn`, and the rest units are propotional to `turn` for convenience. The value 0 indicates fully open, while `finger_maxTurn` represents fully closed. The value of `finger_maxTurn` may vary due to many factors. A proper reference value for a finger turn will be 0 (fully-open) to 6800 (fully-close). If necessary, please modify this variable in the code. The function also takes the option `-r` that will tell the robot if the angle values are relative or absolute. It also has the options `-v` for more verbose output and `-h` for help. The following code fully closes the fingers.

**eg**: `rosrun kinova_demo fingers_action_client.py j2n6s300 percent -- 100 100 100`

The finger position is published via topic: `/'${kinova_robotType}_driver'/out/finger_position`

### Velocity Control for joint space and Cartesian space
The user has access to both joint velocity and Cartesian velocity (angular velocity and linear velocity). The joint velocity control can be realized by publishing to topic  `/'${kinova_robotType}_driver'/in/joint_velocity`. The following command can move the 6th joint of a Jaco robot at a rate of approximate 10 degree/second. Please be aware that the publishing rate **does** affect the speed of motion.

**eg**: `rostopic pub -r 100 /j2n6s300_driver/in/joint_velocity kinova_msgs/JointVelocity "{joint1: 0.0, joint2: 0.0, joint3: 0.0, joint4: 0.0, joint5: 0.0, joint6: 10.0}" ` 

For Cartesian linear velocity, the unit is meter/second. Definition of angular velocity "Omega" is based on the skew-symmetric matrices "S = R*R^(-1)", where "R" is the rotation matrix. angular velocity vector "Omega = [S(3,2); S(1,3); S(2,1)]". The unit is radian/second.  An example is given below:

**eg**: `rostopic pub -r 100 /j2n6s300_driver/in/cartesian_velocity kinova_msgs/PoseVelocity "{twist_linear_x: 0.0, twist_linear_y: 0.0, twist_linear_z: 0.0, twist_angular_x: 0.0, twist_angular_y: 0.0, twist_angular_z: 10.0}" `

The motion will stop once the publish on the topic is finished. Please be cautious when using velocity control as it is a continuous motion unless you stop it.

**Note on publish frequency** : The joint velocity is set to publish at a frequency of 100Hz, due to the DSP inside the robot which loops each 10ms. Higher frequency will not have any influence on the speed. However, it will fill up a buffer (size of 2000) and the robot may continue to move a bit even after it stops receiving velocity topics. For a frequency lower than 100Hz, the robot will not able to achieve the requested velocity.

Therefore, the publishing rate at 100Hz is not an optional argument, but a requirement.

### ROS service commands
Users can home the robot with the command below. It takes no argument and brings the robot to pre-defined home position. The command supports customized home position that users can define by using the SDK or JacoSoft as well.
`rosservice call /'${kinova_robotType}_driver'/in/home_arm`

Users can also enable and disable the ROS motion commands with these rosservices :
`rosservice call /'${kinova_robotType}_driver'/in/start`
`/'${kinova_robotType}_driver'/in/stop`
When `stop` is called, robot commands from ROS will not drive the robot until `start` is called. However, the joystick still has the control during this phase.

### Cartesian Admittance mode 
This lets the user control the robot by manually (by hand).
The admittance force control can be actived and deactivated with these commands :
```
rosservice call /'${kinova_robotType}_driver'/in/start_force_control
rosservice call /'${kinova_robotType}_driver'/in/stop_force_control
```
The user can move the robot by applying force/torque to the end-effector/joints. When there is a Cartesian/joint position command, the result motion will be a combination of both force and position commands.

### Re-calibrate torque sensors

#### New in release 1.2.0
Over time it is possible that the torque sensors develop offsets in reporting absolute torque. For this they need to be re-calibrated. The calibration process is very simple -   
1. Move the robot to candle like pose (all joints 180 deg, robot links points straight up). This configuration ensures zero torques at joints.  
2. Call the service `rosservice call /'${kinova_robotType}_driver'/in/set_zero_torques`

### Support for 7 dof spherical wrist robot
#### New in release 1.2.0 
Support for the 7 dof robot has been added in this new release. All of the previous control methods can be used on a 7 dof Kinova robot.

##### Inverse Kinematics for 7 dof robot
The inverse kinematics of the 7 dof robot results in infinite possible solutions for a give pose command. The choice of the best solution (redundancy resolution) is done in the base of the robot considering criteria such as joint limits, closeness to singularities.

##### Move robot in Null space
To see the full set of solutions, a new fuction is introduced in KinovaAPI - StartRedundantJointNullSpaceMotion(). When in this mode the Kinova joystick can be used to move the robot in null space while keeping the end-effector maintaining its pose.

The mode can be activated by calling the service SetNullSpaceModeState - `${kinova_robotType}_driver /in/set_null_space_mode_state` 
Pass 1 to service to enable and 0 to disable.

### Torque control 
#### New in release 1.2.0 
Torque control has been made more accessible. Now you can publish torque/force commands just like joint/cartesian velocity. To do this you need to :

1. Optional - Set torque parameters  
Usually default parameters should work for most applications. But if you need to change some torque parameters, you can set parameters (listed at the end of page) and then call the service -   
SetTorqueControlParameters `${kinova_robotType}_driver/in/set_torque_control_parameters`

2. Switch to torque control from position control  
You can do this using the service  - SetTorqueControlMode `${kinova_robotType}_driver'/in/set_torque_control_mode`

3. Publish torque commands `rostopic pub -r 100 /j2n6s300_driver/in/joint_torque kinova_msgs/JointTorque "{joint1: 0.0, joint2: 0.0, joint3: 0.0, joint4: 0.0, joint5: 0.0, joint6: 1.0}"`

##### Gravity compensation
Gravity compensation is done by default in the robot's base. This means that if the robot is commanded zero torques the robot does not fall under gravity. This case (zero commanded torque) 
can be refered to as `gravity compensated mode`. The robot can be moved around freely by manually pushing its joints. You can try out this mode by using the command (for a j2n6s300)
```
rosrun kinova_demo gravity_compensated_mode.py j2n6s300 
```
This command moves the robot to a candle-like pose, sets torques to zero, and then starts torque control mode. It publishes torque commands as `[0,0,0,0,0,0]`, so the robot can be moved by pushing on individual joints.

It is posible to publish torque with or without gravity compensation by setting the parameter -
```
publish_torque_with_gravity_compensation: false
```

##### Torque inactivity
If not torque command is sent after a given
time (250ms by default), the controller will take an action: (0): The robot will return in position
mode (1): The torque commands will be set to zero. By default, option (1) is set for Kinova classic robots
(Jaco2 and Mico) while option (0) is set for generic mode.

## Ethernet connection
#### New in release 1.2.0 
**Note** - Although this release supports Ethernet connection, this feature is limited.
Kinova will notify all users when Ethernet support is released for all customers. 

Support for Ethernet connection has been added. All functionalities available in USB are available in Ethernet. 
To use ethernet follow these steps
1. Setup a static IP address for your ethernet network say - 192.168.100.100
2. With the robot connected to your PC via USB open kinova's Develepment Center
3. Open tab General/Ethernet - Set robot IP Address to something like - 192.168.100.xxx 
4. Make sure MAC address is not all zero. If so contact support@kinova.ca
5. Press 'Update' and restart robot
6. In a terminal ping your robot's IP, your robot is setup for ethernet

To connect to robot via ethernet in ROS just set these parameters in robot_parameters.yaml - 
```
connection_type: Ethernet  
local_machine_IP: [your PC network IP]  
subnet_mask: [your network subnet mask]  
```


## Parameters
#### New in release 1.2.0 
##### General parameters
* `serial_number: PJ00000001030703130` Leave commented out if you want to control the first robot found connected.  
* `jointSpeedLimitParameter1: 10` Joint speed limit for joints 1, 2, 3 in deg/s
* `jointSpeedLimitParameter2: 20` Joint speed limit for joints 4, 5, 6 in deg/s
* `payload: [0, 0, 0, 0]` payload: [COM COMx COMy COMz] in [kg m m m]  
* `connection_type: USB` Ethernet or USB
##### Ethernet connection parameters
```
ethernet: {
	local_machine_IP: 192.168.100.100,  
	subnet_mask: 255.255.255.0,  
	local_cmd_port: 25000,  
	local_broadcast_port: 25025  
}
```

##### Torque control parameters
Comment these out to use default values.

torque_parameters:

* `publish_torque_with_gravity_compensation: false`
* `torque_min: [1, 0, 0, 0, 0, 0, 0]`
* `torque_max: [50, 0, 0, 0, 0, 0, 0]`  
  If one torque min/max value is sepecified, all min/max values need to be specified  
* `safety_factor: 1`  
  Decides velocity threshold at which robot switches torque to position control (between 0 and 1)  
* `com_parameters: [0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 0,0,0,0,0,0,0, 0,0,0,0,0,0,0]`
  COM parameters, order [m1,m2,...,m7,x1,x2,...,x7,y1,y2,...y7,z1,z2,...z7]
  

## rqt GUI for robot status 
ROS provides a flexible GUI tool to interact with nodes/robots - **rqt**. You can use this
tool to see topics published by the node - robot position, velocity, torque, etc. 
You can also launch services like AddPoseToCartesianTrajectory.

Monitoring topics

- Launch rqt by typing the command `rqt`
- In the plugin tab, select Topics/Topics monitor
- Select any messages to see published position/torque etc. values

Other plugins in rqt can similarly be used for quick interation with the robot.

## Gazebo 
More informations about Gazebo available [here](https://github.com/Kinovarobotics/kinova-ros/tree/master/kinova_gazebo)

## MoveIt!
More informations about MoveIt! available [here](https://github.com/Kinovarobotics/kinova-ros/tree/master/kinova_moveit)

## New in this release 
#### New in release 1.2.1
A few bug fixes:

Specific to 7 dof robot:
- PID controller parameters for the 7 dof robot with spherical wrist (before, the Gazebo model was unstable when launched)
- addition of an is7dof argument in kinova_gazebo/launch/robot_launch.launch and kinova_control/launch/kinova_control.launch to load joint_7_position_controller in addition to other position_controllers when launching the gazebo model with use_trajectory_controller set to false and a 7 dof robot. This argument has to be set to true for a 7 dof robot. 
- correction in kinova_control/launch/j2s7s300.perspective (rqt tool was publishing to wrong topic)

Specific to MICO robot:
- correction in kinova_control/launch/m1n6s200.perspective (rqt tool was publishing to wrong topic)

For all robots:
- fix in home_arm service (before, was not working when robot was connected through Ethernet)
- commented out the COM parameters all set to zero in kinova_bringup/launch/config/robot_parameters.yaml, or else the robot does not compensate gravity accurately when switched to admittance or torque mode. These COM parameters can be commented out if the user wants to change the default COM parameters, but by default, we take for granted that the user wants to use the parameters already implemented in the robot.
- change the order conditions are checked in the kinova_joint_angles_action.cpp, kinova_tool_pose_action.cpp and kinova_fingers_action.cpp to ensure that the robot does not accept new goals after having been stopped (emergency stop). See issue #92 for more details. 

#### New in release 1.2.0
- Gazebo support
- MoveIt! support
- Restructured URDF files
- Support for 7 dof robot
- Support for Ethernet
- Torque control through publisher/subscriber
- Force control through publisher/subscriber
- Torque control parameters
- Speed limit for actionlib Cartesian/Joint control
- Parameterized base_frame for tf_generator
- Finger models are now updated in RViz
- Ring models added to URDF
- New demo file - gravity_compensated_mode.py
- Test/demo file - TestSrv.py
- New services
  - SetTorqueControlParameters
  - SetZerotorque
  - SetNullSpaceModeState
  - AddPoseToCartesianTrajectory
  - ClearTrajectories
  - SetTorqueControlMode

## Notes and Limitations
1. Force/torque control is only for advanced users. Please use caution when using force/torque control api functions.

2. The ``joint_state`` topic currently reports the joint Names, Position,Velocity and Effort. Depending on your firmware version velocity values can be wrong. 

3. When updating the firmware on the arm (e.g., using Development Center) the serial number will be set to "Not set" which will cause multiple arms to be unusable. The solution is to make sure that the serial number is reset after updating the arm firmware.

4. Some virtualization software products are known to work well with this package, while others do not.  The issue appears to be related to proper handover of access to the USB port to the API.  Parallels and VMWare are able to do this properly, while VirtualBox causes the API to fail with a "1015" error.

5. Previously, files under ``kinova-ros/kinova_driver/lib/i386-linux-gnu`` had a bug which required users on 32-bit systems to manually copy them into devel or install to work. This package has not been tested with 32-bit systems and this workaround may still be required. 64-bit versions seem to be unaffected.


## Report a Bug
Any bugs, issues or suggestions may be sent to support@kinova.ca
