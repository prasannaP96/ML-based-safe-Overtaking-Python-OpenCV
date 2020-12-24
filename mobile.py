import socket
def lap():
    host = '192.168.1.6'
    port = 12345
    s = socket.socket()
    s.connect((host, port))
    message = input("")
    s.send(bytes(message, 'utf-8'))
    s.close()
def rpi():
    host = "192.168.1.8"
    port = 12347
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()
    while True:   #talk(c.recv(1024).decode()) 
        filename = str("Ericsson.jpeg")
        file = open(filename,'wb')
        file_data = c.recv(115200)
        print("picture received")
        file.write(file_data)
        print(c.recv(1024).decode())
lap()
rpi()
