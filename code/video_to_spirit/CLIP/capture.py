import cv2

cap=cv2.VideoCapture('./阳光电影www.ygdy8.com.蜡笔小新：谜团.2021.BD.1080P.国粤日三语中字.mkv')
frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
for i in range(int(frame_count)):
    _,img=cap.read()
    if i < 500:
        cv2.imwrite('./pic/image{}.jpg'.format(i),img)
