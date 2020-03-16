#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import urllib  
import RPi.GPIO as GPIO
import signal  
import atexit
import time
import send
import pygame
import threading
from time import ctime,sleep

def music():
    print 'm'
    file=r'/home/pi/Music/5.ogg'
    pygame.mixer.init()
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(5.0) 
    pygame.mixer.music.play(loops=0,start=0)
    time.sleep(10)
    pygame.mixer.music.stop()
    



recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'BIAOGE', 'Paula', 'Ilza', 'Z', 'W'] 

# Initialize and start realtime video capture
#cam = cv2.VideoCapture(0)
#cam.set(3, 640) # set video widht
#cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 64
minH = 48

while True:
    url = r"http://127.0.0.1:8080/?action=snapshot"  
    path = r"./face.jpg"  
    data = urllib.urlopen(url).read()  
    f = file(path,"wb")  
    f.write(data)  
    f.close() 
    
   # ret, img =cam.read()
  #  img = cv2.flip(img, -1) # Flip vertically
    img = cv2.imread('face.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            confidence=100-confidence
            #confidence = "0".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence=100-confidence
            #confidence = "0".format(round(100 - confidence))
        
 #       cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
#	cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
#    cv2.imshow('camera',img) 
        print id
        print confidence
	
	if confidence>50:
	    print 'real'
            threads = []
            t1 = threading.Thread(target=music)
            threads.append(t1)

            
    
            t1.setDaemon(True)

            t1.start()
            
	    atexit.register(GPIO.cleanup)    
	    servopin = 21  
	    GPIO.setmode(GPIO.BCM)  
	    GPIO.setup(servopin, GPIO.OUT, initial=False)  
	    p = GPIO.PWM(servopin,50) #50HZ  
	    p.start(0)  
	    for i in range(1,7):
		p.ChangeDutyCycle(2.5) #设置转动角度  
		time.sleep(0.02)                      #等该20ms周期结束  
		p.ChangeDutyCycle(0)                  #归零信号
	    time.sleep( 5 )
		
	    s=time.ctime()
	    print '33333'
	    send.sendmsg('oFfru09XqsVOPTHRBXooncms-xBc',id+' open door at '+s)
	    
	    print s
	    time.sleep( 5 )
	    
	    print '1'
	    

	    
	    
	    for i in range(1,7):           #开
		p.ChangeDutyCycle(12.5) #设置转动角度  
		time.sleep(0.02)                      #等该20ms周期结束  
		p.ChangeDutyCycle(0)                  #归零信号
	    
	    print '2'
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
