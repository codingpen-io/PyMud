# 쉘 창 여는 법
# Cmd+Shift+P(Ctrl+Shift+P)
# open shell
import socket


HOST = '127.0.0.1'
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

server.listen()

client, addr = server.accept()
print("connection from", addr)

while True:
    data = client.recv(1024)
    # check data is empty
    # data == None or len(data) == 0
    if not data:
        break
    print("received", addr, data.decode())

    client.sendall(data)

client.close()
server.close()
