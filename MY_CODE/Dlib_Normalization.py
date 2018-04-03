import cv2
import dlib
import numpy as np
import os
import imutils
import pickle
from imutils import face_utils
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import mpmath

face_classifier =  cv2.CascadeClassifier('harcascades/haarcascade_frontalface_default.xml')
dlib_path = "dlibb/shape_predictor_68_face_landmarks.dat"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(dlib_path)
features_vector = []
# global count
def normalization(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    for (i, rect) in enumerate(rects):
        # crop = gray[rect.top():rect.bottom(), rect.left():rect.right()]
    # cv2.imwrite("cropped.jpg", crop)
        shap = predictor(gray, rect)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, "Face {}".format(i + 1), (x - 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        xlist = []
        ylist = []
        shap = face_utils.shape_to_np(shap)

        Centre =(shap[30])
        centre_x = Centre[0]
        centre_y  =  Centre[1]
        shap = shap[18:68]
        for i  in shap:
         xlist.append(i[0])
         ylist.append(i[1])
         forx = []
         fory =[]
        for x in xlist:
            forx.append((x - centre_x) ** 2)
        for y in ylist:
            fory.append((y - centre_y) ** 2)
        listsum = [sum(x) for x in zip(forx, fory)]
        features =[]
        for i in listsum:
            k = mpmath.sqrt(float(i))
            features.append(float(k))
        maxx = (max(features))
        final = []
        for i in features:
            if (i ==0.0):
                continue
            F = i/maxx
            final.append(F)
        # print(final)
        numpy_array = np.array(final)
        # print(numpy_array)
        features_vector.append(numpy_array)
        # print((features_vector))
        for (x, y) in shap:
            cv2.circle(image, (x, y), 1, (0, 0, 255), 1)

    #     cv2.circle(image, (centre_x, centre_y), 1, (0, 0, 0), 5)
    # cv2.imshow("IMAGEDD", image)
    # cv2.waitKey(0)
# count =0
labels = []
src_path = ("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\TRAINING_DATASET\\")
global i
items = os.listdir(src_path)
for img in items:
    # print(img)
    filee = src_path + "\\" + img
    os.chdir(filee)
    images = os.listdir(filee)
    for pic in images:
        photo = cv2.imread(pic)
        normalization(photo)
        # count+=1
        labels.append(img)
        print(pic)

    # if(img == "NEUTRAL"):
    #     break

print(features_vector)
print(labels)
print(len(features_vector))
print(len(labels))
print("model trainibng has started")
model = LinearSVC(C =70.0,random_state=60)
model.fit(features_vector,labels)

# O:\Nama_College\FYP\MY_FYP_CODE\MY_FYP_CODE\MY_CODE
pickle_out = open("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\dlib_normalized.pickle","wb")
pickle.dump(model,pickle_out)
pickle_out.close()
print("everthing is done")
print("done ho gyeaa")
