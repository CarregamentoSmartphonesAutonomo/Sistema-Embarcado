import os
import sys

# Import OpenCV2 for image processing
import cv2

# Import for GPIO
import RPi.GPIO as gpio
import time

def cadastro():

    # Choose the cabin for your smartphone
    fh1 = open("memory_1.txt","r+")
    fh2 = open("memory_2.txt","r+")
    fh3 = open("memory_3.txt","r+")
    op1 = fh1.readline(2)
    op2 = fh2.readline(2)
    op3 = fh3.readline(2)
    fh1.close()
    fh2.close()
    fh3.close()

    if(op1 == '1' and op2 == '1' and op3 == '1'):
        print("No cabins available...\n")
        return False

    # For each person, one face id and a name
    face_id = input('Enter your ID: ')
    name = input("Enter your name: ")

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
            cv2.imshow('frame', image_frame)

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

def colocar_na_cabine():

    # Configuring GPIO
    gpio.setmode(gpio.BOARD)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

    while(True):
        cab_id = input('Enter the cabin for your smartphone (1 to 3): ')
        
        if(cab_id == 1):
            if(op1 == '1'):
                print("This cabin is not available...\n")
            else:
                fh1 = open("memory_1.txt","w")
                fh1.write(str(face_id)+"\n")
                fh1.write("1\n")
                fh1.write(name+"\n")
                fh1.close()
                gpio.output(11, gpio.LOW)
                time.sleep(3)
                gpio.output(11, gpio.HIGH)
                cab_flag = 1
        elif(cab_id == 2):
            if(op2 == '1'):
                print("This cabin is not available...\n")
            else:
                fh2 = open("memory_2.txt","w")
                fh2.write(str(face_id)+"\n")
                fh2.write("1\n")
                fh2.write(name+"\n")
                fh2.close()
                gpio.output(13, gpio.LOW)
                time.sleep(3)
                gpio.output(13, gpio.HIGH)
                cab_flag = 1
        elif(cab_id == 3):
            if(op3 == '1'):
                print("This cabin is not available...\n")
            else:
                fh3 = open("memory_3.txt","w")
                fh3.write(str(face_id)+"\n")
                fh3.write("1\n")
                fh3.write(name+"\n")
                fh3.close()
                gpio.output(15, gpio.LOW)
                time.sleep(3)
                gpio.output(15, gpio.HIGH)
                cab_flag = 1
        else:
            print("Invalid input, try again...\n")
            return False

        if(cab_flag == 1):
            break

    # Undo GPIO configuration
    gpio.cleanup()

    return True