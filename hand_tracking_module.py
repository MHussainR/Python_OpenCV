import cv2 as cv
import mediapipe as mp
import time

class handDetector ():
    def __init__ (self, mode = False, max_hands = 2, detectionCon = 1, trackCon = 0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands (self, frame, draw = True):
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.result = self.hands.process (frame_rgb)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
        return frame


    def findPosition (self, frame, handNo=0, draw = True):
        LmList = []
        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                LmList.append ([id, cx, cy])
                if draw:
                    cv.circle (frame, (cx, cy), 10, (122, 123, 56), -1)

        return LmList


def main ():
    cTime = 0
    pTime = 0
    cap = cv.VideoCapture (0)
    detector = handDetector()

    while True:
        isTrue, frame = cap.read ()
        frame = detector.find_hands(frame)
        LmList = detector.findPosition (frame, draw = False)
        if len(LmList) != 0:
            print (LmList[4])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(frame, str(int(fps)), (10,50), cv.FONT_HERSHEY_COMPLEX, 2, (255,0,0), 2)
        cv.imshow ('video', frame)
        cv.waitKey(1)

if __name__ == '__main__':
    main ()