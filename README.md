# Face_Recognizer_with_OpenCV
-------------------------------------
My first project

***I wanted make a face recognizer using openCv in python.***

Here is function i made  
### 1. Face Collector.py
if you execute Face_Collector, this program will collecting 10 face image data  
This face Collector is also using at face Recognizer.py  


### 2. Face Training.py
first this program ask you your ID and password   
second it request 10 face image datas at Database  
third it create Training data file using your image data  

### 3. Face Recognizer.py

now program is recognize your face for 5 second  
if recognize over 25 frame in time admit your access  
else your access is deny  


if program admit your access, it will update your image data at database.
delete oldest image data and insert lastest image data

### 4. Start.py

Manage files
