import csv
import numpy as np
import pandas as pd

df1=pd.read_csv("C:/Users/ADMIN/Desktop/VMS/VideoStreamingFlask2/Attendance/Attendance_2021-03-13_19-52.csv")

Id = df1.loc[:,'Id'].values
print(Id)

Ids = 21
tim = df1.loc[:,'Time'].values
print(tim)

Id=21
tim1 = df1.loc[df1['Id'] == Id]['Time'].values
print(tim1)

tim1[21]
