#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MoveTurtle(Node):
    
    def __init__(self):
        super().__init__("move_turtle") #node name I chose
        self.get_logger().info("Move turtle node has been started.") #prints out a little something so we know it's working
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/cmd_vel", 10) #this creates a publisher of the type Twist (type, name, cue size)
        self.timer_ = self.create_timer(0.1, self.turtle_mvmt_command) #spits out whatever is in the callback every whatever seconds
        self.counter_ = -0.1 #initializing as -0.1 because in the turtle_mvmt_command I'm adding 0.1 seconds first
        self.msg_ = Twist()
        
    def turtle_mvmt_command(self):
        self.counter_ += 0.1
        
        # SCENARIO 1
        # if self.counter_ < 3.0: # Scenario 1: I want the turtle to move at 2 m/s for 3 sec for a total of 6 m
        #     self.msg_.linear.x = 2.0
        #     self.cmd_vel_pub_.publish(self.msg_)
        # elif self.counter_ >= 3.0: # Scenario 1: After 3 seconds it will stop
        #     self.msg_.linear.x = 0.0
        #     self.cmd_vel_pub_.publish(self.msg_)
        
        # SCENARIO 2
        if self.counter_ <= 4.0: # Scenario 2: Turtle will start accelerating in the -x direction for 4 seconds at 0.3 m/s^2 for a total of 2.4 m
            self.msg_.linear.x = -.3*(self.counter_)
            self.cmd_vel_pub_.publish(self.msg_)
        elif self.counter_ < 8.0: # Scenario 2: After 4 seconds of acceleration, turtle will switch to constant velocity of 1.5 m/s for 4 seconds for a total of 6 m
            self.msg_.linear.x = -1.5
            self.cmd_vel_pub_.publish(self.msg_)
        elif self.counter_ < 14.7: # Scenario 2: After 4 seconds of constant velocity, turtle will begin decelerating in +x direction for 6.7 seconds at 0.225 m/s^2 for 5 m from the starting constant velocity
            self.msg_.linear.x = .225*(self.counter_ - 8.0) - 1.5
            self.cmd_vel_pub_.publish(self.msg_)
        elif self.counter_ >= 14.7: # Scenario 2: At this point it will stop at -13.4 m in the space
            self.msg_.linear.x = 0.0
            self.cmd_vel_pub_.publish(self.msg_)
        

def main(args=None):
    rclpy.init(args=args) #initializes node
    node = MoveTurtle()
    rclpy.spin(node) #keeps node running until manual stop (CTRL+C)
    rclpy.shutdown() #kills node
    
if __name__ == '__main__':
    main()