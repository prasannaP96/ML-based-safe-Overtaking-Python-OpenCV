import numpy as np
import os
import imutils
import cv2
import glob
import pandas as pd
import xlrd
C=0
D=0
def find_marker(image):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 35, 125)
    # find the contours in the edged image and keep the largest one;
    # we'll assume that this is our piece of paper in the image
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    # compute the bounding box of the of the paper region and return it
    return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the maker to the camera
    return (knownWidth * focalLength) / perWidth

#appended_data = pd.DataFrame()
KNOWN_DISTANCE = 12
KNOWN_WIDTH = 8.5
time_diff = 3
image = cv2.imread("E:\Ericsson\images\pic24.jpeg")
#df = pd.read_csv("E:\Ericsson\Ericsson.csv")
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    marker = find_marker(frame)
    inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])
    box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
    box = np.int0(box)
    cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
    F = round((inches/12),2)
    print("Distance",F)
    print("Vel",(F-C)/time_diff)
    G = (F-C)/time_diff
    H = F-C
    print("Acc",(H-D)/((time_diff)*2))
    J = ((H-D)/((time_diff)*(time_diff)))
    D = F-C
    C = (inches / 12)
    #if (F>=40):
        #print("Condition satisfied for Distance")
        #print("Now Checking for Velocity")
        #if (G>=17):
            #print("Checking for Acceleration")
            #if (J<0):
                #print("Dont Over take")
            #elif (J>=3.5):
                #print('We need to accelerate to Overtake')
            #elif (J>0):
                #print("normally overtake")
        #else:
            #print("Do Not Overtake")
    #else:
        #print("Dont over take")
    #print(len(F))
    df = pd.DataFrame({'Distance': [F],'Velocity':[G]})
    #writer = pd.ExcelWriter('Ericsson.xlsx', engine='xlsxwriter')
    #df.to_excel(writer, sheet_name='Sheet1')
    cv2.putText(frame, "Dis=%.2fft" % (inches / 12), (frame.shape[1] - 300, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                1.5, (0, 255, 255), 2)
    cv2.putText(frame, "Vel=%.2fft\sec" %G, (frame.shape[1] - 400, frame.shape[0] - 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)

    cv2.putText(frame, "Acc=%.2fft\sec" %J, (frame.shape[1] - 400, frame.shape[0] - 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
    cv2.imshow("image", frame)
    #writer.save()
    key = cv2.waitKey(3000)
    print()
    if key == 27:
        break
cv2.destroyAllWindows()