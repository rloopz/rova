#!/usr/bin/env python3
import rospy
from visualization_msgs.msg import MarkerArray

def callback(marker_array):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", marker_array.markers)

if __name__ == '__main__':
    rospy.init_node('marker_subscriber', anonymous=True)
    marker_sub = rospy.Subscriber('visualization_marker_array', MarkerArray, callback)
    rospy.spin()

