#!/usr/bin/env python3.8
#!/usr/bin/env python3.8
import rospy as rp
from sensor_msgs.msg import LaserScan
import math
from tf import TransformListener

from geometry_msgs.msg import  PointStamped
import rospy as rp
from rospy.timer import sleep
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point ,PointStamped

from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Pose
from tf_from_one_to_another import tf_tran
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist

from  robot_movment import move,rotate

import random 
Data_range=[]
Data_inten=[]
roll=0
pitch=0
yaw=0
i=0
a11=[]

point11=[]
Len=0
tr_x=0
tr_y=0

# Test Case

class tf_map_base_link:

    def __init__(self):
        self.tf = TransformListener()
        self.sub = rp.Subscriber("/tf", PointStamped, self.some_method)
        # rospy.Subscriber("/map", TransformStamped, )
        # ...

    def some_method(self, PointStamped):
        global tr_x,tr_y,roll,pitch,yaw
       
        try:
            (position, quaternion) = self.tf.lookupTransform("/laser_link", "/map",rp.Time(0))
            #
            (roll, pitch, yaw) = euler_from_quaternion (quaternion)
            #print(roll,pitch,yaw)
            tr_x=position[0]
            tr_y=position[1]
        except:
            pass
        
class Marker_basic:
    a=[]
    def __init__(self,ax=0,ay=0,index=0,co=0) :
        self.marker_objectlisher= rp.Publisher('/visualization_marker',Marker,queue_size=1)
        #self.rate=rp.Rate(100)
        self.index=index
        self.ax=ax
        self.ay=ay
        self.co=co
        self.init_marker(z_val=0,ax=0)
        
    def init_marker(self,z_val=0,ay=0,ax=0):
        
        self.marker_object=Marker()
        self.marker_object.header.frame_id='odom'
        self.marker_object.header.stamp=rp.get_rostime()
        self.marker_object.ns ='some_robot'
        self.marker_object.id=self.index
        self.marker_object.type=Marker.SPHERE_LIST
        self.marker_object.action=Marker.ADD

        my_point=Point()
       
        my_point.z=z_val
        

        if self.ax==0:
           my_point.x=ax
           my_point.y=ay
        else: my_point.x=self.ax
        my_point.y=self.ay
        if len(Marker_basic.a)>3:
            Marker_basic.a=[]
        
        Marker_basic.a.append([my_point.x,my_point.y,my_point.z])
        

        
        

        for i in Marker_basic.a:
            a_=Point()
            a_.x=i[0];a_.y=i[1];a_.z=i[2]
            
            self.marker_object.points.append(a_)
        #self.marker_object.points.append(my_point)
        
            #print(Marker_basic.a)
        #print(Marker_basic.a)
        self.marker_object.pose.orientation.x=0
        self.marker_object.pose.orientation.y=0
        self.marker_object.pose.orientation.z=1.0
        self.marker_object.scale.x=0.5
        self.marker_object.scale.y=0.5
        self.marker_object.scale.z=0.5


        self.marker_object.color.r=0.1
        self.marker_object.color.g=0.0
        self.marker_object.color.b=2.0
        self.marker_object.color.a=1.0


        self.marker_object.lifetime=rp.Duration(1000)
        
    
        
        self.marker_objectlisher.publish(self.marker_object)
        
      #  self.rate.sleep()

counter=0

goal_status=0

def movebase_client(x,y):
    global goal_status
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rp.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y= y
    goal.target_pose.pose.position.z=0
    goal.target_pose.pose.orientation.x=0
    goal.target_pose.pose.orientation.y=0
    goal.target_pose.pose.orientation.z=-0.697
    goal.target_pose.pose.orientation.w = 0.716

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rp.logerr("Action server not available!")
        rp.signal_shutdown("Action server not available!")
    else:
        goal_status=1
        return client.get_result()


