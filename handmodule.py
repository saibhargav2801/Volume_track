import cv2
import mediapipe as mp



class detecthand():
    def __init__(self,mode=False,max=2,detectc=0.5,trackc=0.5):
        self.mode = mode
        self.max = max
        self.detectc = detectc
        self.trackc = trackc
        self.mpHands = mp.solutions.hands
        self.Hands = self.mpHands.Hands(self.mode,self.max,self.detectc,self.trackc)
        self.mpDraw = mp.solutions.drawing_utils

    def track(self,frame,draw=True):
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results = self.Hands.process(frame_rgb)
        if self.results.multi_hand_landmarks:
            for handlm in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(frame,handlm,self.mpHands.HAND_CONNECTIONS)
        return frame

    def findpos(self,frame,handno=0,draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id,lm in enumerate(myhand.landmark):
                h,w,c = frame.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),15,(255,0,255),2)
        return lmlist
def main():
    cap = cv2.VideoCapture(0)
    d = detecthand()
    while True:
        ret,frame = cap.read()
        frame = d.track(frame)
        lmlist = d.findpos(frame)
        if len(lmlist)!=0:
             print(lmlist[4])
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0XFF==27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()