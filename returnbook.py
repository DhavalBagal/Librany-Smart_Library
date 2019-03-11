import cv2
import pyzbar, re, sys
import os
import numpy as np
from pyzbar.pyzbar import ZBarSymbol
from book import *

class Return:

    def __init__(self):
        self.bookset = set()
        self.bk = Book()
        self.qrlist = []
   
    def video_stream(self):

        self.cam = cv2.VideoCapture(0)
   
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280);
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720);
        

        while True :
            ret, self.frame = self.cam.read()

            self.frame = np.array(self.frame)

            try:
               self.qr = pyzbar.pyzbar.decode(self.frame, symbols=[ZBarSymbol.QRCODE])
               for i in range(len(self.qr)):
                       self.qrlist.append(self.qr[i].data.decode('utf-8'))
               
               if len(self.qrlist) != 0 :
                   for qr in self.qrlist:
                           if qr not in self.bookset:
                               self.bookset.add(qr)
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



    
