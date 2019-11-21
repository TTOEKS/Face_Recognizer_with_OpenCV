import cv2
import subprocess
import numpy as np
import sys
import pandas as pd
import base64
from PIL import Image
from sqlalchemy import create_engine
from io import BytesIO
import pymysql


# set values
target_cnt = 10            # how many save image
engine = create_engine('mysql+mysqldb://host:password@localhost/project', echo=False)
conn = pymysql.connect(host='localhost',user='host',password='passwd', db='project',charset='UTF8')
curs = conn.cursor()
buffer = BytesIO()
face_data = []
user_id = 'test123'

# create face recognizer
face_classifier = cv2.CascadeClassifier('../../resource/data/haarcascade_frontalface_default.xml')


print('-------------------------------------------------------------------')
print('\t\t\t FACE COLLECTING')
print('-------------------------------------------------------------------')


# EditText user name, idx
user_id    = input('Insert User ID : ')

query = 'SELECT * FROM users WHERE ID = %s'
curs.execute(query, user_id)
result = curs.fetchone()

# Check User ID
if result is None:
    print('Please insert correct ID')
    sys.exit()
else:
    print('Welcome %s !!'%(user_id))


# create counting images columns in databsase
count_df = pd.read_sql(sql="SELECT COUNT(*) FROM images WHERE ID = '"+user_id+"'", con=engine)
count = int(count_df['COUNT(*)'])

print('count = ',  count)

# Update Oldest Image datas
if count == 10:

    query = 'DELETE FROM images WHERE ID = %s ORDER BY IMG_NUM ASC LIMIT 1'
    curs = conn.cursor()
    curs.execute(query, user_id)

    conn.commit()
    conn.close()
    count -= 1

    print('success Delete oldest data!!')


# make temp directory for save temp images
subprocess.call(['mkdir','./.temp'])

# Camera Capture
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        img = frame.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        # Face Detecting
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 1:
            (x, y, w, h) = faces[0]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)
            
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200,200))
            
            face_data.append(face)
            cv2.putText(frame, str(count), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            
            count += 1

        else:   # failed face detect or over 1
            if len(faces) == 0:
                msg = 'no face.'
            elif len(faces) > 1:
                msg = 'only one people can stay front camera'
            cv2.putText(frame, msg, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255))
        
        cv2.imshow('face_record', frame)
        if cv2.waitKey(1) == 27 or count == target_cnt:
            break

cap.release()
cv2.destroyAllWindows()

print('Success Collect Face Data')
cnt = 0
for img_files in face_data:
    cv2.imwrite('./.temp/' + str(cnt) + '.jpeg',img_files)
    cnt += 1 

for i in range(cnt):
    subprocess.call(['python','send_img_to_database.py', str(i), user_id])

print('Collectng Samples Completed')
subprocess.call(['rm','-rf','./.temp'])
