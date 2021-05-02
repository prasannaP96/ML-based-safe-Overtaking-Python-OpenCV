import socket
def mob():
    host = "192.168.1.6"
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print('listening')
    c, addr = s.accept()
    print(c.recv(1024).decode())
    c.close()
def rpi():
    host = "192.168.1.6"
    port = 12346
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print('listening')
    c, addr = s.accept()
    print(c.recv(1024).decode())
    c.close()
mob()
rpi(
