import os
import cv2
import time

cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier(r'C:\Users\Arnol\Anaconda3\envs\PI2\Library\etc\haarcascades\haarcascade_frontalface_default.xml')

# Criando Folder do DataSet
if (not os.path.isdir("dataSet")):
    os.mkdir('dataSet')

# Importando o ID da pessoa
Id=input('Enter your ID: ')
sampleNum=0

# Criando o Banco de Dados
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
        #incrementing sample number 
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w]) #

        cv2.imshow('frame',img)
    #wait for 100 miliseconds 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum>100:
        break

cam.release()
cv2.destroyAllWindows()