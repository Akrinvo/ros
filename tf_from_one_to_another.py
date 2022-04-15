
import rospy as rp
import tf
import tf2_ros
import tf2_geometry_msgs
def tf_tran(x,y):
   #

    tfbuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfbuffer)

    tf1_listener = tf.TransformListener()

    # give listeners time to receive required transforms
    rp.sleep(1.0)

    # make Pose in the 'b' frame
    p_b = tf2_geometry_msgs.tf2_geometry_msgs.PoseStamped()
    p_b.header.frame_id = 'laser_link'
    p_b.pose.position.x=x
    p_b.pose.position.y = y
   # p_b.pose.orientation.w = 1.0

    # Use tf2 to transform pose to the 'a' frame and print results. Best practice
    # would wrap this in a try-except:
    try:
        t_a_b = tfbuffer.lookup_transform('map', 'laser_link', rp.Time.now(), rp.Duration(1.0))
        p_a = tf2_geometry_msgs.do_transform_pose(p_b, t_a_b)
        #rp.loginfo("Pose expressed in 'frame_a' using tf2: \n%s\n", str(p_a))
       # print(p_a)
 
        
        return(p_a)
    except:
        return 0
if __name__=="__main__":
    rp.init_node("demo_lookup")
    a=tf_tran( 0.7519107738262867, -0.04611665986499371)#-1.1136521710882847, 0.4792564267840509
    print(a)