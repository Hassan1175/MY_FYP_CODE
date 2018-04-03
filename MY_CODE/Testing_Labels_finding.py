import cv2
import os


labels = []
src_path = ("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\TESTING_DATASET\\")
global i
items = os.listdir(src_path)
for img in items:
    # print(img)
    filee = src_path + "\\" + img
    os.chdir(filee)
    images = os.listdir(filee)
    for pic in images:
        # photo = cv2.imread(pic)
        # normalization(photo)
        # # count+=1
        labels.append(img)

Q = str(labels)
file = open("O:\\Nama_College\\FYP\\MY_FYP_CODE\\MY_FYP_CODE\\MY_CODE\\dlib_testing_labels.txt","w" )
file.write(Q)
file.close()
print("DONE")
print(labels)
print(len(labels))
