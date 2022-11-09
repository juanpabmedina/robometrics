# GAZEBO-ROS: Vehicle System Tracking 

Gazebo traffic simulation of the center of the Pasto - Colombia with tracking vechicles using a trained YoloV5x model. 

## Specifications:

* Scaled map of the center of Pasto - Colombia.
* Cars moving on the streets.
* Computer vision model runing in real time (YoloV5x).
* Average velocity and indiviudal velocity of every single object detected. 
* Center of mass of the all objects detected. 

## Instalation: 

### ROS-Noetic:
Enable ROS repositories 

```cmd
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt install curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
```
Install.

```cmd
sudo apt update
sudo apt install ros-noetic-desktop-full
```
Set up enviroment variables.

```cmd
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
Install dependencies.

```cmd
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
sudo rosdep init
rosdep update
```

Download the files into your catkin workspace.

> catkin_ws/src/vehicle_trackin_system

Create a python virtual enviroment and install the requirements.txt 

```cmd
pip install -r requirements.txt
```

Download the tracker and put into the scipts folder. (https://liveudenaredu-my.sharepoint.com/:u:/g/personal/juanpab_m_udenar_edu_co/ERXid4rkLOtNrwkIDczr0jgBhTlt7uxdqmNfu8h5VJab_Q?e=e0hHYW)



Then compile your worksapce.

```cmd
catkin_make
```
