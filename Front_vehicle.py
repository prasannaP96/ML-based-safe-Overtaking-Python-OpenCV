import cv2
import numpy as np
import time
import socket
import imutils
C=0
D=0
S=1
Known_distance = 1500
Known_width = 182.5
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
cap = cv2.VideoCapture("E:\car detection\proj.mp4")
car_detector = cv2.CascadeClassifier("E:\car detection\cars.xml")
time_diff = 1/1000


def FocalLength(measured_distance, real_width, width_in_rf_image):
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


def Distance_finder(Focal_Length, real_car_width, car_width_in_frame):
    distance = (real_car_width * Focal_Length) / car_width_in_frame
    return distance


def car_data(image):
    car_width = 182

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cars = car_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, h, w) in cars:
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 1)
        car_width = w
        print("area",((x+w)*(y+h)))
    return car_width


def lap():
    host = '192.168.1.8'
    port = 12346
    s = socket.socket()
    s.connect((host, port))
    #print("listening")
    s.send(bytes('Data Processing \n Algorithm will take decision now ', 'utf-8'))
    s.close()
#lap()

low_gray = np.array([0, 5, 50])
high_gray = np.array([179, 50, 255])
low_white = np.array([0, 0, 0])
high_white = np.array([0, 0, 255])

ref_image = cv2.imread("E:\car detection\images\car.jpeg")

ref_image_car_width = car_data(ref_image)
Focal_length_found = FocalLength(Known_distance, Known_width, ref_image_car_width)
print(Focal_length_found)
#host = '192.168.1.8'
#port = 12347
#s = socket.socket()
#s.connect((host, port))

while True:
    t = time.time()
    _, frame = cap.read()
    car_width_in_frame = car_data(frame)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if car_width_in_frame != 0:
        F = Distance_finder(Focal_length_found, Known_width, car_width_in_frame)
        R = round(F/100)
        if F == 1500:
            F = 0
        #print(F / 100)
        G = (F - C) / ((time_diff + (time.time() - t)) * S)  # Velocity
        H = F - C
        J = (H - D) / (((time_diff + (time.time() - t)) ** 2) * S)  # Acceleration
        D = F - C
        C = (F / 100)
        if (F>=40):
            print("Condition satisfied for Distance")
            print("Now Checking for Velocity")
            if (G>=17):
                print("Checking for Acceleration")
                if (J<0):
                    print("Dont Over take")
                   # s.send(bytes("Dont Over take", 'utf-8'))
                elif (J>=3.5):
                    print('We need to accelerate to Overtake')
                    #s.send(bytes("Accelerate to Overtake", 'utf-8'))
                elif (J>0):
                    print("normally overtake")
                   # s.send(bytes("Overtake now", 'utf-8'))
            else:
                print("Do Not Overtake")
                #s.send(bytes("Do Not Overtake", 'utf-8'))
        else:
            print("Dont over take")
            #s.send(bytes("Dont over take", 'utf-8'))
        cv2.putText(frame, f"Distance = {round(F / 100)} metres", (50, 50), fonts, 1, (GREEN), 2)
        cv2.putText(frame, "Vel=%.2fm\sec" % (G/100), (frame.shape[1] - 240, frame.shape[0] - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "Acc=%.2fm\sec" % (J/100), (frame.shape[1] - 240, frame.shape[0] - 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("frame", frame)
    mask_1 = cv2.inRange(hsv_frame, low_gray, high_gray)
    mask_2 = cv2.inRange(hsv_frame, low_white, high_white)
    cnts = cv2.findContours(mask_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 500:
            #print(area)
            pass
            #cv2.imshow("frame_1", mask_1)
    cv2.imshow("frame_2", mask_2)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
s.close()
