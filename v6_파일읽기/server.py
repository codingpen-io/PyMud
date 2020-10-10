# 쉘 창 여는 법
# Cmd+Shift+P(Ctrl+Shift+P)
# open shell
import socket
import threading

HOST = '0.0.0.0'
# HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

server.listen()

f = open('welcome.txt')
welcome_message = f.read()


def handle_client(client, addr):
    print(f"New connection from {addr}")
    client.sendall(welcome_message.encode('utf-8'))
    while True:
        data = client.recv(1024)
        if not data:
            break

        print("received", addr, data.decode('utf-8'))
    client.close()


while True:
    client, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(client, addr))
    thread.start()
    print(f"Active connection {threading.activeCount()-1}")

server.close()
