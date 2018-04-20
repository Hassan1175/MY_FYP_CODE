import cv2
vidcap = cv2.VideoCapture(0)
success,image = vidcap.read()
count = 0
dst_path = ("C:\\Users\\ADMIN\\Desktop\\My_data")

while True:
       # save frame as JPEG file
       ret, frame = vidcap.read()
       file_storage = dst_path + "\\" + "NEUTRAL" + str(count) + '.jpg'
       cv2.resize(frame,(300,300))
       gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
       cv2.imwrite(file_storage, gray)
       count += 1
       print(count)
       cv2.imshow("sd",gray)
       cv2.waitKey(1)
vidcap.release()
cv2.destroyAllWindows()