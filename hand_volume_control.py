import cv2 as cv
import time
import numpy as np
import math
import hand_tracking_module as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def main ():

    def dist (x1, y1, x2, y2):
        sum1 = (x2 - x1)**2
        sum2 = (y2 - y1)**2
        d = (sum1 + sum2)**(1/2)

        return d

    wCam, hCam = 640, 480
    cTime = 0
    pTime = 0

    cap = cv.VideoCapture (0)
    detector = htm.handDetector()


    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    Range = volume.GetVolumeRange()

    minvol = Range [0]
    maxvol = Range [1]

    volBar = 0
    volum = 0

    cap.set (3, wCam)
    cap.set (4, hCam)

    while True:
        isTrue, frame = cap.read ()

        frame = detector.find_hands(frame)
        LmList = detector.findPosition (frame, draw = False)

        if len(LmList) != 0:

            x1, y1 = LmList[4][1], LmList[4][2]
            x2, y2 = LmList[8][1], LmList[8][2]
            cx, cy = (x1 + x2)//2, (y1 + y2)//2

            distance = dist(x1, y1, x2, y2)

            vol = np.interp (distance, [30, 180], [minvol, maxvol])
            volBar = (math.e**((vol+64.93473)/14.1) - 0.9777)
            volum = np.interp (volBar, [0, 100], [420, 160])

            volume.SetMasterVolumeLevel(vol, None)

            cv.circle (frame, (x1, y1), 5, (255,0,0), -1)
            cv.circle (frame, (x2, y2), 5, (255,0,0), -1)

            cv.line (frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            if distance < 30:
                cv.circle (frame, (cx, cy), 15, (0,0,255), -1)
            elif distance > 180:
                cv.circle (frame, (cx, cy), 15, (255,0,0), -1)
            else:
                cv.circle (frame, (cx, cy), 15, (255,0,100), -1)

        cv.rectangle (frame, (50,160), (70, 420), (0, 255, 0), 3)
        cv.rectangle (frame, (50,int(volum)), (70, 420), (0, 255, 0), -1)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv.putText(frame, str(int(volBar + 1)), (50,120), cv.FONT_HERSHEY_PLAIN, 2, (200,130,50), 2)
        cv.putText(frame, str(int(fps)), (10,50), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 2)

        cv.imshow ('image', frame)

        cv.waitKey (1)

main ()