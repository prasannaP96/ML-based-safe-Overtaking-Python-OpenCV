import socket
def mob():
    host = '192.168.1.7'
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()
    c.send(bytes('shall i overtake now', 'utf-8'))
    c.close()
def rpi():
    host = "192.168.1.7"
    port = 12347
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    c, addr = s.accept()
    while True:
        print(c.recv(1024).decode())
    c.close()
mob()
rpi()