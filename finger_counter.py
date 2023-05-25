import cv2 as cv
import time
import os
import hand_tracking_module as htm

wCam, hCam = 640, 480

cap = cv.VideoCapture (0)

detector = htm.handDetector()

cTime = 0
pTime = 0

tipIds = [4, 8, 12, 16, 20]

action = 0
sm = 0
pnum = 1

cap.set (3, wCam)
cap.set (4, hCam)

while True:
    isTrue, frame = cap.read ()

    frame = detector.find_hands(frame)
    LmList = detector.findPosition (frame, draw = False)

    if len(LmList) != 0:

        fingers = []

        for Id in range (len(tipIds)):
            if Id == 0:
                if LmList[2][1] < LmList[1][1]:  #seedha haath
                    if  LmList[tipIds[Id]][1] < LmList[tipIds[Id]-1][1]:
                        fingers.append (1)
                    else:
                        fingers.append (0)
                else:  #Ulta haath
                    if  LmList[tipIds[Id]][1] > LmList[tipIds[Id]-1][1]:
                        fingers.append (1)
                    else:
                        fingers.append (0)
            elif Id != 0 and LmList[tipIds[Id]][2] < LmList[tipIds[Id]-2][2]:
                fingers.append (1)
            else:
                fingers.append (0)

    #     if fingers == [0, 1, 0, 0, 0] or fingers == [0, 0, 1, 0, 0] or fingers == [0, 0, 0, 1, 0] or fingers == [0, 0, 0, 0, 1]:
    #         action = 1
    #     elif fingers == [0, 1, 1, 0, 0] or fingers == [1, 1, 0, 0, 0]  or fingers == [0, 1, 1, 0, 0] or fingers == [0, 0, 1, 1, 0] or fingers == [0, 0, 0, 1, 1] or fingers == [1, 0, 0, 0, 1] or fingers == [0, 1, 0, 0, 1] or fingers == [0, 0, 1, 0, 1] or fingers == [0, 1, 0, 1, 0] or fingers == [1, 0, 1, 0, 0]:
    #         action = 2
    #     elif fingers == [0, 1, 1, 1, 0] or fingers == [1, 1, 1, 0, 0] or fingers == [0, 0, 1, 1, 1] or fingers == [1, 1, 0, 0, 1] or fingers == [1, 0, 0, 1, 1] or fingers == [1, 0, 1, 0, 1]:
    #         action = 3
    #     elif fingers == [0, 1, 1, 1, 1] or fingers == [1, 1, 1, 1, 0] or fingers == [1, 0, 1, 1, 1] or fingers == [1, 1, 0, 1, 1] or fingers == [1, 1, 1, 0, 1]:
    #         action = 4
    #     elif fingers == [1, 1, 1, 1, 1]:
    #         action = 5
    #     elif fingers == [0, 0, 0, 0, 0]:
    #         action = 0
    #     print (fingers)
    
    # if action == pnum:
    #     sm = sm
    # else:
    #     sm += action

    cv.putText(frame, str(action), (10,100), cv.FONT_HERSHEY_DUPLEX, 2, (255,0,0), 2)
    cv.putText(frame, str(sm), (10,200), cv.FONT_HERSHEY_DUPLEX, 2, (255,0,0), 2)        

    pnum = action

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(frame, str(int(fps)), (10,50), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 2)

    cv.imshow ('frame', frame)

    cv.waitKey(1)