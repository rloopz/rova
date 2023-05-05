#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import Marker, MarkerArray
from interactive_markers.interactive_marker_server import InteractiveMarkerServer
from interactive_markers.menu_handler import MenuHandler
from geometry_msgs.msg import PoseStamped, Point
from std_msgs.msg import String
from visualization_msgs.msg import InteractiveMarker, InteractiveMarkerControl


def make_marker(x, y, id):
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.Time.now()
    marker.type = Marker.SPHERE
    marker.action = Marker.ADD
    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = 0
    marker.pose.orientation.x = 0
    marker.pose.orientation.y = 0
    marker.pose.orientation.z = 0
    marker.pose.orientation.w = 1
    marker.scale.x = 0.2
    marker.scale.y = 0.2
    marker.scale.z = 0.2
    if (x + y) % 2 == 0:
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
    else:
        marker.color.r = 0.5
        marker.color.g = 0.5
        marker.color.b = 0.5
    marker.color.a = 1.0

    return marker


def callback(msg):
    marker_id = int(msg.marker_name)
   # rospy.loginfo('Clicked marker ID: %d', marker_id)
    pub.publish(str(marker_id))


def make_marker_array():
    markers = MarkerArray()

    for i in range(6):
        for j in range(6):
            marker = make_marker(i + 1, j + 1, i * 6 + j)
            marker.id = i * 6 + j

            int_marker = InteractiveMarker()
            int_marker.header.frame_id = "map"
            int_marker.name = str(marker.id)
            int_marker.pose = marker.pose

            # create a control for the marker
            control = InteractiveMarkerControl()
            control.interaction_mode = InteractiveMarkerControl.BUTTON
            control.always_visible = True
            control.markers.append(marker)
            int_marker.controls.append(control)

            markers.markers.append(marker)
            server.insert(int_marker, callback)

    return markers


if __name__ == '__main__':
    rospy.init_node('marker_publisher', anonymous=True)
    pub = rospy.Publisher('clicked_node', String, queue_size=10)

    server = InteractiveMarkerServer("marker_server")
    marker_array = make_marker_array()
    server.applyChanges()

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        rate.sleep()

    server.clear()
    server.applyChanges()

