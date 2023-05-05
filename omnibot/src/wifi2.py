#!/usr/bin/env python3

import rospy
import socket

from std_msgs.msg import String

def talker():
    #pub = rospy.Publisher('chatter', String, queue_size=10)
    #rospy.init_node('listener', anonymous=True)
    #rate = rospy.Rate(10) # 10hz

    # Crear un socket de servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(1)

    while not rospy.is_shutdown():
        conn, addr = s.accept()
        data = conn.recv(1024)  # Leer datos del socket
        if data:
            rospy.loginfo(data)
           # pub.publish(data)
        conn.close()
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

