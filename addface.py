import cv2, re
import os
import time
import numpy as np

cam = cv2.VideoCapture(0)

#The directory name is the label or the index which would be returned by the face recogniser on successful detection of that particular face.
name = input("Enter the name of the directory where you want to store the pictures : ")

#Create the directory for training images in the face_dataset directory,if it doesn't exist.
os.makedirs("face_dataset"+"/"+name, exist_ok=True)

#Count stores the label which will be given for each image in the dataset
#E.g for user 1 in the directory '1' each image would be saved as 1.jpg, 2.jpg, 3.jpg... and so on.
count = 0

#Capture the start time
start = time.time()

#While the elapsed time since the start is less than 10 secs, do the following
while int(time.time() - start) <= 10 :
    ret, frame = cam.read()
    
    w = int(frame.shape[1]/2)
    h = int(frame.shape[0]/2)

    #Capture each frame and store it in .jpg format in the dataset directory      
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

#Input to the function is a video frame. Output is only that portion of the frame in which 1 face is detected.
def detect_face(image):
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

    #A smaller scale  will increase the number of layers in the image pyramid and increase the amount of time it takes to process your image
    #minNeighbors specifies how many neighbors each candidate rectangle should have to retain it. This parameter will affect the quality of the detected faces: higher value results in less detections but with higher quality. 
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5)
    
    #If no face is found, return None
    if (len(faces) == 0):
        return None, None
    
    #The project assumes that there would be just one face at a single point in time.
    (x, y, w, h) = faces[0]
    
    return image[y:y+w, x:x+h], faces[0]

def prepare(datasetpath):
    
    names = os.listdir(datasetpath)

    #Stores each face for a particular user in its training directory
    faces=[]
    labels =[]

    #names contain the index of each user.
    for name in names:

        #Ignore hidden files like .DStore etc
        if name.startswith("."):
            continue
            
        print("Training on "+name+"\'s pictures...")

        #train_images contain the names of all images for a particular user.
        #E.g 1.jpg, 2.jpg and so on
        train_images = os.listdir(datasetpath+"/"+name)
        
        for train_image in train_images:
            
            if name.startswith("."):
                continue
            
            #Read each image in that particular user's directory   
            train_image = cv2.imread(datasetpath+"/"+name+"/"+train_image)

            #Detect faces and bounding box
            face, rect = detect_face(train_image)
            
            #If face is detected, add it to the 'faces' list
            if face is not None:
                
                faces.append(face)
                
                #Labels is the index which would be returned by the face recogniser on recognising that user
                labels.append(int(name))
           
    cv2.destroyAllWindows()

    return faces, np.array(labels)

print("Training the model..\n")
faces, labels = prepare("face_dataset")

print("\nModel trained completely!")

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

face_recognizer.train(faces, labels)
face_recognizer.save('face_model.yml')

print("\nModel saved successfully!")
 
