import rospy as rp
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler

import math as m
import time
from nav_msgs.msg import Odometry
x=0
y=0

def move(speed):
    velocity_publisher=rp.Publisher("/cmd_vel",Twist,queue_size=10)
   

    velocity_message=Twist()
    global x,y
    x0=x
    y0=y
    velocity_message.linear.x=speed
    if speed>0:
        print("move forword")
    else:
        print("move backword")
    loop_rate=rp.Rate(1000)
 
    velocity_publisher.publish(velocity_message)
def rotate(angular_speed_degree):
    velocity_publisher=rp.Publisher("/cmd_vel",Twist,queue_size=10)
   
    velocity_message=Twist()
    angular_speed=m.radians(angular_speed_degree)
    
    velocity_message.angular.z=angular_speed
   
    
        
    velocity_publisher.publish(velocity_message)        
    print("rotate")
def go_to_goal(velocity_publisher,x_goal,y_goal):
    global x,y,yaw
    loop_rate=rp.Rate(100)
    velocity_message=Twist()

    while True:
        k_linear=0.6
        distance= abs(m.sqrt(((x_goal-x)**2)+((y_goal-y)**2)))

        linear_speed=distance*k_linear

        K_angular=0.5

        desire_angle_goal=m.atan2(y_goal-y,x_goal-x)
        angular_speed=(desire_angle_goal-yaw)*K_angular

        velocity_message.linear.x=linear_speed
        velocity_message.angular.z=angular_speed

        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        print('x = ',x ,', y = ',y,' , distance to goal = ',distance)
        if distance<0.01:
            break
def desire_orientation(velocity_publisher,speed_in_degree,desire_angle):
    relative_angle_radian=m.radians(desire_angle)-yaw
    if relative_angle_radian<0:
        clockwise=1
    else:
        clockwise=0
    print(relative_angle_radian  , desire_angle)
    rotate(velocity_publisher,speed_in_degree,m.degrees(relative_angle_radian),clockwise)
    
def posecallback(p):
    global x
    global y, yaw
    x=p.pose.pose.position.x
    y=p.pose.pose.position.y
    (roll, pitch, yaw) = euler_from_quaternion ([p.pose.pose.orientation.x,p.pose.pose.orientation.y,p.pose.pose.orientation.z,p.pose.pose.orientation.w])
   

if __name__=="__main__":
    
        rp.init_node('motion_pos',anonymous=False)
       
        #go_to_goal(velocity_publisher,1,5)
        # rotate(velocity_publisher,9.0,55,0)
        #rotate(15,0)

        #move(0.2)
        # #rotate(velocity_publisher,9.0,55,1)
        for i in range(20000):
            rotate(-10)
        # move(velocity_publisher,8.0,4.0,1)
        # go_to_goal(velocity_publisher,1.0,1.0)
        # desire_orientation(velocity_publisher,30,270)
        # go_to_goal(velocity_publisher,1.0,5.0)



 