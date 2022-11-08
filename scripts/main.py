#!/usr/bin/env python3.8
import rospy
import cv2
import numpy as np 

from camera_read import camera_1


def main():
	
	camera_1()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		rospy.loginfo("Shutting down")
	
	cv2.destroyAllWindows()

if __name__ == '__main__':
	
	rospy.init_node('camera_read', anonymous=False)
	main()

	

	# create and show mainWindow
	
	#sys.exit(app.exec_())

	
	
	
