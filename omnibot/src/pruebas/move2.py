#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

# Variable global
vel_msg = Twist()
PI = 3.1415926535897

# def movimiento(data):
def movimiento(data):
    global vel_msg
    speed = 25 # grados por segundo

    vel_msg.linear.x = 1
    # vel_msg.angular.z = -abs(speed*2*PI/360)

    if data.range >= 1.8:
        vel_msg.linear.x = 0.1
        vel_msg.angular.z = 0
    else:
        vel_msg.linear.x = 0
        vel_msg.angular.z = -abs(speed*2*PI/360)

def move():
    rospy.init_node('robot_movement', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(100)

    rospy.Subscriber('/sensor/sonar_front', Range, movimiento)

    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass

