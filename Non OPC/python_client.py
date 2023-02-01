import socket

HOST = '142.244.38.72'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("connected")
    print("Sending data")
    s.sendall(b'Hello World')
    print("Receiving data")
    data = s.recv(1024)
    print('Echoing: ', repr(data))
