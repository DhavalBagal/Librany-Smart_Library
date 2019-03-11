import cv2
import pyzbar, re, sys
import os
import numpy as np
from pyzbar.pyzbar import ZBarSymbol
from book import *

class Return:

    def __init__(self):
        #bookset stores all the bookids of the books returned from when the camera is switched on untill its switched off.
        self.bookset = set()

        #bk is the object which will be required for all the transactions with the database.
        self.bk = Book()       
   
    def video_stream(self):

        self.cam = cv2.VideoCapture(0)
   
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280);
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720);

        while True :
            
            #Since for each frame the qrlist must contain all the detected qr codes, we intialize it to empty for each frame.
            #Qrlist contains the text (i.e bookid) of all the detected qr codes. 
            self.qrlist = []
            
            ret, self.frame = self.cam.read()

            self.frame = np.array(self.frame)

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
                           if qr not in self.bookset:
                               
                               #Add all the detected qrcodes to the bookset so that the same qr code captured in the immediate next frame wont be considered.
                               self.bookset.add(qr)

                               #Return the book i.e update the database as required.
                               status = self.bk.returnbook(qr)
                   
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

a = Return()
a.video_stream()



    
