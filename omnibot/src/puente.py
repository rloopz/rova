#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

last_node_number = -1

def clicked_node_callback(msg):
    global last_node_number
    node_number = int(msg.data)

    node_map = {
        30: 1,
        31: 2,
        32: 3,
        33: 4,
        34: 5,
        35: 6,
        24: 7,
        25: 8,
        26: 9,
        27: 10,
        28: 11,
        29: 12,
        18: 13,
        19: 14,
        20: 15,
        21: 16,
        22: 17,
        23: 18,
        12: 19,
        13: 20,
        14: 21,
        15: 22,
        16: 23,
        17: 24,
        6: 25,
        7: 26,
        8: 27,
        9: 28,
        10: 29,
        11: 30,
        0: 31,
        1: 32,
        2: 33,
        3: 34,
        4: 35,
        5: 36
    }

    if node_number in node_map:
        new_node_number = node_map[node_number]
        if new_node_number != last_node_number:
      #      rospy.loginfo("Clicked node ID: %d", new_node_number)
            last_node_number = new_node_number
            publisher.publish(str(new_node_number))
    else:
        rospy.loginfo("Invalid node number")

def main():
    global publisher
    rospy.init_node('puente', anonymous=True)
    rospy.Subscriber("clicked_node", String, clicked_node_callback, queue_size=1)
    publisher = rospy.Publisher('node_number', String, queue_size=1)

    rospy.spin()

if __name__ == '__main__':
    main()

