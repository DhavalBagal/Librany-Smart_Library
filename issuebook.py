import cv2
import pyzbar, re, sys
import os
import numpy as np
from pyzbar.pyzbar import ZBarSymbol
from book import *

class Issue:

    def __init__(self):

        #Stores the qr codes of all the issued books from when the cam starts and uptill it is switched off.
        self.issued_set = set()

        #Grab the userid's of all the registered users in 'namelist'
        with open("users.txt", 'r') as f:
            self.namelist = f.read()

        #users.txt files has names of all registered users with each name on a new line
        #Also the first line is left empty
        self.namelist = self.namelist.split("\n")

        #Create an object of class Book. This object is responsible for all the database transactions
        self.bk = Book()

        #Import the frontal face cascade classifier
        self.face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

    #Input to the function is a video frame. Output is only that portion of the frame in which 1 face is detected.
    def detect(self):

        #Convert the obtained frame (in self.frame) to grayscale
        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        #A smaller scale  will increase the number of layers in the image pyramid and increase the amount of time it takes to process your image
        #minNeighbors specifies how many neighbors each candidate rectangle should have to retain it. This parameter will affect the quality of the detected faces: higher value results in less detections but with higher quality. 
        faces = self.face_cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5)

        #If no face is detected return none
        if (len(faces) == 0):
            return None
    
        #The project assumes that there would be just one face at a single point in time.
        (self.x, self.y, self.w, self.h) = faces[0]

        image = image[self.y:self.y+self.w, self.x:self.x+self.h]

        #Return just the image (i.e the rectangle) which has just the face in it.
        return image

    def draw_rectangle(self):
        cv2.rectangle(self.frame, (self.x, self.y), (self.x+self.w, self.y+self.h), (0, 255, 0), 2)

    def draw_text(self):
        cv2.putText(self.frame, self.namelist[self.label], (self.x, self.y-5), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    #Input is the video frame. Output is a frame with bounding box and label drawn and return value is this frame along with the userid of the detected face.
    def recognise(self):

        #Get the face from the entire video frame
        face = self.detect()
        
        if face is not None:

            #Predict the label for the face. conf gives the confidence value. It should be low for higher accuracy.
            #conf actually is the loss.
            #label returned by the predcitor is the index which starts from 0
            self.label, conf = self.face_recognizer.predict(face)

            #Thresholding only those faces who have confidence value less than 70.
            #This is to avoid detecting the users which are not registered with the system.
            if conf<80:
                self.draw_rectangle()
                self.draw_text()

                #Find the name from the namelist with index = self.label.
                return self.frame, self.namelist[self.label]
            else :
                return self.frame, None
        else :
            return self.frame, None
            
        
    def video_stream(self):

        self.cam = cv2.VideoCapture(0)

        #Set webcam resolution
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280);
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720);

        #Create a face recognizer object
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()

        #Import the pretrained model into the face recognizer object
        self.face_recognizer.read("face_model.yml")

        while True :

            #Since for each frame the qrlist must contain all the detected qr codes, we intialize it to empty for each frame.
            #Qrlist contains the text (i.e bookid) of all the detected qr codes.
            self.qrlist = []

            #Capture the frame in self.frame 
            ret, self.frame = self.cam.read()

            #Convert the raw opencv image into numpy array
            self.frame = np.array(self.frame)

            #Get the frame with drawn bounding boxes along with the userid of the detected face.
            self.frame, self.name = self.recognise()

            
            #If a user is detected
            if self.name != None:   

                try:

                   #Get all the qr codes in self.qr
                   self.qr = pyzbar.pyzbar.decode(self.frame, symbols=[ZBarSymbol.QRCODE])

                   #We need to decode the array returned by pyzbar to extract just the data out of it,
                   #since it contains various other stuff like coordinates of bounding box along with the data.
                   for i in range(len(self.qr)):
                       xp,yp,wf,hf = self.qr[i].rect
                       cv2.rectangle(self.frame, (xp, yp), (xp+wf, yp+hf), (255, 0, 0), 2)

                       self.qrlist.append(self.qr[i].data.decode('utf-8'))

                   #If self.qrlist is not empty, i.e if some qrcode exists in the frame
                   if len(self.qrlist) != 0 :

                       for qr in self.qrlist:
                           if qr not in self.issued_set:
                    
                               #Add all the detected qrcodes to the issued_set so that the same qr code captured in the immediate next frame wont be considered.
                               self.issued_set.add(qr)

                               #Issue the book (i.e qr which stores the bookid) on the detected user's name (i.e self.name which stores userid of detected user)
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


    
