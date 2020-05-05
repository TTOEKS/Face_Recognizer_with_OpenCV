import glob
import sys
import cv2
import threading
import pandas as pd
import base64
from PIL import Image
from sqlalchemy import create_engine
from io import BytesIO
from time import sleep


print('\n\n### Image Sending Module\nStart sending Images')
engine = create_engine('mysql+mysqldb://host:qwer@localhost/project', echo=False)
buffer = BytesIO()
cnt = 0
user_id = sys.argv[2]
img_data = []
thread_data = []

jpg_files = glob.glob('./.temp/*.jpeg')

img = cv2.imread(jpg_files[int(sys.argv[1])])
#img = cv2.cvtColor(face, cv2.COLOR_GRAY2RGB)
im = Image.fromarray(img)

im.save(buffer, format='jpeg')
img_str = base64.b64encode(buffer.getvalue())

img_df = pd.DataFrame({'ID': user_id,'IMG_DATA':[img_str]})
img_df.to_sql('images', con = engine, if_exists='append', index=False)
print(sys.argv[1] + ':  ## Success sending image to database')


