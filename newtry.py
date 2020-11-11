import numpy as np
import os
import imutils
import cv2
import glob
#import pandas as pd
#import xlrd
import time
#import smtplib
import socket
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
#from selenium import webdriver
from twilio.rest import Client

list_1 = []
list_2 = []
list_3 = []
C=0
D=0
P=0
Q=0
S=1
def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(gray, 35, 125)
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    # compute the bounding box of the of the paper region and return it
    return cv2.minAreaRect(c)
def find_marker_1(image_1):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(gray, 35, 125)
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    conts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    conts = imutils.grab_contours(conts)
    d = max(conts, key=cv2.contourArea)
    # compute the bounding box of the of the paper region and return it
    return cv2.minAreaRect(d)
def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

KNOWN_DISTANCE = [12,6]
KNOWN_WIDTH = [8.5,0.5]
#real_Height = 11.6929
#image_Height = 720
#object_Height = 1122.519685
#sensor_Height = 0.1968
time_diff = 1
low_white = np.array([0,0,0])
high_white = np.array([0,0,255])
low_gray = np.array([0,5,50])
high_gray = np.array([179, 50, 255])
image = cv2.imread("E:\Ericsson\images\pic24.jpeg")
image_1 = cv2.imread("E:\Ericsson\images\mobile.jpeg")
#print(image.shape)
marker = find_marker(image)
marker_1 = find_marker(image_1)
focalLength = (marker[1][0] * KNOWN_DISTANCE[0]) / KNOWN_WIDTH[0]
focalLength_1 = (marker_1[1][0] * KNOWN_DISTANCE[1]) / KNOWN_WIDTH[1]
video = cv2.VideoCapture(0)
count = 1
#server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#ip = socket.gethostbyname(socket.gethostname())
#port = 1234
#address = ((ip,port))
#server.bind(address)
#server.listen(0)
#print("socket is listening")
#client, addr = server.accept()
#print("connected")
account_sid = 'AC19f9340f70eb57a4d02ff9b27fc3bc4d'
auth_token = 'bcec039e7b8eabe7a9bf8392e44cc0a1'
client = Client(account_sid, auth_token)
driver = webdriver.Chrome("C:\webdrivers\chromedriver")
driver.get('http://web.whatsapp.com')
name = input('Enter the name of user or group : ')
user = driver.find_element_by_xpath("//span[@title='Twilio']".format(name))
user.click()
msg_box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
msg_box.send_keys("Shall i Overtake now?")
driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()

