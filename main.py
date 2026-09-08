import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0

screen_w, screen_h = pyautogui.size()

camera = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.6)
drawing_tool = mp.solutions.drawing_utils

LEFT_CLICK_DISTANCE = 75
RIGHT_CLICK_DISTANCE = 110
RING_CLICK_DISTANCE = 125

last_left_click_time = 0
last_right_click_time = 0
CLICK_COOLDOWN = 0.3 

is_dragging = False

while True:
    success, frame = camera.read()
    if not success:
        print("Camera not working!")
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_tool.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

            landmarks = hand.landmark

            thumb = np.array([int(landmarks[4].x * screen_w), int(landmarks[4].y * screen_h)])
            index = np.array([int(landmarks[8].x * screen_w), int(landmarks[8].y * screen_h)])
            middle = np.array([int(landmarks[12].x * screen_w), int(landmarks[12].y * screen_h)])
            ring = np.array([int(landmarks[16].x * screen_w), int(landmarks[16].y * screen_h)])

            pyautogui.moveTo(index[0], index[1])

            current_time = time.time()

            left_distance = np.linalg.norm(index - thumb)
            if left_distance < LEFT_CLICK_DISTANCE:
                if current_time - last_left_click_time > CLICK_COOLDOWN:
                    pyautogui.click()
                    last_left_click_time = current_time
                cv2.putText(frame, "LEFT CLICK!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            right_distance = np.linalg.norm(middle - thumb)
            if right_distance < RIGHT_CLICK_DISTANCE:
                if current_time - last_right_click_time > CLICK_COOLDOWN:
                    pyautogui.rightClick()
                    last_right_click_time = current_time
                cv2.putText(frame, "RIGHT CLICK!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            drag_distance = np.linalg.norm(ring - thumb)
            if drag_distance < RING_CLICK_DISTANCE:
                if not is_dragging:
                    pyautogui.mouseDown()
                    is_dragging = True
                cv2.putText(frame, "DRAGGING...", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False

    cv2.imshow("Virtual Mouse Window", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
