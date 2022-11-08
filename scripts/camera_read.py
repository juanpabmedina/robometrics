#!/usr/bin/env python3.8

# Tutorial link: https://dhanuzch.medium.com/using-opencv-with-gazebo-in-robot-operating-system-ros-part-1-display-real-time-video-feed-a98c078c708b
import rospy
import cv2
import torch
import numpy as np
import pandas as pd 
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Leemos el modelo
model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path = '/home/juanpabmedina/catkin_ws/src/camera_robot/scripts/tracker/best_100epochs.pt')



class camera_1():

  def __init__(self):

    self.vel = 0
    self.vel_mag = 0
    self.xy1 = np.zeros((1,6), dtype=int)
    self.pos_mag_1 = 0
    self.x_center_hst = []
    self.y_center_hst = []
    self.ad_time_change = 0
    self.image_sub = rospy.Subscriber("/camera_1/image_raw", Image, self.callback)
 

  def callback(self,data):

    
    plt.close('all')
    bridge = CvBridge()

    try:
      cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
    except CvBridgeError as e:
      rospy.logerr(e)
    
    image = cv_image

    resized_image = cv2.resize(image, (640, 640)) 
    detected = model(resized_image)
    img_detected = np.squeeze(detected.render())


    ######################## DATA MOVEMENT ########################
  
    df = pd.DataFrame(detected.xyxy[0])
    xy = df.to_numpy()
    xy = xy.astype(int)

    ######################## CENTER OF MASS ########################

    x_center = []
    y_center = []

    for n in range(0,len(xy[:,0])):
        x_center.append(xy[n,0] + abs(int((xy[n,0] - xy[n,2])/2))) 
        y_center.append(xy[n,1] + abs(int((xy[n,1] - xy[n,3])/2))) 
        
        img_detected = cv2.circle(image,(x_center[n], y_center[n]), 5, (0,255,0), -1)

    x_center_all = int(np.mean(x_center))
    y_center_all = int(np.mean(y_center))

    img = cv2.circle(img_detected,(x_center_all, y_center_all), 8, (0,0,255), -1)

    ######################## PLOT TRAJECTORIES ########################
    fig1 = plt.figure()

    self.x_center_hst.append(x_center)
    self.y_center_hst.append(y_center)

    if len(self.x_center_hst) > 10:
      self.x_center_hst.pop(0)
      self.y_center_hst.pop(0)


    plt.scatter(self.x_center_hst,self.y_center_hst,linewidths=0.01)
    plt.xlim(0,640)
    plt.ylim(640,0)

    fig1.canvas.draw()
    trajectory = np.fromstring(fig1.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    trajectory  = trajectory.reshape(fig1.canvas.get_width_height()[::-1] + (3,))
    trajectory = cv2.cvtColor(trajectory,cv2.COLOR_RGB2BGR)
    cv2.imshow("plot",trajectory)

    ######################## PLOT HEATMAP ########################

    fig2 = plt.figure()
    heatmap, xedges, yedges = np.histogram2d(x_center, y_center, bins=50, range=[[0, 1280], [0, 960]])
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    

    plt.imshow(heatmap.T, extent=extent, origin='upper')

    fig2.canvas.draw()
    heatmap = np.fromstring(fig2.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    heatmap  = heatmap.reshape(fig2.canvas.get_width_height()[::-1] + (3,))
    heatmap = cv2.cvtColor(heatmap,cv2.COLOR_RGB2BGR)
    #cv2.imshow("Heatmap",heatmap)
    
    #################### Vel ####################
    x_positions = xy[:,0]
    y_positions = xy[:,1]

    pos_mag = np.sqrt(x_positions**2 + y_positions**2)
    dif_pos = abs(pos_mag - self.pos_mag_1)
    self.pos_mag_1 = pos_mag

    ad_time = data.header.stamp.secs
    dif_time = abs(ad_time - self.ad_time_change)

    self.ad_time_change = ad_time

    if dif_time!=0:
      self.vel = dif_pos/dif_time

    #################### TEXT VEL ####################  
    avg_vel = []  

    for n in range(0,len(xy[:,0])):
      self.vel_mag = np.round(self.vel*0.33,2)
      avg_vel.append(self.vel_mag)
      img = cv2.putText(
              img = img,
              text = f"v={str(self.vel_mag[n])}",
              org = (xy[n,2], xy[n,3]),
              fontFace = cv2.FONT_HERSHEY_DUPLEX,
              fontScale = 0.4,
              color = (125, 246, 55),
              thickness = 1
              )

    #################### AVG VEL ####################  

    avg_vel = np.round(np.mean(avg_vel),2)

    #################### TEXT AVG VEL ####################  

    img = cv2.putText(
            img = img,
            text = f"Av Vel ={str(avg_vel)}",
            org = (50, 50),
            fontFace = cv2.FONT_HERSHEY_DUPLEX,
            fontScale = 1,
            color = (125, 246, 55),
            thickness = 2
            )
    
    ########################  IMAGE ###########################

    cv2.imshow('Detector de Carros',img )
    cv2.waitKey(3)

        