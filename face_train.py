import pandas as pd
import base64
from sqlalchemy import create_engine
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import glob
import sys
import subprocess


print('-------------------------------------------------------------------')
print('\t\t\t FACE TRAINING')


engine = create_engine('mysql+mysqldb://host:password@localhost/project',echo=False)
img_df = pd.read_sql(sql="SELECT * FROM images WHERE ID = '"+ sys.argv[1] + "'", con=engine)

# Create Temp directory
subprocess.call(['mkdir','./.temp'])
base_dir = './.temp/'



for i in range(0,10):
    img_str = img_df['IMG_DATA'].values[i]
    print(type(img_str))

    img = base64.decodebytes(img_str)

    im = Image.open(BytesIO(img))
    im.save(base_dir + str(i) +'.jpeg')
    print("save Image file from Database:"+str(i)+".jpeg")

base_dir = './.temp/'
train_data, train_labels = [], []

print('\nCollecting train data who ID = '+sys.argv[1]+' set:')

# seperate name_id -> name
files = glob.glob(base_dir+'*.jpeg')
print("\t path:%s, %d image files"%(base_dir, len(files)))

for file in files:
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

    # save image data to train_data and save id data to labels
    train_data.append(np.asarray(img, dtype=np.uint8))
    train_labels.append(0)

# convert numpy array
train_data = np.asarray(train_data)
train_labels = np.int32(train_labels)

# create LBP face detector and training
print('Starting LBP Model Training....')
    
model = cv2.face.LBPHFaceRecognizer_create() 
model.train(train_data, train_labels)
model.write('./'+ sys.argv[1] +'_face.xml')
print('Model trained successfully!!')

subprocess.call(['rm','-rf','./.temp'])
print('-------------------------------------------------------------------')

