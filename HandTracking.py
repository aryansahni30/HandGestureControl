import cv2
import mediapipe as mp
import time



class HandDetector():
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):  # constructor
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
      
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):  # finding the hands
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converting the image to RGB
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
      
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):  # id is the index number of the landmark
                h, w, c = img.shape  # height, width, channel
                cx, cy = int(lm.x * w), int(lm.y * h)  # center x, center y
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
        return lmList

    def detectHandType(self):
        if self.results.multi_hand_landmarks:
            handLandmarks = self.results.multi_hand_landmarks[0]  # Assuming we are dealing with the first detected hand

            wrist_x, wrist_y = handLandmarks.landmark[0].x, handLandmarks.landmark[0].y
            middle_finger_x, middle_finger_y = handLandmarks.landmark[9].x, handLandmarks.landmark[9].y

            # Calculate the direction vector from the wrist to the middle finger
            direction_vector = [middle_finger_x - wrist_x, middle_finger_y - wrist_y]

            # Assuming that if the direction vector points to the left, it's a left hand; otherwise, it's a right hand
            if direction_vector[0] < 0:
                return "Right"
            else:
                return "Left"
        else:
            return None




def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    pTime = 0
    cTime = 0

    
    while True:
        success, img = cap.read()  # reading the image
        #img=cv2.flip(img,1)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        img=detector.findHands(img)
        lmList=detector.findPosition(img)
        #if len(lmList) != 0:
            #print(lmList[4])
        
        hand_type = detector.detectHandType()
        if hand_type:
            print(f"{hand_type} Hand Detected")

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the Esc key
            break





if __name__ == "__main__":
    main()