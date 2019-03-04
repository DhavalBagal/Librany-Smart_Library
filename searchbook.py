import pyzbar, re, sys
from pyzbar.pyzbar import ZBarSymbol
import cv2, numpy as np

class Search:
    def __init__(self):
        self.found = set()
        self.flag = 0

    def search(self, book):

        self.book = book
        c = 0

        cap = cv2.VideoCapture(0)

        while True:
          c = c+1  
          ret, frame = cap.read()
          
          if ret == True:

              frame = np.array(frame)

              try:
                allbooks = pyzbar.pyzbar.decode(frame, symbols=[ZBarSymbol.QRCODE])
                
                if len(allbooks) != 0:
                    allbooks = str(allbooks)
                    allbooks = re.findall('data=b\'(.+?)\'', allbooks)
                    allbooks = [x.lower() for x in allbooks]

                    for b in allbooks:
                          if self.book.lower()==b.lower():
                                self.flag = 1
                                self.found.add(b)
                                          
                    #As soon as all relevant books are found break the loop
                    if self.flag == 1:
                        sys.stdout.write("SHELF_1")
                        sys.stdout.flush()
                        break
                    
              except:
                   pass

              winname = "Welcome to Librany!"
              cv2.namedWindow(winname)        
              cv2.moveWindow(winname, 40,30)
              cv2.imshow(winname, frame)

              if c>10:
                  break
                
              if cv2.waitKey(25) & 0xFF == ord('q'):
                  break

          else:
                break
            
        if self.flag==0:
            sys.stdout.write("NOT_FOUND")
            sys.stdout.flush()    
        cap.release()
        cv2.destroyAllWindows()

        
a =Search()
b = a.search(sys.argv[1])
sys.exit(0)
        





