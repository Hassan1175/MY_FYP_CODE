import sklearn
from sklearn import svm
from sklearn.svm import LinearSVC

from imutils import paths
import cv2
import dlib

from imutils import face_utils
# face_classifier =  cv2.CascadeClassifier('harcascades/haarcascade_frontalface_default.xml')
dlib_path = "dlibb/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(dlib_path)
import argparse
import pickle
import cv2
import os
import mpmath
import numpy as np
# src_path = ("O:\\Nama_College\\FYP\\Final_Year\\TESTING_DATASET\\")
predict = []
features_vector = []
pickle_in = open("dlib_normalized.pickle","rb")
# pickle_in = open("O:\\Nama_College\\FYP\\Final_Year\\dlib_normalized_full.pickle", "rb")
model = pickle.load(pickle_in)
# items = os.listdir(src_path)
# for imgage in items:
#     folder = src_path+"\\"+imgage
#     os.chdir(folder)
#     pics = os.listdir(folder)
#     for piic in pics:
# tasveer = cv2.imread("C:\\Users\\Admin\\Desktop\\12.jpg")
tasveer = cv2.imread("C:\\Users\\Admin\\Desktop\\m.jpg")


# tasveer = cv2.cvtColor(tasveer, cv2.COLOR_BGR2GRAY)
face = detector(tasveer,1)
for (J, rect) in enumerate(face):
            shap = predictor(tasveer, rect)
            xlist = []
            ylist = []
            shap = face_utils.shape_to_np(shap)
            Centre = (shap[30])
            centre_x = Centre[0]
            centre_y = Centre[1]
            shap =  shap[18:68]
            for i in shap:
                xlist.append(i[0])
                ylist.append(i[1])
            forx = []
            fory = []
            for x in xlist:
                forx.append((x - centre_x) ** 2)
            for y in ylist:
                fory.append((y - centre_y) ** 2)
            listsum = [sum(x) for x in zip(forx, fory)]
            features = []
            for i in listsum:
                k = mpmath.sqrt(float(i))
                features.append(float(k))
            maxx = (max(features))
            final = []
            for i in features:
                if (i == 0.0):
                    continue
                F = i / maxx
                final.append(F)

            numpy_array = np.array(final)
            # features_vector.append(numpy_array)
            for (x, y) in shap:
                cv2.circle(tasveer, (x, y), 1, (0, 0, 255), 1)
            cv2.circle(tasveer, (centre_x, centre_y), 1, (0, 0, 0), 5)
            # print(features_vector)
            prediction = model.predict([numpy_array])[0]
            predict.append(prediction)
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(tasveer, (x, y), (x + w, y + h),
                      (0, 255, 0), 2)
        # display the image and the prediction
            cv2.putText(tasveer,  prediction, (x-5 , y-5 ), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                    (0, 0, 255), 2)
            # print(prediction)
count1 = 0
count2 = 0
count3 = 0

for i in predict:
    if (i =="INTERESTED"):
        count1 +=1
    elif(i == "NEUTRAL"):
        count2+=1
    else:
        count3+=1

print(  "Total Number of Faces "  , len(predict))

print(  "Number of Interested faces "  , count1)

print(  "Number of Neutral faces "  , count2)

print(  "Number of Bore Faces "  , count3)
cv2.imshow("Image", tasveer)
cv2.waitKey(0)
print("Everything is done. . . . . .")