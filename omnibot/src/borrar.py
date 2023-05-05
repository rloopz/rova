import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from random import uniform

def odom_callback(data):
    # do something with odometry data if needed
    pass

if __name__ == '__main__':
    rospy.init_node('random_move_robot')

    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('odom', Odometry, odom_callback)

    rate = rospy.Rate(5) # publish every 5 seconds

    while not rospy.is_shutdown():
        vel_cmd = Twist()
        vel_cmd.linear.x = uniform(-0.6, 0.6) # randomly choose x velocity between -0.6 and 0.6
        vel_cmd.linear.y = uniform(-0.6, 0.6) # randomly choose y velocity between -0.6 and 0.6
        vel_cmd.angular.z = uniform(-0.5, 0.5) # randomly choose yaw velocity between -0.5 and 0.5

        cmd_vel_pub.publish(vel_cmd)

        rate.sleep()

