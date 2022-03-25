import rospy as rp
from path_maker.srv import POINTRequest
from path_maker.srv import POINT
from path_maker.srv import POINTResponse
from  brama1 import points
po=[]
coun=0
def handle(data):
    global po,coun
    po.append([data.x,data.y])
    
    
    if len(po)>1:
        
       # print(coun)
        #print(pp)
        if coun==2:
            a_=po[0]
            b_=po[1]
        else:
            a_=po[len(po)-2]
            b_=po[len(po)-1]

        poi=points(a_,b_)
        x_=poi[0]
        y_=poi[1]
    else:
        x_=[po[0][0],]
        y_=[po[0][1],]
    return POINTResponse(x_ ,y_)



def add_two():
    rp.init_node("add_node")
    s=rp.Service("COSTUM",POINT,handle)
    print("ready to make path ")
    rp.spin()




if __name__=="__main__":
    add_two()
