import cv2
import pyzbar, re, sys
import os
import numpy as np
from pyzbar.pyzbar import ZBarSymbol
from book import *

class Issue:

    def __init__(self):
        self.user_set = set()
        self.issued_set = set()

        with open("users.txt", 'r') as f:
            self.namelist = f.read()
        self.namelist = self.namelist.split("\n")

        self.bk = Book()
        self.qrlist = []

    def detect(self):
        
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
        
        faces = face_cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5)

        if (len(faces) == 0):
            return None
    
        #The project assumes that there would be just one face at a single point in time.
        (self.x, self.y, self.w, self.h) = faces[0]

        image = image[self.y:self.y+self.w, self.x:self.x+self.h]
    
        return image

    def draw_rectangle(self):
        cv2.rectangle(self.frame, (self.x, self.y), (self.x+self.w, self.y+self.h), (0, 255, 0), 2)

    def draw_text(self):
        cv2.putText(self.frame, self.namelist[self.label], (self.x, self.y-5), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
 
    def recognise(self):
        
        face = self.detect()
        
        if face is not None:
            self.label, _ = self.face_recognizer.predict(face)
            self.draw_rectangle()
            self.draw_text()

            return self.frame, self.namelist[self.label]
        else :
            return self.frame, None
            
        
    def video_stream(self):

        self.cam = cv2.VideoCapture(0)
   
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280);
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720);
        
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_recognizer.read("face_model.yml")

        while True :
            self.qrlist = []
            ret, self.frame = self.cam.read()

            self.frame = np.array(self.frame)

            self.frame, self.name = self.recognise()

            if self.name != None:   

                try:
                   self.qr = pyzbar.pyzbar.decode(self.frame, symbols=[ZBarSymbol.QRCODE])
                   
                   for i in range(len(self.qr)):
                       self.qrlist.append(self.qr[i].data.decode('utf-8'))
                   #print(self.qrlist)
                   
                   if len(self.qrlist) != 0 :

                       for qr in self.qrlist:
                           if qr not in self.issued_set:
                               self.issued_set.add(qr)
                               status = self.bk.issue(self.name, qr)
                  
                except :
                   pass
 
            winname = "Welcome to Librany!"
            cv2.namedWindow(winname)        
            cv2.moveWindow(winname, 60,0)
            cv2.imshow(winname, self.frame)
   
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cam.release()
        cv2.destroyAllWindows()

a = Issue()
a.video_stream()


    
