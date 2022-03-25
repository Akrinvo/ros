#!/usr/bin/env python3
import matplotlib.pyplot as plt 
import math 
def points (p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    dis=math.sqrt(math.pow((x1-x0),2)+math.pow((y1-y0),2))
    
    x_=[x0]
    y_=[y0]
    dx = (x1-x0)
    dy = (y1-y0)
    if dx!=0:
        inc=abs(dx)/(dis/0.01)
        
    else: inc=0.01
    # print(x0,y0)
    if dx==0:
        
        while(y0<=y1):
            y0=y0+inc
            # print(x0,y0)
            x_.append(x0)
            y_.append(y0)
        while(y0>=y1):
            y0=y0-inc
            # print(x0,y0)
            x_.append(x0)
            y_.append(y0)

    if dx==0:
        
        while(x0<=x1) :
            x0=x0+inc
            
            # print(x0,y0)
            x_.append(x0)
            y_.append(y0)
        while(x0>=x1) :
            x0=x0-inc
            
            # print(x0,y0)
            x_.append(x0)
            y_.append(y0)
    if dx!=0:
        m=dy/dx
        c=y0-m*x0
        if dx>0 and dy>0:
            while(x0<=x1 ):
                x0=x0+inc
                y0=m*x0+c
                # print(x0,y0)
                x_.append(x0)
                y_.append(y0)
        else:
              
            while(x1<=x0 ):
                x0=x0-inc
                y0=m*x0+c
                # print(x0,y0)
                x_.append(x0)
                y_.append(y0)
            while(x1>=x0 ):
                x0=x0+inc
                y0=m*x0+c
                # print(x0,y0)
                x_.append(x0)
                y_.append(y0)
  
    # plt.plot(x_,y_)
    # plt.show()

  
    return(x_,y_)
       




if __name__=="__main__":
    
    print('enter the start point x1,y1 ')
    a=[float(x) for x in input().split()]
    print('enter the end point x2,y2 ')
    b=[float(x) for x in input().split()]
    points (a,b)
 