import socket

HOST = "127.0.0.1"
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
s.sendall('안녕 서버'.encode())
s.close()
