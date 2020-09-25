# 쉘 창 여는 법
# Cmd+Shift+P(Ctrl+Shift+P)
# open shell
import socket
import os

HOST = '0.0.0.0'
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

server.listen()


while True:
    client, addr = server.accept()
    print("connection from", addr)

    while True:
        data = client.recv(1024)
        # check data is empty
        # data == None or len(data) == 0
        if not data:
            break
        print("received", addr, data.decode())

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        f = open(path)
        content = f.read()
        response = 'HTTP/1.1 200 OK\n'
        response += content
        client.sendall(response.encode())

    client.close()

server.close()

'''
참고 : https://www.tutorialspoint.com/http/http_responses.htm

HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: Apache/2.2.14 (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Length: 88
Content-Type: text/html
Connection: Closed
<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>


HTTP/1.1 404 Not Found
Date: Sun, 18 Oct 2012 10:36:20 GMT
Server: Apache/2.2.14 (Win32)
Content-Length: 230
Connection: Closed
Content-Type: text/html; charset=iso-8859-1
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
   <title>404 Not Found</title>
</head>
<body>
   <h1>Not Found</h1>
   <p>The requested URL /t.html was not found on this server.</p>
</body>
</html>
'''
