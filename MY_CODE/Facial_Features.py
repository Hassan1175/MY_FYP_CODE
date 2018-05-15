import cv2
import dlib
import numpy as np
from imutils import face_utils
import mpmath
path = "dlibb/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(path)
img = cv2.imread("C:\\Users\\Admin\\Desktop\\S.png")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.resize(img,(800,600))


def normalization(image):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(image, 1)
    done =[]
    for (i, rect) in enumerate(rects):
        # crop = gray[rect.top():rect.bottom(), rect.left():rect.right()]
    # cv2.imwrite("cropped.jpg", crop)
        shap = predictor(image, rect)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText(image, "Face {}".format(i + 1), (x - 10, y - 10),
        #         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        xlist = []
        ylist = []
        shap = face_utils.shape_to_np(shap)

        Centre =(shap[30])
    # print(Centre)
        centre_x = Centre[0]
        centre_y  =  Centre[1]
        # shap = shap[18:68]
        for i  in shap:
         xlist.append(i[0])
         ylist.append(i[1])
         forx = []
         fory =[]
        for x in xlist:
            forx.append((x - centre_x) ** 2)
    # print(xlist)
        for y in ylist:
            fory.append((y - centre_y) ** 2)
        listsum = [sum(x) for x in zip(forx, fory)]
    # print(min(listsum))

        features =[]
        for i in listsum:
            k = mpmath.sqrt(float(i))
            features.append(float(k))
        # print(len(features))
        maxx = (max(features))
        # print(maxx)
        final = []
        # print(min(features))
        # print("hello word")
        for i in features:
            if (i ==0.0):
                continue
            F = i/maxx
            final.append(F)
        # print(final)
        NN = np.array(final)
        done.append(NN)
        for (x, y) in shap:
            cv2.circle(image, (x, y), 1, (0, 0, 255), 2)
            # cv2.line(image,(x,y),(centre_x, centre_y),(255,0,0),1)

    # cv2.circle(image, (xm,ym), 1, (0, 0, 0), 5)
    #     cv2.circle(image, (centre_x, centre_y), 1, (0, 0, 0), 5)
    print(done)
    print(len(done))

    cv2.imshow("IMAGEDD", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

 # cv2.line(img,(0,0),(511,511),(255,0,0),5)

normalization(img)
