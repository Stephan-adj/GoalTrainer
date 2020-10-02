# test de la caméra picamera.py
# importer les paquets requis pour la Picaméra
from picamera import PiCamera
import cv2.cv as cv
from time import sleep
import time
import cv2
i=0

# initialisation des paramètres pour la capture
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 32
camera.rotation = 180

# temps réservé pour l'autofocus
time.sleep(0.1)
camera.start_preview()
while True :
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        camera.stop_preview()
    if key == "c":
        camera.capture('/home/pi/Desktop/image' + str(i) + '.jpg' )
        i+=1
        
        



import cv2.cv as cv

if __name__=='__main__':
    ma_caméra = cv.CaptureFromCAM(0)
    cv.NamedWindow("Test_Webcam")
    while True:
        ma_frame = cv.QueryFrame(ma_caméra)
        cv.ShowImage("Test_Webcam", ma_frame)

        if (cv.WaitKey(10) % 0x100) == 113:
            break
