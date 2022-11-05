# GAZEBO-ROS: Vehicle System Tracking 

Gazebo traffic simulation of the center of the Pasto - Colombia with tracking vechicles using a trained YoloV5x model. 

## Specifications:

* Scaled map of the center of Pasto - Colombia.
* Cars moving on the streets.
* Computer vision model runing in real time (YoloV5x).
* Average velocity and indiviudal velocity of every single object detected. 
* Center of mass of the all objects detected. 

## Instalation: 

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
