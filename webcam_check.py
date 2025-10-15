import cv2
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print("Webcam opened:", cap.isOpened())
cap.release()