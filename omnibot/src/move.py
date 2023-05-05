#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import TwistStamped
from random import uniform

rospy.init_node('omnibot_random_move')

cmd_vel_pub = rospy.Publisher('/cmd_vel', TwistStamped, queue_size=1)

while not rospy.is_shutdown():
    twist_msg = TwistStamped()
    twist_msg.header.stamp = rospy.Time.now()
    twist_msg.twist.linear.x = 5
    twist_msg.twist.angular.z = uniform(-5.0, 5.0)
    cmd_vel_pub.publish(twist_msg)
    rospy.sleep(1.0)

