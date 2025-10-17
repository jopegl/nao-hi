import mediapipe as mp
import cv2
import qi
import numpy as np
import time

session = qi.Session()


print("Sessão iniciada")

limite_polegar = 0.07

def todos_dedos_levantados(hand_landmarks):
    lm = hand_landmarks.landmark
    if abs(lm[4].x - lm[2].x) < limite_polegar:
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

print("Rodando")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

session.connect("tcp://169.254.51.192:9559")
print("Conectou")
cam_proxy = session.service('ALVideoDevice')
animation = session.service('ALBehaviorManager')
motion = session.service('ALMotion')


print("Pegou camera e mov")

def acenar():
    animation.runBehavior('animations/Stand/Gestures/Hey_2')

motion.wakeUp()

resolution = 2 
color_space = 11  
fps = 30
cooldown = 5
acenando = False
tempo_aceno = 0

camera_name = "cam_recog"
cam_id = 0  # 0=top, 1=bottom
capture = cam_proxy.subscribeCamera(camera_name, cam_id, resolution, color_space, fps)

hands = mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 2,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.5
)

while True:
    nao_image = cam_proxy.getImageRemote(capture)

    if nao_image is None:
        continue

    width = nao_image[0]
    height = nao_image[1]
    array = nao_image[6]  
    frame = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))
    print(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)


    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            if(todos_dedos_levantados(hand_landmarks) and not acenando and time.time()- tempo_aceno > cooldown):
                acenando = True
                tempo_aceno = time.time()
                acenar()
                print('Todos os dedos levantados!')
            elif time.time() - tempo_aceno < cooldown:
                print('Esperando para acenar...')
            else:
                print('Dedos não levantados')

    cv2.imshow('Camera', frame)

    acenando = False

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam_proxy.unsubscribe(capture)
cv2.destroyAllWindows()