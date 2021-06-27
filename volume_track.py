import cv2
import mediapipe as mp
import numpy as np
import time
import handmodule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

obj = htm.detecthand(detectc=0.7)

#we use pycaw to change volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
voulmeRange = volume.GetVolumeRange()#volume range is -65(min) to 0(max)
#volume.SetMasterVolumeLevel(-5.0, None)#sets the volume 0 is max and -65 is min
minvol = voulmeRange[0]
maxvol = voulmeRange[1]



wcap = 600
hcap = 600
cap = cv2.VideoCapture(0)

#setting the width and height of the frame
cap.set(3,wcap)
cap.set(4,hcap)
ptime =0
ctime =0
vol = 0
volBar = 400
while True:
    ret,frame = cap.read()
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    frame = obj.track(frame)

    lmlist = obj.findpos(frame,draw=False)
    #we should make sure there are some points
    if len(lmlist)!=0:
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        #finding their center
        cx,cy = (x1+x2)//2,(y1+y2)//2
        #CREATING CIRCLES AROUND OUR REQUIRED POINTS
        cv2.circle(frame,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(frame, (x2, y2),10, (255, 0, 255), cv2.FILLED)
        #marking the center point

        cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        #joining the two points
        cv2.line(frame,(x1,y1),(x2,y2),(255,0,255),1)
        # based on the length of line we will work so...we need to find the length
        length = math.hypot(x2-x1,y2-y1)
        #print(length)
        #our length rande is 300max and 50 min
        #our volume randge is -65 max and 0 min

        vol = np.interp(length,[50,300],[minvol,maxvol])#changes the range
        volBar = np.interp(length,[50,300], [400, 150])
        #now we print the length
        print(vol)
        #now we need to set volume accorfing to vol
        volume.SetMasterVolumeLevel(vol, None)
        #print(lmlist[4],lmlist[8])
        if length<50:
            #if the length is less tha 50 chage the color
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(frame,(50,150),(80,400),(0,255,0),3)
    #when my volume is 0 height should be 400 and for max vol height is 150
    cv2.rectangle(frame, (50, int(volBar)), (80, 400), (0, 255, 0), cv2.FILLED)
    #we actually need index 4 for thumb and 8 for index finger
    cv2.putText(frame,f'FPS:{int(fps)}',(30,50),cv2.FONT_HERSHEY_PLAIN,2,(150,255,120),3)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0XFF==27:
        break
cap.release()
cv2.destroyAllWindows()