x_cord_mid_point=0
y_cord_mid_point=0
move_sta=0
def stop_bot():
    global move_sta
    rate = rp.Rate(10)
    velocity_publisher=rp.Publisher("/cmd_vel",Twist,queue_size=1)
    v=Twist()
    v.linear.x=0
    v.linear.y=0
    v.linear.z=0
    v.angular.x=0
    v.angular.y=0
    v.angular.z=0
    now = rp.Time.now()
    rate = rp.Rate(100)


    while rp.Time.now() < now + rp.Duration.from_sec(2):
        velocity_publisher.publish(v)
        rate.sleep() 

   
    move_sta=1
a14=[]
point_check=0
check_speed=0
def cmd_status(data):
    global check_speed
    if data.linear.x==0 and data.angular.z==0:
        check_speed=1
    else:
        if point_check==0:
           stop_bot()

def robot_dock(start_point,mid_point,end_point,ang_inc):
        global dock_point,forw,rot

        df=start_point[3]-end_point[3]
        if dock_point==0:
            if forw==0:
                if rot==0:
                    if (mid_point*ang_inc)*(180/math.pi)<180 or df>0.0009:
                        rotate(0.5,1)
                    

                        if mid_point==360 or df<0.0009:
                            rotate(0,0)
                        

                    elif (mid_point*ang_inc)*(180/math.pi)>180 or df>-0.0009:
                        rotate(0.5,0)
                        
                        if mid_point==360 or df<-0.0009:
                            rotate(0,0)
                            
                    if (mid_point*ang_inc)*(180/math.pi)==180 or mid_point==360 :
                        rotate(0,0)
                        rot=1
                        
                
                if rot==1:
                    move(-0.1)
                    rot=0
                else:
                    move(0)
            
                if (mid_point*ang_inc)*(180/math.pi)==180 or (mid_point==360 and Data_range[mid_point]<0.4 and (df<0.0009 or df<-0.0009)):
                    move(0)
                    rotate(0,0)
                    forw=1
                    rot=0

            if forw==1:
                
                if rot==0:
                    if (mid_point*ang_inc)*(180/math.pi)<180 or df>0.0009:
                        rotate(0.5,1)
                    

                        if mid_point==360 or df<0.0009:
                            rotate(0,0)
                        

                    elif (mid_point*ang_inc)*(180/math.pi)>180 or df>-0.0009:
                        rotate(0.5,0)
                        
                        if mid_point==360 or df<-0.0009:
                            rotate(0,0)
                            
                    if (mid_point*ang_inc)*(180/math.pi)==180 or( mid_point==360 and (df<0.0009 or df<-0.0009) ):
                        rotate(0,0)
                        rot=1


def cmd_sub():
	rp.Subscriber("/cmd_vel", Twist,cmd_status)

a12=[]
a13=[]	
dock_point=0
rot=0
forw=0
entri=0
def angle_error(mid_point,ang_inc):
   # print(180-(mid_point*ang_inc)*(180/math.pi))
    return(180-(mid_point*ang_inc)*(180/math.pi))
df=0
def error_point(star,endd,mid_point):
    global df
    endd=0
    star=0
    
    df=star-endd

    return(0-df)
def error_dis(mid_point):
    global Data_range
    return(0.25-Data_range[mid_point])
pvt=0
p=20#10#20#40#0.5
p1=0.7
kp=5
rotation=0
di=0
diss=0
ki=35#17.5#35#70
import time 
def PID(start_point,mid_point,end_point,ang_inc):
    global Data_range,pvt,entri,p,ki,entri,rotation,diss
    curt=time.time()
    dlt=(curt-pvt)/1000000000
    pvt=curt
    entri=entri+angle_error(mid_point,ang_inc)*dlt
    rotation=angle_error(mid_point,ang_inc)*p +entri*ki
    if rotation>360:
        rotation=360
        entri=entri-angle_error(mid_point,ang_inc)*dlt
    if rotation<-360:
        rotation=-360
        entri=0

        

    
    return -rotation
 
def pid_dis_two(start,endd,mid_point):
    global Data_range,pvt,entri,p,kp,entri,diss
    diss=error_point(star,endd,mid_point)*kp
    return -diss

