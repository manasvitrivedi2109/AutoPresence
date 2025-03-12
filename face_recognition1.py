import face_recognition
import cv2
import numpy as np
import os
import smtplib
import imghdr
import xlwt
from xlwt import Workbook
from datetime import date
import xlrd,xlwt
from xlutils.copy import copy as x1_copy

CurrentFolder = os.getcwd()
image = CurrentFolder
image2 = CurrentFolder
video_capture = cv2.VideoCapture(1)

person1_name = "Manasvi Trivedi"
person1_image = face_recognition.load_image_file(image)
person1_face_encoding = face_recognition.face_encodings(person1_image)

person2_name = "Aayushi Soni"
person2_image = face_recognition.load_image_file(image)
person2_face_encoding = face_recognition.face_encodings(person2_image)

known_face_encodings = [person1_face_encoding,person2_face_encoding]
known_face_name = [person1_name,person2_name]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

rb = xlrd.open_workbook('attendance_excel.xls',formatting_info=True)
wb = x1_copy(rb)
inp = input("Please give current subject lecture name: ")
sheet1 = wb.add_sheet(inp)
sheet1.write(0,0,'Name/Date')
sheet1.write(0,1,str(date.today()))
row = 1
col = 0
already_attendance_taken = ""
while True:
    ret,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx = 0.25,fy = 0.25)
    rbg_small_frame = small_frame[:,:,::-1]
    if process_this_frame:
        face_locations = face_recognition.face_locations(rbg_small_frame)
        face_encodings = face_recognition.face_encodings(rbg_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
            name = "Unknown"
            
            face_distances = face_recognition.face_distances(known_face_encodings,face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_name[best_match_index]
            face_names.append(name)
            if((already_attendance_taken != name) and (name != "Unknown")):
                sheet1.write(row,col,name)
                col = col+1
                sheet1.write(row,col,"Present")
                row = row +1
                col = 0
                print("Attendance taken")
                wb.save('attendance_excel.xls')
                
            




