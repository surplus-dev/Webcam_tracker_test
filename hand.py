import cv2
import vmcp
import numpy as np
import mediapipe as mp
 
cap = cv2.VideoCapture(0)

hands = mp.solutions.hands.Hands(model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5)
 
while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue
 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
 
    color = np.zeros(image.shape, np.uint8)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                color,
                hand_landmarks,
                mp.solutions.hands.HAND_CONNECTIONS,
                mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                mp.solutions.drawing_styles.get_default_hand_connections_style()
            )
 
 
    cv2.imshow('test', cv2.flip(color, 1))
    if cv2.waitKey(5) & 0xFF == 27:
        break
 
cap.release()