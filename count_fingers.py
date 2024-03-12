import cv2
import mediapipe as mp
cap = cv2.VideoCapture(0)

mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils

hands=mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)

def draw_hand_landmarks(image,hand_landmarks):
    if hand_landmarks:
        for i in hand_landmarks:
            mp_drawing.draw_landmarks(image,i,mp_hands.HAND_CONNECTIONS)
            

tip_id=[4,8,12,16,20]

def count_fingers(image,hand_landmarks,hand_no=0):
    if hand_landmarks:
        landmarks=hand_landmarks[hand_no].landmark
        print(landmarks)
        fingers=[]
        
        for lm_index in tip_id:
            finger_tipy=landmarks[lm_index].y
            bottomy=landmarks[lm_index-2].y
            
            if lm_index != 4:
                
                if finger_tipy < bottomy:
                    fingers.append(1)
                    print("finger with id",lm_index,"is opened")
                    
                if finger_tipy > bottomy:
                    fingers.append(0)
                    print("finger with id",lm_index,"is closed")
                
        total_fingers=fingers.count(1)
        text=f'fingers:{total_fingers}'
        
        cv2.putText(image,text,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    
while True:
    
    success, image = cap.read()
    
    image=cv2.flip(image,1)
    results=hands.process(image)
    hand_landmarks=results.multi_hand_landmarks 
    draw_hand_landmarks(image,hand_landmarks)
    count_fingers(image,hand_landmarks)
    
    cv2.imshow("Media Controller", image)
    
    
    
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()

