
import rospy as rp 
from path_maker.srv import POINT
from path_maker.srv import POINTRequest
from path_maker.srv import POINTResponse
from geometry_msgs.msg import Point ,PointStamped,PoseStamped
from  nav_msgs.msg import Path


from rospy.timer import sleep
from visualization_msgs.msg import Marker
import sys


class Marker_basic:
    a=[]
    def __init__(self,ax=0,ay=0,index=0,co=0) :
        self.marker_objectlisher= rp.Publisher('/visualization_marker',Marker,queue_size=1)
        self.rate=rp.Rate(100)
        self.index=index
        self.ax=ax
        self.ay=ay
        self.co=co
        self.init_marker(z_val=0,ax=0)
        
    def init_marker(self,z_val=0,ay=0,ax=0):
        
        self.marker_object=Marker()
        self.marker_object.header.frame_id='/map'
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
       
        
        Marker_basic.a.append([my_point.x,my_point.y,my_point.z])
        
        
        path=Path()
  
        path.header.frame_id='/map'
        path.header.stamp=rp.get_rostime()
        
        for i in Marker_basic.a:
            bot_point=PoseStamped()
            bot_point.header.frame_id='/map'
            bot_point.header.stamp=rp.get_rostime()
            bot_point.pose.position.x=i[0]
            bot_point.pose.position.y=i[1]
            bot_point.pose.position.z=i[2]
            bot_point.pose.orientation.x=0.0
            bot_point.pose.orientation.y=0.0
            bot_point.pose.orientation.z=0.0
            bot_point.pose.orientation.w=1.0
            path.poses.append(bot_point)
            
            a_=Point()
            a_.x=i[0];a_.y=i[1];a_.z=i[2]
           
            self.marker_object.points.append(a_)
        # print(len(Marker_basic.a))
        pub.publish(path)
        
        
        
            # print(Marker_basic.a)
        #print(Marker_basic.a)
        self.marker_object.pose.orientation.x=0
        self.marker_object.pose.orientation.y=0
        self.marker_object.pose.orientation.z=1.0
        self.marker_object.scale.x=0.02
        self.marker_object.scale.y=0.02
        self.marker_object.scale.z=0.02


        self.marker_object.color.r=0.1
        self.marker_object.color.g=0.0
        self.marker_object.color.b=2.0
        self.marker_object.color.a=1.0


        self.marker_object.lifetime=rp.Duration(1000)
        
    
        
        self.marker_objectlisher.publish(self.marker_object)
        
        self.rate.sleep()



def add_two_client(a,b):
    rp.wait_for_service("COSTUM")
    try:
        path=rp.ServiceProxy("COSTUM",POINT)
        re=path(a,b)
        return (re.x_,re.y_)   
    except:
        pass


def clickdata(click_d):

    
    x11=click_d.point.x
    y11=click_d.point.y
    x_,y_=add_two_client(x11,y11)
    # path=Path()
    
    # path.header.frame_id='/map'
    # path.header.stamp=rp.get_rostime()
    f = open("path_data.txt","a")

    for j,k in zip(x_[:len(x_)-2],y_[:len(y_)-2]):
        
        f.write(str(j)+','+str(k)+'\n')
        m1=Marker_basic(ax=-j,ay=-k)
     
    f.close()
    
       
    
            
    
   
    
   
if __name__=="__main__":
    if __name__=='__main__':
        rp.init_node("marker_basic",anonymous=True)
       
        click=rp.Subscriber('/clicked_point',PointStamped,clickdata)
        pub=rp.Publisher('/r',Path,queue_size=10)
        rp.spin()
  

    

