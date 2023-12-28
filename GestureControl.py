import cv2
import mediapipe as mp
import numpy as np
import math

import HandTracking as ht 

import osascript

import time






cap=cv2.VideoCapture(0)
detector=ht.HandDetector()


result1 = osascript.osascript('get volume settings')
volInfo = result1[1].split(',')
outputVol = volInfo[0].replace('output volume:', '')
outputVol = int(outputVol)
pTime=0



result2=osascript.osascript('tell application "Music" to get player state')

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
        
def calculateAverageFingerDistance(lmList, cx, cy):
    distances = []
    for i in [4, 8, 12, 16, 20]:  # Index of fingertips in lmList
        x, y = lmList[i][1], lmList[i][2]
        distance = math.hypot(x - lmList[9][1], y - lmList[9][2])
        distances.append(distance)
    return sum(distances) / len(distances) if distances else 0

def AverageFingerDistancenothumb(lmList, cx, cy):
    distances = []
    for i in [8, 12, 16, 20]:  # Index of fingertips in lmList
        x, y = lmList[i][1], lmList[i][2]
        distance = math.hypot(x - lmList[9][1], y - lmList[9][2])
        distances.append(distance)
    return sum(distances) / len(distances) if distances else 0

def AverageFingerDistancenothumindex(lmList, cx, cy):
    distances = []
    for i in [12, 16, 20]:  # Index of fingertips in lmList
        x, y = lmList[i][1], lmList[i][2]
        distance = math.hypot(x - lmList[9][1], y - lmList[9][2])
        distances.append(distance)
    return sum(distances) / len(distances) if distances else 0

cooldown_duration = 1.5  # seconds
last_gesture_time = time.time()


while True:
    success, img=cap.read()
    img=cv2.flip(img,1)
    #cTime = time.time()
    #fps = 1 / (cTime - pTime)
    #pTime = cTime
    #cv2.putText(img, f'FPS: {str(int(fps))}', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(img, f'Volume: {int(outputVol)}', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    img=detector.findHands(img)
    resized_img = cv2.resize(img, (200,200))
    lmList=detector.findPosition(img, draw=False)
    hand_type = detector.detectHandType()
    if len(lmList) != 0:

        #print(lmList[4], lmList[8])
        x1, y1= lmList[4][1], lmList[4][2]
        x2, y2= lmList[8][1], lmList[8][2]
        cx,cy=(x1+x2)//2, (y1+y2)//2
        
        
        length=math.hypot(x2-x1, y2-y1) #hypotenuse, x2-x1 (delta x), y2-y1(delta y
        #print(length) #max lenth is 300 and min length is 50
        if hand_type == "Left":
            current_time = time.time()
            cv2.circle(img, (x1,y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (255, 0, 255), 3)
            #cv2.circle(img, (cx,cy), 15, (255, 0, 255), cv2.FILLED)
            if length<30:
                cv2.circle(img, (cx,cy), 15, (0, 255, 0), cv2.FILLED)
            #elif current_time - last_gesture_time > cooldown_duration:
                
            outputVol=np.interp(length, [50, 300], [0, 100])
            osascript.osascript(f'set volume output volume {outputVol}')
        
       # angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
       # if 45 <= angle <= 135:
       #         print("Thumb pointing to the right")
       # elif -135 <= angle <= -45:
       #     print("Thumb pointing to the left")
            
        avgdist=AverageFingerDistancenothumb(lmList, cx, cy)
        avgdist2=AverageFingerDistancenothumindex(lmList, cx, cy)
        #print(avgdist)
        #print(avgdist2)
        avg_distance = calculateAverageFingerDistance(lmList, cx, cy)
        #print(avg_distance)
        length0=math.hypot(lmList[4][1]-lmList[5][1], lmList[4][2]-lmList[5][2])
        #print(length0)
        length1=math.hypot(lmList[8][1]-lmList[9][1], lmList[8][2]-lmList[9][2])
        #print(length1)
        #length2=math.hypot(lmList[12][1]-lmList[9][1], lmList[12][2]-lmList[9][2])
        #length3=math.hypot(lmList[16][1]-lmList[9][1], lmList[16][2]-lmList[9][2])
        #length4=math.hypot(lmList[20][1]-lmList[9][1], lmList[20][2]-lmList[9][2])
        #print(length1, length2, length3, length4)
        if hand_type == "Right":
            current_time = time.time()
            if length0>120 and avgdist<80 and current_time - last_gesture_time > cooldown_duration:
                osascript.osascript('tell application "Music" to previous track')
                last_gesture_time = current_time
            elif length1>180 and avgdist2<80 and current_time - last_gesture_time > cooldown_duration:
                osascript.osascript('tell application "Music" to next track')
                last_gesture_time = current_time
            elif avg_distance < 80:
                osascript.osascript('tell application "Music" to pause')
            elif avg_distance > 165:
                osascript.osascript('tell application "Music" to play')     

               



            

        
        
            
            
# 8:70 12:40 16:70 20:95
            


    



    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the Esc key
        break
   


