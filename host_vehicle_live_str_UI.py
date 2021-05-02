import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
from tkinter import *
import tkinter as tk
var=""
#out=""
host = '192.168.1.7' # Your PC IP Address 
port = 12345
s = socket.socket()
s.connect((host, port))
root = tk.Tk()


def write_slogan():
    print("Shall I overtake Now!")

def store():
    global var
    var = "shall i overtake?"
    print("Shall I overtake Now!")
    s.send(bytes(str(var), 'utf-8'))
    s.close()
    root.destroy()


frame = tk.Frame(root)
slogan = tk.Button(frame, text="shall I overtake?", command=write_slogan)
but = tk.Button(command=store, text="shall I overtake?")

frame.pack()
but.pack()
root.mainloop()
host = "192.168.1.8" # Your PC IP Address sir
port = 12347
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((host,port))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
#print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        #print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    #print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    #print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    if cv2.waitKey(500) == ord("q"):
        break
cv2.destroyAllWindows()
