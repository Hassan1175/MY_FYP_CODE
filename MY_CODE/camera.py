import dlib
from imutils import face_utils
dlib_path = "dlibb/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(dlib_path)
import argparse
import pickle
import cv2
import os
import mpmath
import numpy as np

class VideoCamera(object):
    def __init__(self):

        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        pickle_in = open("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\dlib_normalized.pickle", "rb")
        # pickle_in = open("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\dlib_normalized_full.pickle","rb")
        model = pickle.load(pickle_in)
        B=0
        while(True):
            ret, frame = self.video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            B += 1
            if B % 5 == 0:
                face = detector(gray, 0)
                for (J, rect) in enumerate(face):
                    shap = predictor(gray, rect)
                    xlist = []
                    ylist = []
                    shap = face_utils.shape_to_np(shap)
                    Centre = (shap[30])
                    centre_x = Centre[0]
                    centre_y = Centre[1]
                    shap = shap[18:68]
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
                    prediction = model.predict([numpy_array])[0]

                    # predict.append(prediction)
                    (x, y, w, h) = face_utils.rect_to_bb(rect)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # display the image and the prediction
                    #     cv2.putText(frame, "FACE ({})".format(J+ 1) + " " + prediction, (x , y ), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                    #             (0, 255, 0), 2)
                    cv2.putText(frame, prediction, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                (0, 255, 0), 2)
                    print(prediction)
                    cv2.circle(frame, (centre_x, centre_y), 1, (0, 0, 0), 10)
                    for (x, y) in shap:
                        cv2.circle(frame, (x, y), 1, (0, 0, 255), 2)
                        print(x,y)
                        print("done")
                    ret, jpeg = cv2.imencode('.jpg', frame)
                    return jpeg.tobytes()


