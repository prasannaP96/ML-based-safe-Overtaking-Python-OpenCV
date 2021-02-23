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
ser = c.recv(1024).decode()
# pygame.init()
#
# gw = pygame.display.set_mode((500, 500))
# pygame.display.set_caption("Your title")
# white = (255, 255, 255)
# font = pygame.font.SysFont(None, 40)
#
#
# def printsc(text, x, y, color):
#     screen_text = font.render(text, False, color)
#     gw.blit(screen_text, (x, y))
#
#
# while True:
#     gw.fill(white)
#     printsc(out, 10, 10, (0, 0, 0))
#     pygame.display.update()
#     for e in pygame.event.get():
#         if e.type == pygame.QUIT:
#             quit()

window = Tk()
window.title("Ericsson")
frame_1 = Frame(window)
message = Entry(window,width=50)
message.insert(0,'Command: ')
frame_1.pack()
def recvmessage():
#while loop should come there...i took out that from here...
    #ser =  # this one should get printed in tkinter
    print(ser)
    message.insert(END,"\n"+ser)
    message.pack()

        #window.update()

#window.after(100000,recvmessage)
#recvmessage(window)
recvmessage()
window.mainloop()
# window.mainloop()
#while True:
    #recvmessage()
