import cv2 
from  sensor_msgs.msgs import Image
cap=cv2.VideoCapture(0)
print(cap.isOpened())
while (True):
    ret,frame=cap.read()
    cv2.imshow("frame",frame)
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()