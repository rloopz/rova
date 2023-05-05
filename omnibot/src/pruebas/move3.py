#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState

def move_omnibot():
    # Initialize the ROS node
    rospy.init_node('move_omnibot', anonymous=True)

    # Create a publisher to the joint_states topic
    pub = rospy.Publisher('/joint_states', JointState, queue_size=10)

    # Set the loop rate
    rate = rospy.Rate(10) # 10 Hz

    # Create a JointState message
    joint_state = JointState()
    joint_state.name = ['joint_front_left', 'joint_front_right', 'joint_back_left']
    joint_state.position = [0, 0, 0] # initial joint positions

    # Move the robot in a circle
    while not rospy.is_shutdown():
        # Update the joint positions
        joint_state.position[0] += 0.01 # increment the position of the front left wheel joint
        joint_state.position[1] += 0.01 # increment the position of the front right wheel joint
        joint_state.position[2] += 0.01 # increment the position of the back left wheel joint

        # Publish the JointState message
        pub.publish(joint_state)

        # Sleep to maintain the loop rate
        rate.sleep()

if __name__ == '__main__':
    try:
        move_omnibot()
    except rospy.ROSInterruptException:
        pass

