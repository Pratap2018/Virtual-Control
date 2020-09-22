import numpy as np
import math 
import time
import cv2 
from imutils.video import VideoStream as vs #opencv videocap frame rate is less so imutils video
import pydirectinput # of nouse
from directkeys import PressKey,ReleaseKey,W,S,D,A,SPACE # For Key Press

#cap=cv2.VideoCapture(0)
#cv2.namedWindow('image')
vs = vs(src=0).start()
current_key_pressed=set()
def nothing():       #lamda call back for trackbar
    pass
""" cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)
cv2.createTrackbar('R2','image',0,255,nothing)
cv2.createTrackbar('G2','image',0,255,nothing)
cv2.createTrackbar('B2','image',0,255,nothing ) """
while True:
    keyPressed = False
    keyPressed_lr = False
    frame=vs.read()    
    frame1 = cv2.flip(frame,1) # i dont have webcam so i used droidcam that takes mirror image so i filpped 
    
    hsv_frame=cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV) # to hsv
    """ r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    r2 = cv2.getTrackbarPos('R2','image')
    g2 = cv2.getTrackbarPos('G2','image')
    b2 = cv2.getTrackbarPos('B2','image') """
   # s = cv2.getTrackbarPos(switch,'image')
    cv2.line(frame1,(320,0),(320,480),(0,255,0),1) # segmenting to left and right section by putting a line
    low_red=np.array([123,95,88]); # mask value min red
    
    high_red=np.array([255,255,255]) # mask max red
    mask=cv2.inRange(hsv_frame,low_red,high_red)
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)) # Changing morphology of the pixels 
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    
    mask=cv2.dilate(mask,kernel,iterations=4)
    mask=cv2.GaussianBlur(mask,(3,3),0)
    #anded=cv2.bitwise_and(frame1,frame1,mask=mask)
    #print(low_red,high_red)

    contours,h=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    try:
        for id, contour in enumerate(contours): 
            area = cv2.contourArea(contour)
            #print(area)
            if(area > 300  ): 
                x, y, w, h = cv2.boundingRect(contour)             
                imageFrame = cv2.rectangle(frame1, (x, y),(x + w, y + h),  (0, 255,0), 2)
                m1=cv2.moments(contours[0])
                m2=cv2.moments(contours[1])
                x=int(m1["m10"]/m1["m00"])
                y=int(m1["m01"]/m1["m00"])
                if(x>320): #detecting exact right cont
                    x2=x
                    y2=y
                else:   #detecting exact left cont
                    x1=x
                    y1=y
               
                x=int(m2["m10"]/m2["m00"])
                y=int(m2["m01"]/m2["m00"])
                if(x>320):
                    x2=x
                    y2=y
                else:
                    x1=x
                    y1=y
               
                
                slope=math.atan((y2-y1)/(x2/x1)) # getting the slope
                slope=round(slope,2)*100
                
                
                distance=math.sqrt(((x2-x1)**2) + ((y2-y1)**2)) # distance between two cont
                distance=round((distance/300)*200,2)
                cv2.line(frame1,(x1,y1),(x2,y2),(0,255,0),2)
               
                cv2.putText(frame1,"L",(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
                cv2.putText(frame1,"R",(x2,y2),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
               
                #print(slope)
                if slope<-150 :
                    """ pydirectinput.keyUp('s')
                    pydirectinput.keyUp('d')
                    pydirectinput.keyDown('a')
                    pydirectinput.keyDown('w')
                     """
                    #print(" <-- ")
                    PressKey(A)
                    keyPressed=True
                    keyPressed_lr=True
                    current_key_pressed.add(A)
                    
                elif slope>150 :
                    """ pydirectinput.keyUp('s')
                    pydirectinput.keyUp('a')
                    pydirectinput.keyDown('d')
                    pydirectinput.keyDown('w') """
                    #print(" --> ")
                    PressKey(D)
                    keyPressed=True
                    keyPressed_lr=True
                    current_key_pressed.add(D)
                if distance>160:    
                    """ pydirectinput.keyUp('s')
                    pydirectinput.keyUp('a')
                    pydirectinput.keyUp('d') """
                    #print(" ^ ")
                    PressKey(W)
                    keyPressed=True
                    
                    current_key_pressed.add(W)
                    
                elif distance <90:
                    """ pydirectinput.keyUp('s')
                    pydirectinput.keyUp('a')                    
                    pydirectinput.keyUp('w')
                    pydirectinput.keyDown('d') """   
                    #print("**")
                    PressKey(S)
                    keyPressed=True
                    
                    current_key_pressed.add(S)
                
             
                    
    except:
        pass

    if not keyPressed and len(current_key_pressed) != 0:
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()
    
    if not keyPressed_lr and ((A in current_key_pressed) or (D in current_key_pressed)):
        if A in current_key_pressed:
            ReleaseKey(A)
            current_key_pressed.remove(A)
        elif D in current_key_pressed:
            ReleaseKey(D)
            current_key_pressed.remove(D)

    #anded=cv2.bitwise_and(frame,frame,mask=mask)
    #cv2.imshow("hsv",mask)
    
    key=cv2.waitKey(1) & 0xFF
    cv2.imshow("color",frame1)
    if key==27:
        break