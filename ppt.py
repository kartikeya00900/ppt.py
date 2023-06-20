import subprocess
import speech_recognition as sr
import cv2
import mediapipe as mp
import pyautogui
import time

listener = sr.Recognizer()
powerpoint_path = r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"


subprocess.Popen([powerpoint_path])


def count_fingers(lst):
    cnt = 0
    thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2

    if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
        cnt += 1

    return cnt


cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands.Hands(max_num_hands=1)

prev = -1
start_time = time.time()

while True:
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    res = hands.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
        hand_keyPoints = res.multi_hand_landmarks[0]

        cnt = count_fingers(hand_keyPoints)

        if not (prev == cnt):
            if (time.time() - start_time) > 0.2:
                if cnt == 1:
                    pyautogui.press("right")
                elif cnt == 2:
                    pyautogui.press("left")

                start_time = time.time()
                prev = cnt

        drawing.draw_landmarks(frm, hand_keyPoints, mp.solutions.hands.HAND_CONNECTIONS)

    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break



