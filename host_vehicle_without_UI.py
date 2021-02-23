import tkinter as tk
from tkinter import *
import socket
#import pygame

var=""
#out=""
host = '192.168.1.8' # Your PC IP Address sir
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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print('listening')
c, addr = s.accept()
while True:
    print(c.recv(1024).decode())
