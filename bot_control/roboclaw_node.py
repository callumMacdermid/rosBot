#!/usr/bin/env python3
import rospy
from bot_control.roboclaw_3 import Roboclaw
from geometry_msgs.msg import Twist

roboclaw = Roboclaw("/dev/ttyACM0", 115200)

address = 0x80
PPM = 4000

def cmd_vel_callback(twist):
	linear_x = twist.linear.x
	angular_z = twist.angular.z

	v1 = linear_x + twist.angular.z *  0.3 / 2.0
	v2 = linear_x - twist.angular.z * 0.3 / 2.0

	m1 = int(v1 * PPM)
	m2 = int(v2 * PPM)

	if m1 == 0 and m2 == 0:
		roboclaw.SpeedM1M2(address, 0, 0)
	else:
		roboclaw.SpeedM1M2(address, m1, m2)


def roboclawControl():
	roboclaw.Open()
	rospy.init_node('roboclawControl', anonymous=True)
	rospy.Subscriber("cmd_vel", Twist, cmd_vel_callback)
	rospy.spin()

if __name__ == "__main__":
	roboclawControl()
