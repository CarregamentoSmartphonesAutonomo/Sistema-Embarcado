import cv2
import numpy as np

# recognizer = cv2.createLBPHFaceRecognizer()
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read('trainner/trainner.yml')
# cascadePath = "haarcascade_frontalface_default.xml"
# faceCascade = cv2.CascadeClassifier(cascadePath);
faceCascade = cv2.CascadeClassifier(r'C:\Users\Arnol\Anaconda3\envs\PI2\Library\etc\haarcascades\haarcascade_frontalface_default.xml')

fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 255, 255)

cam = cv2.VideoCapture(0)
# font = cv2.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
        if(conf<50):
            if(Id==1):
                Id="Arnoldo"
            elif(Id==2):
                Id="Davi"
        else:
            Id="Unknown"
        # cv2.PutText(cv2.cv.fromarray(im),str(Id), (x,y+h),font, 255)
        cv2.putText(im, str(Id), (x,y+h), fontFace, fontScale, fontColor) 
    cv2.imshow('im',im) 
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

# ret, im = cam.read()
# locy = int(im.shape[0]/2) # the text location will be in the middle
# locx = int(im.shape[1]/2) #           of the frame for this example

# while True:
#     ret, im = cam.read()
#     cv2.putText(im, "Success!", (locx, locy), fontFace, fontScale, fontColor) 
#     cv2.imshow('im', im)
#     if cv2.waitKey(10) & 0xFF==ord('q'):
#         break

# cam.release()
# cv2.destroyAllWindows()