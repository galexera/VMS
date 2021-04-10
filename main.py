from flask import Flask, render_template, Response ,request
from camera import VideoCamera
from Takeimage import TakeImages
from Detectface import DetectFace
import cv2
from flask import redirect,url_for,flash
import csv
import numpy as np
import pandas as pd
import datetime
import time,os
from PIL import Image
from Takeimage import TakeImages
from nameid import c1
from itertools import zip_longest
from flask_mysqldb import MySQL
from sms import sendsms
 
res=""
obj =c1()

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'vms'

mysql = MySQL(app)
@app.route('/login', methods=['POST', 'GET'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username') 
        password = request.form.get('password')

        if username == 'root' and password == 'pass':
            message = "Correct username and password"
        else:
            message = "Wrong username or password"

    return render_template('train.html')

@app.route('/renderpass')
def renderpass():
    return render_template('OTpass.html')

@app.route('/otpass',methods = ['POST', 'GET'])
def otpass():

    print("OTPAS")
    if request.method == "POST":
        name = request.form['name']
        cmpny = request.form['cmpny']
        mno = request.form['mno']
        flat = request.form['flat']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO otpass VALUES(%s,%s,%s,%s)''',(name,cmpny,mno,flat))
        mysql.connection.commit()
        cur = mysql.connection.cursor() 

        cur.execute("""SELECT Phone_no FROM residents WHERE Flatno = %s""", (flat,))
        to = cur.fetchone()
        print(to)
        obj1 = sendsms()
        obj1.send(name,cmpny,mno,to)
        
        cursor.close()
        print("values added to sql")
        flash("USER HAS BEEN INFORMED")
        return render_template('train.html')


@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen1(camera,a,b,c):
    sampleNum = 0
    Id =a
    name =b
    Category =c
    
    # print("inside gen1",Id)
    # print("inusde gen1",name)
    # print("inside gen 1 ")
    global res
    res = "Images Saved for ID : " + str(Id) +" Name : "+ name   
    row = [Id , name , Category]
    with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    print(res)
    while True:
        sampleNum=sampleNum+1
        frame,Id,name,Category = camera.get_frame(sampleNum,Id,name,Category)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        if cv2.waitKey(100) & sampleNum>=60:
            with app.app_context(), app.test_request_context():
                 return redirect(url_for('train'))
            print("way passed")    
    
    print('Training Done')
    camera.__del__()    


def gen2(camera):
    col_names =  ['Id','Name','Category','Date','Time']
    attendance = pd.DataFrame(columns = col_names)
    ts = time.time() 
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
    Hour,Minute=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+".csv"
    attendance.to_csv(fileName,index=False)
    df1=pd.read_csv(fileName)
    tim=[]
    tim.append(timeStamp)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath); 
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
 
    while True:
            frame = camera.get_frame(attendance,df,faceCascade,recognizer)
        
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            ts = time.time() 
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
            Hour,Minute=timeStamp.split(":")
            attendance.to_csv(fileName,index=False)
            res=attendance
            res = "Attendance Taken"
            # print(res)
            # print('Completed','Congratulations ! Your attendance has been marked successfully for the day!!')
            attendance=attendance.drop_duplicates(subset=['Id','Time'],keep='first') 
            
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cap_img',methods = ['POST', 'GET'])
def cap_img():
    
    Id,name,Category = obj.f2()
    return Response(gen1(TakeImages(),Id,name,Category),
                    mimetype='multipart/x-mixed-replace; boundary=frame'),flash(res)

@app.route('/detect_face')
def detect_face():
    return Response(gen2(DetectFace()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/json',methods = ['POST', 'GET'])
def json():
    if request.method == "POST": 
        # getting input with name = fname in HTML form 
        Id = request.form.get("fname") 
        # getting input with name = lname in HTML form  
        name = request.form.get("lname")
        Category = request.form.get("categ")
        global obj
        obj = c1()
        obj.f1(Id,name,Category)
    return render_template('json.html')

@app.route('/train')
def train():
    return render_template('train.html')

@app.route('/TrainImage')
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    path="TrainingImage"
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]   
    faces=[]
    Ids=[]
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        # print(imageNp)
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # print(Id)
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id) 

    recognizer.train(faces, np.array(Ids))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"
    print(res)
    print('Completed','Your model has been trained successfully!!')
    return redirect(url_for('red'))

@app.route("/red")
def red():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    path="D:\ADITYA\projects\DeepBlue\VMS-SEMIFINAL\TrainingImage"
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]   
    faces=[]
    Ids=[]
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        # print(imageNp)
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # print(Id)
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id) 

    recognizer.train(faces, np.array(Ids))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"
    print(res)
    print('Completed','Your model has been trained successfully!!')
    return render_template("train.html")

@app.route("/new_form")
def new_form():
    return render_template('new_form1.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='192.168.0.187', debug=True)