def pid_distance(mid_point):
    global Data_range,di,p1
    di=error_dis(mid_point)*p1
    return di


endd=0
star=0
ce=0
pidd=0
def laser_int(data):
    global diss,endd,star,Data_range,ce,Data_inten,pidd,x_cord_mid_point,y_cord_mid_point,point_check,a12,counter,a13,a14,dock_point,rot,forw,rotation
    Data_inten=data.intensities
    Data_range=data.ranges
    ang_inc=data.angle_increment
    
    intensity1=[]
    intensity2=[]
    # print(len(Data_inten),len(Data_range))
    t=0
    index=0
    f=0
    for i in range(len(Data_inten)):
        
        if t==0:
            if Data_inten[i] >0.5:
                intensity1.append([i,(i*ang_inc)*(180/math.pi),Data_inten[i],Data_range[i]])
            else: 
             if len(intensity1)==0 or len(intensity2)!=0: t=0
             else: t=1
        if t==1:
            
            if Data_inten[i] >0.5:
                if f==0:
                    index=intensity1[-1][0]
                    f=1
                intensity2.append([i,(i*ang_inc)*(180/math.pi),Data_inten[i],Data_range[i]])
            else:
                if len(intensity2)==0:
                    t=1
                else:t=0

    # print("intensity1    ",intensity1)
    # print("                                                       ")
    # print("intensity2    ",intensity2)
    ang=0
    try:
        if abs(intensity1[0][0]-intensity2[0][0])>600:
            
            if abs(intensity1[-1][0]-intensity2[-1][0])<600:
                start_point=intensity2[-1]
                end_point=intensity1[index+1]
            else:
                ang=1
                start_point=intensity2[-1]
                end_point=intensity1[0]

        else:
            if abs(intensity1[-1][0]-intensity2[-1][0])>600:
                start_point=intensity1[index]
                end_point=intensity2[0]
            else:
                start_point=intensity1[-1]
                end_point=intensity2[0]
       
        if ang==1:
            angle_btw_point=(360+end_point[1])-start_point[1]
            mid_point=(((719+end_point[0])-start_point[0])//2)+start_point[0]
            if mid_point>719:
                mid_point=mid_point-719
        else:
            angle_btw_point=(end_point[1])-start_point[1]
            mid_point=((end_point[0]-start_point[0])//2)+start_point[0]

        if start_point[0]>mid_point:
            endd=start_point[3]
            star=end_point[3]
        else:
            endd=end_point[3]
            star=start_point[3]
      
        tran= 0#-0.2735
        x_cord_mid_point=(Data_range[mid_point])*math.cos(mid_point*ang_inc)
        y_cord_mid_point=(Data_range[mid_point])*math.sin(mid_point*ang_inc)
        
       

    
 
        x_cord_mid_point1=(Data_range[mid_point]-1.5)*math.cos(mid_point*ang_inc)
        y_cord_mid_point1=(Data_range[mid_point]-1.5)*math.sin(mid_point*ang_inc)
        
        x_cord_mid_point2=(Data_range[mid_point]-2)*math.cos(mid_point*ang_inc)
        y_cord_mid_point2=(Data_range[mid_point]-2)*math.sin(mid_point*ang_inc)

     

        #T=tf_map_base_link()
    
        
        # TF2=tf_tran(x_cord_mid_point,y_cord_mid_point)
        # print(TF2)
        # ax1=-TF2.pose.position.x
        # ay1=-TF2.pose.position.y
        global tr_x,tr_y,point11,yaw,a11
        if len(point11)<2:
            point11.append([x_cord_mid_point,y_cord_mid_point])
            print(x_cord_mid_point,y_cord_mid_point)

        
        
        for i in point11:
            if len(a11)==0:
                TF2=tf_tran(x_cord_mid_point,y_cord_mid_point)
                print(TF2)
                ax1=-TF2.pose.position.x
                ay1=-TF2.pose.position.y
                a11=[ax1,ay1]
        
       # m1=Marker_basic(ax=a11[0],ay=a11[1])
        if point_check==0 and len(a12)==0:
                print("i am still call")
                cmd_sub()
                
        
        if len(a11)==2:
            

            if check_speed==1:
                if point_check==0:
                    stop_bot()
                    print(x_cord_mid_point2,y_cord_mid_point2)
                    TF2=tf_tran(x_cord_mid_point2,y_cord_mid_point2)
                    print(TF2)
                    ax1=-TF2.pose.position.x
                    ay1=-TF2.pose.position.y
                    a12=[ax1,ay1]
                    point_check=1
                    print("11111111111111111111111111111111111111111111", a12[0],a12[1])


       # m2=Marker_basic(ax=a12[0],ay=a12[1])
       # m2=Marker_basic(ax=a12[0],ay=a12[1]+1.5)
        if goal_status==0:
                 result = movebase_client(-a12[0],-a12[1])
                 

        
        if goal_status==1:
            counter+=1
        if counter>880 and counter<882:
            print(x_cord_mid_point,y_cord_mid_point,"    " ,counter)

            print(x_cord_mid_point,y_cord_mid_point)
            TF2=tf_tran(x_cord_mid_point,y_cord_mid_point)
            print(TF2)
            ax1=-TF2.pose.position.x
            ay1=-TF2.pose.position.y
            # print(x_cord_mid_point,y_cord_mid_point,"    " ,counter)
            print("2222222222222222222222222222222222222222222")
            print(x_cord_mid_point1,y_cord_mid_point1)
            TF2=tf_tran(x_cord_mid_point1,y_cord_mid_point1)
            print(TF2)
            ax2=-TF2.pose.position.x
            ay2=-TF2.pose.position.y
            
            dx=abs(ax1-ax1)
            dy=abs(ay1-ay2)
            if dx>0.6:
                ay2=ay1
            if dy>0.6:
                ax2=ax1
            a14=[ax2,ay2]
            a13=[ax1,ay1]
            
            result = movebase_client(-a14[0],-a14[1])
       # print(x_cord_mid_point,y_cord_mid_point,"    " ,counter,"  ",x_cord_mid_point1,y_cord_mid_point1)
        
        m2=Marker_basic(ax=a13[0],ay=a13[1])
        m2=Marker_basic(ax=a14[0],ay=a14[1])

        if ce==0:
            if pidd==0:                
                rotate(PID(star,mid_point,endd,ang_inc))

                move(0)

           # print(start_point[3]," ",rotation," ",diss," ",end_point[3],"  ",(mid_point*ang_inc)*(180/math.pi),"  ",mid_point," ",Data_range[mid_point])
            
            if (mid_point<361 and  mid_point >359)and Data_range[mid_point]>0.30:
                pidd=1  
                move(pid_distance(mid_point))
                

               
            else:
                pidd=0
                move(0)
            if (mid_point>359 and mid_point<361) and Data_range[mid_point]<0.30 :
                print("hiiii")
                pidd=1
                rotate(0)
                move(0)
               
                # rotate(pid_dis_two(start_point,end_point,mid_point))
            
            if (mid_point>=359 and mid_point<=361) and Data_range[mid_point]<0.30 :#and star-endd<0.001 and star-endd>-0.001:
                print(222222222222)
                rotate(0)
                move(0)
                ce=1
        
        print(star," ",rotation," ",diss," ",endd,"  ",(mid_point*ang_inc)*(180/math.pi),"  ",mid_point," ",Data_range[mid_point])
        
        
        # robot_dock(start_point,mid_point,end_point,ang_inc)
    
        
    except:
        pass  
    
    



   
    return(0)
 
    
def laser_sub():
   
    
    rp.Subscriber("scan",LaserScan,laser_int)
    print("hello")
    rp.spin()


if __name__=="__main__":
    rp.init_node("intensity")
    rp.loginfo("Starting ")
    laser_sub()

           