while True:


    t = time.time()
    check, frame = video.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    marker = find_marker(frame)
    marker_1 =find_marker_1(frame)
    mask = cv2.inRange(hsv_frame, low_white, high_white)
    mask_1 = cv2.inRange(hsv_frame, low_gray, high_gray)
    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts_1 = cv2.findContours(mask_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts_1 = imutils.grab_contours(cnts_1)
    inches = distance_to_camera(KNOWN_WIDTH[0], focalLength, marker[1][0])
    inches_1 = distance_to_camera(KNOWN_WIDTH[1], focalLength_1, marker_1[1][0])
    box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
    box = np.int0(box)
    box_1 = cv2.cv.BoxPoints(marker_1) if imutils.is_cv2() else cv2.boxPoints(marker_1)
    box_1 = np.int0(box_1)
    range = cv2.contourArea(box)
    range_1 = cv2.contourArea(box_1)
    if(17500<range<100900):

        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
        #cv2.drawContours(frame, [box_1], -1, (255, 0, 0), 2)

        F = round((inches/12),2)
        #print(time.time()-t)
        list_1.append(F)
        #print("Distance_1", F)
        G = (F-C)/((time_diff+(time.time()-t))*S)# Velocity
        #print("Vel_1", G)
        list_2.append(G)
        H = F-C
        #print("Acc",(H-D)/((time_diff))
        J = (H-D)/(((time_diff +(time.time()-t))**2)*S) # Acceleration
        #print("Acc_1", J)
        list_3.append(J)
        #t = time.time()
        D = F-C
        C = (inches / 12)
        for c in cnts:
            area = cv2.contourArea(c)
            #print(area)
            if (area > 5):
                pass
                #print("white")
                #list_4.append("white")
        if (F>=40):
            #print("Condition satisfied for Distance")
            #print("Now Checking for Velocity")
            if (G>=17):
                #print("Checking for Acceleration")
                if (J<0):
                    print("Dont Over take")
                    message = client.messages \
                        .create(
                        body="Don't Overtake",
                        from_='whatsapp:+14155238886',
                        to='whatsapp:+919944334767'
                    )
                    #client.send(bytes("Dont Overtake Now!", "utf-8"))
                elif (J>=3.5):
                    print('Accelerate to Overtake')
                    #c.send(bytes('Accelerate to Overtake', 'utf-8'))
                    #client.send(bytes("Accelerate to overtake", "utf-8"))
                elif (J>0):
                    message = client.messages \
                        .create(
                        body="Overtake Now",
                        from_='whatsapp:+14155238886',
                        to='whatsapp:+919944334767'
                    )
                    print("normally overtake")
                    #c.send(bytes('Overtake Now', 'utf-8'))
                    #client.send(bytes("Overtake Now", "utf-8"))
            else:
                message = client.messages \
                    .create(
                    body="Don't Overtake",
                    from_='whatsapp:+14155238886',
                    to='whatsapp:+919944334767'
                )
                print("Do Not Overtake")
                #c.send(bytes("Don't Overtake Now", 'utf-8'))
                #client.send(bytes("Dont' Overtake Now", "utf-8"))
        else:
            #print("Dont over take")
            message = client.messages \
                .create(
                body="Don't Overtake",
                from_='whatsapp:+14155238886',
                to='whatsapp:+919944334767'
            )
            #client.send(bytes(" Don't Overtake Now", "utf-8"))
        cv2.putText(frame, "Dis=%.2fft" % (inches / 12), (frame.shape[1] - 240, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2)
        cv2.putText(frame, "Vel=%.2fft\sec" %G, (frame.shape[1] - 240, frame.shape[0] - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame, "Acc=%.2fft\sec" %J, (frame.shape[1] - 240, frame.shape[0] - 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255,0),2)
        count = 1
    elif (1600<range_1<5500):
        for c in cnts_1:
            area_1 = cv2.contourArea(c)
            if (area_1 > 100000):
                print("Black")
                #list_8.append(print("Black"))
        cv2.drawContours(frame, [box_1], -1, (255, 0, 0), 2)

        F_1 = round((inches_1 / 12), 2)
        # print("Distance",F)
        # print("Vel",(F-C)/time_diff)
        #print(time.time()-t)
        #print("Dist_2",F_1)
        G_1 = (F_1 -P) / ((time_diff + (time.time() - t)) * S)  # Velocity
        #print("Vel_2",G_1)
        H_1 = F_1 - P
        # print("Acc",(H-D)/((time_diff)))
        J_1 = (H_1 - Q) / (((time_diff + (time.time() - t)) ** 2) * S)  # Accelerati
        #print("Acc_2",J_1)
        t = time.time()
        Q = F_1 -P
        P = (inches_1 / 12)
        if (F_1 >= 40):
            #print("Condition satisfied for Distance")
            #print("Now Checking for Velocity")
            if (G_1 >= 17):
                #print("Checking for Acceleration")
                if (J_1 < 0):
                    message = client.messages \
                        .create(
                        body="Don't Overtake",
                        from_='whatsapp:+14155238886',
                        to='whatsapp:+919944334767'
                    )
                    print("Dont Over take")
                    #c.send(bytes("Don't Overtake ", 'utf-8'))
                    #client.send(bytes("Don't Overtake Now", "utf-8"))
                elif (J_1 >= 3.5):
                    message = client.messages \
                        .create(
                        body="Accelerate to Overtake",
                        from_='whatsapp:+14155238886',
                        to='whatsapp:+919944334767'
                    )
                    print('We need to accelerate to Overtake')
                    #c.send(bytes("Accelerate to overtake", 'utf-8'))
                    #client.send(bytes("Accelerate to Overtake Now", "utf-8"))
                elif (J_1 > 0):
                    message = client.messages \
                        .create(
                        body="Overtake Now",
                        from_='whatsapp:+14155238886',
                        to='whatsapp:+919944334767'
                    )
                    print("normally overtake")
                    #c.send(bytes("Overtake Now", 'utf-8'))
                    #client.send(bytes("Overtake Now", "utf-8"))
            else:
                #print("Do Not Overtake")
                message = client.messages \
                    .create(
                    body="Don't Overtake",
                    from_='whatsapp:+14155238886',
                    to='whatsapp:+919944334767'
                )
                #c.send(bytes("Don't Overtake ", 'utf-8'))
                #client.send(bytes("Don't Overtake Now", "utf-8"))
        else:
            message = client.messages \
                .create(
                body="Don't Overtake",
                from_='whatsapp:+14155238886',
                to='whatsapp:+919944334767'
            )
            print("Dont over take")
            #c.send(bytes("Don't Overtake Now", 'utf-8'))
            #client.send(bytes("Don't Overtake Now", "utf-8"))
        cv2.putText(frame, "Dis=%.2fft" % (inches_1 / 12), (frame.shape[1] - 230, frame.shape[0] - 140),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2)
        cv2.putText(frame, "Vel=%.2fft\sec" % G_1, (frame.shape[1] - 230, frame.shape[0] - 170),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.putText(frame, "Acc=%.2fft\sec" % J_1, (frame.shape[1] - 230, frame.shape[0] - 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        count = 1
    cv2.imshow("image",frame)
    key = cv2.waitKey(1000)
    print()

    if key == 27:
        break
#p = pd.DataFrame()
#p['Distance'] = list_1
#p['Velocity'] = list_2
#p['Acceleration'] = list_3
#p.to_csv('Data1.csv')
cv2.destroyAllWindows()