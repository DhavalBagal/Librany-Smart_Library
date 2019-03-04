import cv2, re
import os
import time
import numpy as np

cam = cv2.VideoCapture(0)
name = input("Enter the name of the directory where you want to store the pictures : ")
os.makedirs("face_dataset"+"/"+name, exist_ok=True)

count = 0
start = time.time()

while int(time.time() - start) <= 10 :
    ret, frame = cam.read()
    
    w = int(frame.shape[1]/2)
    h = int(frame.shape[0]/2)
        
    try:
        frame = cv2.resize(frame, (w,h))
        cv2.imwrite("face_dataset/"+name+"/"+str(count)+".jpg", frame) 
        count += 1
        
    except : 
        pass
    
    cv2.imshow("Register User", frame)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cam.release()
cv2.destroyAllWindows()

def detect_face(image):
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5)
    
    #If no face is found, return None
    if (len(faces) == 0):
        return None, None
    
    #The project assumes that there would be just one face at a single point in time.
    (x, y, w, h) = faces[0]
    
    return image[y:y+w, x:x+h], faces[0]

def prepare(datasetpath):
    
    names = os.listdir(datasetpath)
    faces=[]
    labels =[]
    
    for name in names:
       
        if name.startswith("."):
            continue
            
        print("Training on "+name+"\'s pictures...")
            
        train_images = os.listdir(datasetpath+"/"+name)
        
        for train_image in train_images:
            
            if name.startswith("."):
                continue
                
            train_image = cv2.imread(datasetpath+"/"+name+"/"+train_image)
            
            face, rect = detect_face(train_image)
            
            
            if face is not None:
                
                faces.append(face)
                
                labels.append(int(name))
           
    cv2.destroyAllWindows()
    #cv2.waitKey(1)
    #cv2.destroyAllWindows()

    return faces, labels

print("Training the model..\n")
faces, labels = prepare("face_dataset")

print("\nModel trained completely!")

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

face_recognizer.train(faces, np.array(labels))
face_recognizer.save('face_model.yml')

print("\nModel saved successfully!")
 
