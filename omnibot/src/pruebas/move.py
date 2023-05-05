#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

global linear_vel
global angular_vel
linear_vel = 1 
angular_vel= 1
def move_robot(linear_vel, angular_vel):
    # Crear un objeto Twist con los valores de velocidad lineal y angular
    cmd_vel = Twist()
    cmd_vel.linear.x = linear_vel
    cmd_vel.angular.z = angular_vel

    # Crear un objeto ModelState con la posición y orientación actual del robot
    model_state = ModelState()
    model_state.model_name = 'omnibot'
    model_state.pose.position.x = 0
    model_state.pose.position.y = 0
    model_state.pose.position.z = 0
    model_state.pose.orientation.x = 0
    model_state.pose.orientation.y = 0
    model_state.pose.orientation.z = 0
    model_state.pose.orientation.w = 1

    # Publicar los comandos de velocidad en el tópico de ROS
    while not rospy.is_shutdown():
	    rospy.init_node('robot_movement', anonymous=True) 
	    #rospy.Publisher('/cmd_vel', Twist, queue_size=10).publish(cmd_vel)
	    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	    rate = rospy.Rate(100)
	    velocity_publisher.publish(linear_vel,angular_vel)
	    rate.sleep()

    # Enviar el estado del modelo al servicio de Gazebo para actualizar la posición y orientación del robot
    rospy.wait_for_service('/gazebo/set_model_state')
    try:
        set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        set_model_state(model_state)
    except rospy.ServiceException as e:
        rospy.loginfo("Fallo al enviar comando: %s" % e)
        
if __name__ == '__main__':
    try:
        move_robot(1,1)
    except rospy.ROSInterruptException:
    	pass
