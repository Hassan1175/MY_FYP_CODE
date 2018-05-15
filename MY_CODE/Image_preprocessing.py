#in that file i made the editing of all of pics.. which i used in project.. mean preprocessing
import skimage
import cv2
import dlib
import numpy as np
import glob
import imutils
from imutils import face_utils
import os
face_classifier =  cv2.CascadeClassifier('harcascades/haarcascade_frontalface_default.xml')
src_path = ("C:\\Users\\ADMIN\\Desktop\\My_data")
dst_path = ("C:\\Users\\ADMIN\\Desktop\\mmmm")

#face = face_classifier1.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),  flags=cv2.CASCADE_SCALE_IMAGE)
def face_croppped(image):
    global crop
    face = face_classifier.detectMultiScale(image,scaleFactor=1.1, minNeighbors=10,minSize=(5,5), flags=cv2.CASCADE_SCALE_IMAGE)
    if face is ():
        return None
        print ("Sorry there is no face")
    for (x, y, w, h) in face:
     crop = image[y:y + h, x:x + w]
     mm= cv2.resize(crop,(300,300))
    grey = cv2.cvtColor(mm, cv2.COLOR_BGR2GRAY)
    return grey
items = os.listdir(src_path)
i = 0
for img in items:
    filee = src_path + "\\" + img
    image = cv2.imread(filee)
    s = face_croppped(image)

    i = i + 1
    file_storage = dst_path +"\\"+"NEUTRAL" +str(i) + '.jpg'
    cv2.imwrite(file_storage,s)
    #cv2.imshow("ss",grey)
cv2.waitKey()
print("done")
cv2.destroyAllWindows()
