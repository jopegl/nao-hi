import mediapipe as mp
import cv2
import os

def todos_dedos_levantados(hand_landmarks):
    lm = hand_landmarks.landmark
    if (lm[4].x < lm[2].x):
        return False
    if(lm[8].y > lm[6].y):
        return False
    if (lm[12].y > lm[10].y):
        return False
    if(lm[16].y > lm[14].y):
        return False
    if (lm[20].y > lm[18].y):
        return False
    
    return True

    

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)


cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            if(todos_dedos_levantados(hand_landmarks)):
                print('Todos os dedos levantados!')


    cv2.imshow('Camera', frame)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()