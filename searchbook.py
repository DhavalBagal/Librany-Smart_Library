import pyzbar, re, sys
from pyzbar.pyzbar import ZBarSymbol
import cv2, numpy as np
from book import Book
import time

class Search:
    def __init__(self):
        self.bk = Book()

    def update_locations(self):

        cap = cv2.VideoCapture(0)

        while True:
                ret, frame = cap.read()

                frame = np.array(frame)


                #Since for each frame the allbooks must contain all the detected qr codes, we intialize it to empty for each frame.
                #allbooks contains the text (i.e bookid) of all the detected qr codes.
                allbooks=[]
                
                try:
                        #Get all the qr codes detected in a particular frame in allbooks
                        qr = pyzbar.pyzbar.decode(frame, symbols=[ZBarSymbol.QRCODE])

                        #We need to decode the array returned by pyzbar to extract just the data out of it,
                        #since it contains various other stuff like coordinates of bounding box along with the data.   
                        for i in range(len(qr)):
                               xp,yp,wf,hf = qr[i].rect
                               cv2.rectangle(frame, (xp, yp), (xp+wf, yp+hf), (255, 0, 0), 2)

                               allbooks.append(qr[i].data.decode('utf-8'))

                        if len(allbooks) != 0:

                            for eachbook in allbooks:
                                self.bk.updatelocation(eachbook, 'SHELF_1')

                except :
                        pass

                winname = "Welcome to Librany!"
                cv2.namedWindow(winname)        
                cv2.moveWindow(winname, 40,30)
                cv2.imshow(winname, frame)

                #time.sleep(5)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

a = Search()
a.update_locations()

                        

                
