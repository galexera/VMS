from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2,os
from PIL import Image
import csv
import numpy as np
import pandas as pd
import datetime
import time
   
font = cv2.FONT_HERSHEY_SIMPLEX 

class DetectFace(object):   
    def __init__(self):
        self.video = cv2.VideoCapture(0)
           
    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self,attendance,df,faceCascade,recognizer):            
        df=pd.read_csv("StudentDetails\StudentDetails.csv")
        ret, im =self.video.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        recognizer.read("TrainingImageLabel\Trainner.yml")
           
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                  
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
                aa=df.loc[df['Id'] == Id]['Name'].values
                cc=df.loc[df['Id'] == Id]['Category'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,cc,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  

            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2) 

        ret, jpeg = cv2.imencode('.jpg', im)           
        return jpeg.tobytes()
        

                    
         
    