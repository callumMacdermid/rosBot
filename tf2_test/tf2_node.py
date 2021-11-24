#!/usr/bin/env python

import rospy
import tf_conversions
import tf2_ros
from geometry_msgs.msg import Twist
import geometry_msgs.msg
import math

xPos = 0.0
yPos = 0.0
theta = 0.0

def twist_listener():
	rospy.init_node('teleop_tf', anonymous=True)
	rospy.Subscriber('cmd_vel', Twist, twist_callback)
	rospy.spin()

def twist_callback(twist):

	#Broadcaster Setup
	br = tf2_ros.TransformBroadcaster()
	t = geometry_msgs.msg.TransformStamped()
	
	#Twist Inputs
	vel = twist.linear.x
	dTheta = twist.angular.z
	
	global theta
	theta = theta + (0.1 * dTheta)

	if theta > (2*math.pi):
		theta = theta - (2*math.pi)
	elif theta < -(2*math.pi):
		theta = theta + (2*math.pi)

	#Pose Estimation Calculation
	dX = vel * math.cos(theta-dTheta)
	dY = vel * math.sin(theta-dTheta)

	global xPos 
	xPos = xPos + dX
	global yPos 
	yPos = yPos + dY	
	
	
	#Position Publish
	t.header.stamp = rospy.Time.now()
	t.header.frame_id = "world"
	t.child_frame_id = "robot"
	t.transform.translation.x = (0.01 * xPos)
	t.transform.translation.y = (0.01 * yPos)
	t.transform.translation.z = 0.0
	q = tf_conversions.transformations.quaternion_from_euler(0, 0, theta)
	t.transform.rotation.x = q[0]
	t.transform.rotation.y = q[1]
	t.transform.rotation.z = q[2]
	t.transform.rotation.w = q[3]

	br.sendTransform(t)
	
if __name__ == '__main__':
	twist_listener()
