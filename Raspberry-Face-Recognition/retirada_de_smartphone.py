import sys

# Import OpenCV2 for image processing
import cv2

# Import numpy for matrices calculations
import numpy as np

# Import for GPIO
import RPi.GPIO as gpio
import time

# Checking if Id has smartphone on a cabin
fh1 = open("memory_1.txt","r+")
fh2 = open("memory_2.txt","r+")
fh3 = open("memory_3.txt","r+")
id1 = fh1.readline(1)
id2 = fh2.readline(1)
id3 = fh3.readline(1)
fh1.close()
fh2.close()
fh3.close()

while(True):
    face_id = input('Enter your ID (enter 0 if you want to exit): ')
    if(face_id == 0):
        sys.exit()
    elif(id1 == str(face_id)):
        g = 11
        p = 12
        n = 1
        fh1 = open("memory_1.txt","r")
        name = fh1.readline(3)
        fh1.close()
	break
    elif(id2 == str(face_id)):
        g = 13
        p = 16
        n = 2
        fh2 = open("memory_2.txt","r")
        name = fh2.readline(3)
        fh2.close()
	break
    elif(id3 == str(face_id)):
        g = 15
        p = 18
        n = 3
        fh3 = open("memory_3.txt","r")
        name = fh3.readline(3)
        fh3.close()
	break

fh = open("memory_"+str(n)+".txt","r")
name = fh.readline(3)
fh.close()

# Configuring GPIO
gpio.setmode(gpio.BOARD)
# Locks GPIOs
gpio.setup(g, gpio.OUT) # Cabin 
gpio.setup(p, gpio.OUT) # Power plug 

# Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.createLBPHFaceRecognizer()

# Load the trained mode
recognizer.load('trainer/trainer.yml')

# Load prebuilt model for Frontal Face
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath);

# Set the font style
font = cv2.FONT_HERSHEY_SIMPLEX

# Recognition flag
rec_flag = 0

# Initialize and start the video frame capture
cam = cv2.VideoCapture(0)

# Loop
while True:
    # Read the video frame
    ret, im =cam.read()

    # Convert the captured frame into grayscale
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    # Get all face from the video frame
    faces = faceCascade.detectMultiScale(gray, 1.2,5)

    # For each face in faces
    for(x,y,w,h) in faces:

        # Create rectangle around the face
        cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)

        # Recognize the face belongs to which ID
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
        
        # Check the ID if exist 
        if(conf < 50):
            if(Id == face_id):
                Id = name
                gpio.output(g, gpio.HIGH) # Open cabin 
                gpio.output(p, gpio.HIGH) # Stop power plug
                rec_flag = 1
                fh = open("memory_"+str(n)+".txt","w")
                fh.write("0\n")
                fh.write("0\n")
                fh.write("0")
                fh.close()
        else:
            Id = "Unknown"
	
        # Put text describe who is in the picture
        cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
        cv2.putText(im, str(Id), (x,y-40), font, 2, (255,255,255), 3)

    # Display the video frame with the bounded rectangle
    cv2.imshow('im',im) 

    # If 'q' is pressed, close program
    if(rec_flag == 1):
        break

# Stop the camera
cam.release()

# Close all windows
cv2.destroyAllWindows()

# End operation
input("Press any key to end operation...")

# Undo GPIO configuration
gpio.cleanup()
