import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
from tensorflow.keras import layers,models
import matplotlib.pyplot as plt
import io
import socket
import struct
import time
import pickle
import zlib
import glob
import numpy as np
import socket
import datetime
import cv2
overtake = glob.glob("E:\\Ericsson\\ML\\model\\overtake\\*.*")
dont_overtake = glob.glob("E:\\Ericsson\\ML\\model\\dont_overtake\\*.*")
data =[]
labels =[]
for i in overtake:
    image=tf.keras.preprocessing.image.load_img(i, color_mode='rgb', target_size= (250,250))
    image=np.array(image)
    data.append(image)
    labels.append(0)
for i in dont_overtake:
    image=tf.keras.preprocessing.image.load_img(i, color_mode='rgb', target_size= (250,250))
    image=np.array(image)
    data.append(image)
    labels.append(1)
    print(len(data))
data = np.array(data)
labels = np.array(labels)
classes = ["Dont'Overtake","Overtake Now"]
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.01,
                                                random_state=42)
model = models.Sequential([
    layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu', input_shape=(250, 250, 3)),
    layers.MaxPooling2D((3, 3)),
    
    layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D((3, 3)),
    
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(2, activation='softmax')
])
X_train = X_train/255.0
X_test = X_test/255.0
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(X_train,y_train,epochs=10)
def lap():
    host = '192.168.1.7'
    port = 12346
    s = socket.socket()
    s.connect((host, port))
    #print("listening")
    s.send(bytes('Data Processing \n Algorithm will take decision now ', 'utf-8'))
    s.close()
lap()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.8', 12347))
connection = client_socket.makefile('wb')
location = "E:\\Ericsson\\ML\\traffic_1.mp4"
cap = cv2.VideoCapture(location)
img_counter = 0
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
while True:    
    _,frame = cap.read()
    frame_1 = np.array(frame)
    frame_2 = frame_1.reshape(-1,250,250,3)
    frame_3 = frame_2 / 255.0
    out = np.argmax(model.predict(frame_3))
    print((classes[out]))     
    cv2.putText(frame,classes[out],(frame_2.shape[2]-230,frame_2.shape[1]-50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0) ,2)
    cv2.imshow("frame_1",frame)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)
    #print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
    if cv2.waitKey(500) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
