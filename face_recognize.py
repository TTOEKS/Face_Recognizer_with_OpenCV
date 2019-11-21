import cv2
import numpy as np
import os, glob
import time
import subprocess
import sys
import pymysql
from pygame import mixer


print('-------------------------------------------------------------------')
print('\t\t\t FACE RECOGNIZING')
print('-------------------------------------------------------------------')


# set values
base_dir = './'
min_accuracy = 79
rectangle_color = (0,255,255)
count = 0
pass_count = 25
conn = pymysql.connect(host='localhost',user='host',password='password', db='project',charset='UTF8')
curs = conn.cursor()
user_id = 'test123'
mixer.init()


user_id =  input('Insert ID: ')

query = 'SELECT * FROM users WHERE ID = %s'
curs.execute(query, user_id)
result = curs.fetchone()

# Check User ID
if result is None:
    print('Please insert correct ID')
    sys.exit()
else:
    print('Welcome %s !!'%(user_id))

mixer.music.load('./resource/face_contect.mp3')
mixer.music.play()
subprocess.call(['python','face_train.py', user_id])

face_classifier = cv2.CascadeClassifier('../../resource/data/haarcascade_frontalface_default.xml')

model = cv2.face.LBPHFaceRecognizer_create()
model.read(os.path.join(base_dir, user_id+'_face.xml'))


# Starting count time
start_time  = time.time()

# set camera captuer dev
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret , frame = cap.read()
    if not ret:
        print("no frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    #face Detecte
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for(x, y, w, h) in faces:
        # draw rectnagle 
        cv2.rectangle(frame, (x, y), (x+w, y+h), rectangle_color, 2)
        face = frame[y:y+h, x:x+w]
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        label, confidence = model.predict(face)
        if confidence < 400:
            accuracy = int(100 * (1 - confidence/400))
            if accuracy >= min_accuracy:
                msg = '%s(%.1f%%)'%("True", accuracy)
                rectangle_color = (0,255,0)
                count += 1
            else:
                msg = '%s(%.1f%%)'%("False", accuracy)
                rectangle_color = (0,0,255)

        # print user name and %
        text, base = cv2.getTextSize(msg, cv2.FONT_HERSHEY_PLAIN, 1, 3)
        cv2.rectangle(frame, (x, y-base-text[1]), (x+text[0], y+text[1]), rectangle_color, -1)
        cv2.putText(frame, msg, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 2, cv2.LINE_AA)
    
    cv2.putText(frame, "%.1f"%(time.time() - start_time),(20,35), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 1, cv2.LINE_AA) 
    cv2.imshow('Face Recognizer', frame)
    if cv2.waitKey(1) == 27:
        print('User Exit')
        break
    # Success Access
    if count > pass_count:
        mixer.music.load('./resource/access_success.mp3')
        print("Success Face recognizing!! Enjoy Driving!")
        mixer.music.play()
        break
    # Fail Access
    if time.time() - start_time > 8:
        # Fail Face recognizing during 5 sec
        mixer.music.load('./resource/access_fail.mp3')
        print("Fail Face recognizing!!  Please try Again!")
        mixer.music.play()
        break
time.sleep(5)
cap.release()
cv2.destroyAllWindows()
                







