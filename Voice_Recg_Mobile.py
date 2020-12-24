import socket
import speech_recognition as sr
import pyttsx3
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
def talk(text):
    engine.say(text)
    engine.runAndWait()
def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            #command = command.lower()
            print(command)
    except:
        pass
    return command
def lap():
    host = '192.168.1.7'
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()
    c.send(bytes(take_command() , 'utf-8'))
    c.close()
def rpi():
    host = "192.168.1.7"
    port = 12347
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()
    while True:
        talk(c.recv(1024).decode())
    c.close()
lap()
rpi()
