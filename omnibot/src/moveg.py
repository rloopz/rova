#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from random import uniform

def move_robot(move):
    twist_msg = Twist()
    if move == 'f':
        twist_msg.linear.x = 1.0
    elif move == 'b':
        twist_msg.linear.x = -1.0
    elif move == 'r':
        twist_msg.angular.z = -1.0
    elif move == 'l':
        twist_msg.angular.z = 1.0
    cmd_vel_pub.publish(twist_msg)

def movee_callback(msg):
    moves = msg.data.split(',')
    for move in moves:
        move_robot(move)
        rospy.sleep(1.0)

if __name__ == '__main__':
    rospy.init_node('omnibot_movee')
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.Subscriber('/movee', String, movee_callback)
    rospy.spin()


