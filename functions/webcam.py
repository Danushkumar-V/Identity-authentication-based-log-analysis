from tokenize import Name
from tracemalloc import start
from functions import detect 
import cv2
import face_recognition
import numpy as np
import streamlit as st
from functions import add
import time
name = ""

def showvideo(encoded_list , imgclasses):

    Frame_window = st.image([])
    cap = cv2.VideoCapture(0)
    # address="http://192.168.1.12:8080/video"
    # cap.open(address)
    while (True):
        encodesCurFrame, facesCurFrame, img = detect.detectface(cap)
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encoded_list, encodeFace)
            faceDis = face_recognition.face_distance(encoded_list, encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
            
            
            if matches[matchIndex]:
                name = imgclasses[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                frame = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                frame = cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                frame = cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                print(name)
                add.add_csv(name)
                Frame_window.image(frame)
