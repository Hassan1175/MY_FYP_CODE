import sklearn
from sklearn import svm
from sklearn.svm import LinearSVC
# from MYSVM import LocalBinary
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

src_path = ("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\TESTING_DATASET\\")
predict = []
features_vector = []

pickle_in = open("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\dlib_normalized.pickle","rb")

# pickle_in = open("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\dlib_normalized_full.pickle","rb")

model = pickle.load(pickle_in)

items = os.listdir(src_path)
for imgage in items:
    folder = src_path+"\\"+imgage
    os.chdir(folder)
    pics = os.listdir(folder)
    for piic in pics:
        tasveer = cv2.imread(piic)
        face = detector(tasveer,0)
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
            # print(final)
            numpy_array = np.array(final)
            # features_vector.append(numpy_array)
            for (x, y) in shap:
                cv2.circle(tasveer, (x, y), 1, (0, 0, 255), 2)
            cv2.circle(tasveer, (centre_x, centre_y), 1, (0, 0, 0), 5)
            # print(features_vector)
            prediction = model.predict([numpy_array])[0]
            predict.append(prediction)
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(tasveer, (x, y), (x + w, y + h),
                      (0, 255, 0), 2)
        # display the image and the prediction
        cv2.putText(tasveer, "FACE ({})".format(J+ 1) + " " + prediction, (x , y ), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                    (0, 255, 0), 2)
        # cv2.putText(tasveer,  prediction, (x-5 , y-5 ), cv2.FONT_HERSHEY_COMPLEX, 1.2,
        #             (0, 0, 255),4)
        print(prediction)
        cv2.imshow("Image", tasveer)
        cv2.waitKey(0)
file =  open("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\dlib_testing_labels.txt","r")
reading = file.read()
reading2 = reading.split()
new_list = []
for item in reading2:
    new_str = ""
    for entry in item:
        if entry.isalpha()==True:
            new_str = new_str+entry
    new_list.append(new_str)
count = 0.0
correct = 0
for i in range(len(new_list)):
    count = count + 1
    if new_list[i] == predict[i]:
        correct =  correct+1
print(count)
print(correct)
M = correct/count
Accuray = M *100
print("Accuracy is ", Accuray, " percent")
print("Everything is done. . . . . .")
