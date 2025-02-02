import cv2
import numpy as np
import dlib
from imutils import face_utils
import serial
import time

s = serial.Serial('COM3', 9600)

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()    
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")   

sleep = 0
active = 0
status = ""
color = (0, 0, 0)
previous_status = ""  
start_sleep_time = None 

def compute(ptA, ptB):
    return np.linalg.norm(ptA - ptB)   #distance

def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)
    if ratio > 0.25:
        return 2
    elif 0.21 < ratio <= 0.25:
        return 1
    else:
        return 0

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    face_frame = frame.copy()
    
    for face in faces:
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)  # find
        landmarks = face_utils.shape_to_np(landmarks)  #convert 

        left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        if left_blink == 0 or right_blink == 0:
            sleep += 1
            active = 0
            if sleep > 6:
                status = "SLEEPING !!!"
                color = (255, 0, 0)
                #start
                if start_sleep_time is None:
                    start_sleep_time = time.time()
              
                elif time.time() - start_sleep_time >= 2:
                    if status != previous_status:
                        s.write(b'a')  
                        previous_status = status
        else:
            sleep = 0
            active += 1
            status = "Active :)"
            color = (0, 255, 0)
            if active > 6 and status != previous_status:
                s.write(b'b')  
                previous_status = status
            start_sleep_time = None    #reset

        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for (x, y) in landmarks:
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
s.close()
