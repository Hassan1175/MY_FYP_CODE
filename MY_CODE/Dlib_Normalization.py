import cv2
import dlib
import numpy as np
import os
import imutils
import pickle
from imutils import face_utils

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
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
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)





    rects = detector(image, 1)
    for (i, rect) in enumerate(rects):
        # crop = gray[rect.top():rect.bottom(), rect.left():rect.right()]
    # cv2.imwrite("cropped.jpg", crop)
        shap = predictor(image, rect)
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
src_path = ("O:\\Namal\\TESTING_PROJECT\\testing\\test_project\\TRAINING_DATASET\\")
global i
items = os.listdir(src_path)
for img in items:
    filee = src_path + "\\" + img
    os.chdir(filee)
    images = os.listdir(filee)
    for pic in images:
        photo = cv2.imread(pic)

        print(pic)
        normalization(photo)
        labels.append(img)
print(features_vector)

file =  open("O:\\Namal\\TESTING_PROJECT\\testing\\test_project\\data_features.txt","w")
file.write(str(features_vector))
file.close()
file =  open("O:\\Namal\\TESTING_PROJECT\\testing\\test_project\\training_labels.txt","w")
file.write(str(labels))
file.close()
print(labels)
print(len(features_vector))

print(len(labels))
print("model trainibng has started")
# model = LinearSVC(C =150.0,random_state=80)
#
# model =LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
#      intercept_scaling=1, loss='squared_hinge', max_iter=1000,
#      multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
#      verbose=0)
#
#

model = SVC(C=170.0, kernel='linear', degree=3, gamma='auto', coef0=0.0,
            shrinking=True, probability=True, tol=0.001, cache_size=200,
            class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr',
            random_state=80)

# model = LogisticRegression(penalty='12', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='liblinear', max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs=1)
model.fit(features_vector,labels)


pickle_out = open("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\MY_CODE\\New_testing_dlib_normalized.pickle","wb")
pickle.dump(model,pickle_out)
pickle_out.close()
print("everthing is done")
print("done ho gyeaa")