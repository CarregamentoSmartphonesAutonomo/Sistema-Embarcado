import sys
import cv2
import numpy as np
import RPi.GPIO as gpio
import time
import os
import decimal

def checar_cabines():
    cabine = ""
    # Check if there are cabins available
    fh1 = open("memory_1.txt","r+")
    fh2 = open("memory_2.txt","r+")
    fh3 = open("memory_3.txt","r+")
    op1 = fh1.readline(2)
    op1 = op1.rstrip()
    op2 = fh2.readline(2)
    op2 = op1.rstrip()
    op3 = fh3.readline(2)
    op3 = op1.rstrip()
    fh1.close()
    fh2.close()
    fh3.close()
    if(op1 == '0'):
        cabine = cabine+"1"
    if(op2 == '0'):
        cabine = cabine+"2"
    if(op3 == '0'):
        cabine = cabine+"3"
    print "Cabine:", cabine
    return cabine

def obter_fotos(face_id):

    # Start capturing video 
    vid_cam = cv2.VideoCapture(0)

    # Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Initialize sample face image
    count = 0

    # Cabin flag
    cab_flag = 0

    # Start looping
    while(True):

        # Capture video frame
        _, image_frame = vid_cam.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

        # Detect frames of different sizes, list of faces rectangles
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # Loops for each faces
        for (x,y,w,h) in faces:

            # Crop the image frame into rectangle
            cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
            
            # Increment sample face image
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            # Display the video frame, with bounded rectangle on the person's face
            #cv2.imshow('frame', image_frame)

        # If image taken reach 100, stop taking video
        if count>100:
            break

    # Stop video
    vid_cam.release()

    # Close all started windows
    cv2.destroyAllWindows()

    print("Training data...")
    os.system("python training.py")
    print("\nTraining done!")

    return True

def colocar_na_cabine(name,face_id,cab_id):
    print(name)
    print(face_id)
    print(cab_id)
    if(cab_id == '1'):
        gpio.output(12, gpio.LOW) # ativar tomada
        fh1 = open("memory_1.txt","w")
        fh1.write(face_id+"\n")
        fh1.write("1\n")
        fh1.write(name+"\n")
        fh1.close()
        gpio.output(11, gpio.LOW) # abrir cabine
        return True
    elif(cab_id == '2'):
        gpio.output(16, gpio.LOW)
        fh2 = open("memory_2.txt","w")
        fh2.write(face_id+"\n")
        fh2.write("1\n")
        fh2.write(name+"\n")
        fh2.close()
        gpio.output(13, gpio.LOW)
        cab_flag = 1
        return True
    elif(cab_id == '3'):
        gpio.output(18, gpio.LOW)
        fh3 = open("memory_3.txt","w")
        fh3.write(face_id+"\n")
        fh3.write("1\n")
        fh3.write(name+"\n")
        fh3.close()
        gpio.output(15, gpio.LOW)
        cab_flag = 1
        return True
    else:
        return False

def confirmar_fechamento(cab_id):
    if(cab_id == '1'):
        gpio.output(11, gpio.HIGH)
        return True
    elif(cab_id == '2'):
        gpio.output(13, gpio.HIGH)
        return True
    elif(cab_id == '3'):
        gpio.output(15, gpio.HIGH)
        return True
    else:
        return False

def remover_smartphone(cab_id):

    if(cab_id == '1'):
        g = 11
        p = 12
        n = 1
        fh1 = open("memory_1.txt","r")
        face_id = fh1.readline(1)
        name = fh1.readline(3)
        fh1.close()
    elif(cab_id == '2'):
        g = 13
        p = 16
        n = 2
        fh2 = open("memory_2.txt","r")
        face_id = fh2.readline(1)
        name = fh2.readline(3)
        fh2.close()
    elif(cab_id == '3'):
        g = 15
        p = 18
        n = 3
        fh3 = open("memory_3.txt","r")
        face_id = fh3.readline(1)
        name = fh3.readline(3)
        fh3.close()
    else:
        return False

    print(name)
    print(face_id)
    print(int(face_id))

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

    # Flags
    rec_flag = 0
    unk_flag = 0

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
            print("Id reconhecido: ", Id)
            print("Confianca: ", conf)
            # Check the ID if exist
            if(conf < 60):
                if(Id == int(face_id)):
                    print "Bem vindo de volta", name
                    gpio.output(g, gpio.LOW) # Open cabin
                    gpio.output(p, gpio.HIGH) # Stop power plug
                    #rec_flag += 1
                    fh = open("memory_"+str(n)+".txt","w")
                    fh.write("0\n")
                    fh.write("0\n")
                    fh.write("0")
                    fh.close()
                    # Stop the camera
                    cam.release()
                    # Close all windows
                    cv2.destroyAllWindows()
                    return True
            else:
                Id = "Unknown"

            print("Estou vendo: ", Id)

        unk_flag += 1
        # Display the video frame with the bounded rectangle
        #cv2.imshow('im',im)

        # If 'q' is pressed, close program
        #if(rec_flag == 5):
            # Stop the camera
         #   cam.release()
            # Close all windows
          #  cv2.destroyAllWindows()
           # return True
        if(unk_flag == 500):
            # Stop the camera
            cam.release()
            # Close all windows
            cv2.destroyAllWindows()
            return False