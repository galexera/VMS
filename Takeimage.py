from flask import Flask, render_template, Response, redirect, url_for
import cv2
import csv
import numpy as np
import pandas as pd
import datetime
import time
from nameid import c1

detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

ds_factor = 0.6

class TakeImages(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        # self.video.stop()
        self.video.release()
        cv2.destroyAllWindows()
        # print("Executed")

    def get_frame(self, sampleNum, a, b, c):
        ret, img = self.video.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        Id = a
        name = b
        Category = c

        # print("inside ti", Id)
        # print("inside ti", name)
        # # Id =self.Id

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite(
                "TrainingImage\ " + name + "." + str(Id) + '.' + Category +
                '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes(), Id, name, Category
