#!/usr/bin/env python
import rospy
import tf
from std_msgs.msg import String, Header
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import sqrt, cos, sin, pi, atan2
import numpy
import sys

#from dynamic_reconfigure.server import Server
#from wall_following_assignment.cfg import DynamicHuskyConfig


class PID:
    def __init__(self, Kp, Kd, Ki, dt):
    	#initialize controller
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.curr_error = 0
        self.prev_error = 0
        self.sum_error  = 0
        self.curr_error_deriv = 0
        self.control = 0
        self.dt = dt
        
    def update_control(self, current_error, reset_prev=False):
        #update controller output
        self.prev_error 	  = self.curr_error
        self.curr_error 	  = current_error
        self.sum_error 		 += current_error
        self.curr_error_deriv = (current_error - self.prev_error)/self.dt
		
        self.control = self.Kp*current_error + self.Kd*self.curr_error_deriv + self.Ki*self.sum_error 
        
    def get_control(self):
    	#return controller output
        return self.control

    def change_parameters(self, Kp, Kd, Ki):
    	#update controller parameters
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki

class WallFollowerHusky:
    def __init__(self):
        rospy.init_node('wall_follower_husky', anonymous=True)
        #initialize parameters for the controller
        self.forward_speed = rospy.get_param("~forward_speed")
        self.desired_distance_from_wall = rospy.get_param("~desired_distance_from_wall")
        self.hz    = 50 
        self.Kp    =-2
        self.Kd    =-0
        self.Ki    =-0.01
        self.tao   = 0.8
        self.max_w = 1.3 
        dt= 1.0/self.hz
        self.forward_danger_zone= 1.5
        self.controller = PID(self.Kp,self.Kd,self.Ki,dt)

        #set-up publishers and subscribers
        self.error_pub  =  rospy.Publisher('/husky_1/cte', String, queue_size=10)
        self.cmd_pub    = rospy.Publisher('/husky_1/cmd_vel', Twist, queue_size=10)
        self.laser_sub  = rospy.Subscriber('/husky_1/scan', LaserScan,self.laser_scan_callback)

        #set-up the dynamic server
        #srv = Server(DynamicHuskyConfig, self.server_callback)

    def server_callback(self, config, level):
    	#update parameters from the server
	    self.Kp 	= config.Kp
	    self.Kd 	= config.Kd
	    self.Ki 	= config.Ki
	    self.max_w  = config.max_w
	    self.tao	= config.tao

	    #update the controller
	    self.controller.change_parameters(self.Kp, self.Kd, self.Ki)
	    return config
        
    def laser_scan_callback(self, msg):
    	#find the minimum distance,
    	#the error compared to the desired distance,
    	#and the index of the closest point

    	#note: I only look at the left side of the robot, an emergency brake system
    	#can be implemented in case of a close wall on the right
    	forward_ind	= len(msg.ranges)/2
    	min_dist 	= min(msg.ranges[0:forward_ind])
    	error 		= min_dist - self.desired_distance_from_wall
    	angle_index = msg.ranges[0:forward_ind].index(min_dist)

        #check the distance to the wall in front
        #if it is too close and there is no opening on the left it becomes the new reference point
        if((msg.ranges[forward_ind] - self.forward_danger_zone)<min_dist and not 
        	max(msg.ranges[angle_index:forward_ind])>5):

			min_dist    = msg.ranges[forward_ind]
			error       = min_dist - self.desired_distance_from_wall
			angle_index = forward_ind
        
        #compute the angle towards the reference point.
        #We want to move perpendicular to that direction.
        #compute are current angle compared to the perpendicular direction.
        #we try to approach the perpendicular direction at 
        #the right distance using an exponential trajectory with time constant tao.
        #the desired angle is the derivative of the trajectory at x=0
        min_angle      = msg.angle_min + msg.angle_increment*angle_index
        current_angle  = -(min_angle+pi/2)
        desired_angle  = atan2(-error,self.tao)
        angle_error    = desired_angle - current_angle

        #angle of 300 deg = - 60 deg
        if(angle_error>pi):
        	angle_error= angle_error-2*pi
        elif(angle_error<-pi):
        	angle_error= angle_error+2*pi

        #get the angular speed from the controller with angle error as input
        self.controller.update_control(angle_error)
        wz = self.controller.get_control()
        #limit max angular speed to avoid drifting in sharp corners
        wz =min(abs(wz),self.max_w)*numpy.sign(wz)

        #publish the desired angular speed and the cross-track error
        pub_msg = Twist()
        pub_msg.linear.x=self.forward_speed
        pub_msg.angular.z =wz
        self.cmd_pub.publish(pub_msg)
        self.error_pub.publish(str(error))
            
    def run(self):
    	rate = rospy.Rate(self.hz)
    	while not rospy.is_shutdown():
    		rate.sleep()

    
if __name__ == '__main__':
	wfh = WallFollowerHusky()
	wfh.run()

