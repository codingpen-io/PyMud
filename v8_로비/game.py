f = open('welcome.txt')
welcome_message = f.read()
f.close()

users_in_lobby = []

user_password = {}
f = open('passwords.txt')
while True:
    line = f.readline()
    if not line:  # 파일 끝까지 읽으면 더 읽을게 없음
        break
    user_name, password = line.split()
    user_password[user_name] = password

f.close()

state_ask_user_name = 'state_ask_user_name'
state_ask_password = 'state_ask_password'
state_lobby = 'state_lobby'


class User:
    def __init__(self, socket, addr) -> None:
        self.socket = socket
        self.addr = addr
        self.state = state_ask_user_name
        print("addr ", self.addr)
        self.send(welcome_message)
        self.send("유저명을 입력하세요")

    def send(self, text):
        text += '\n'
        self.socket.sendall(text.encode('utf-8'))

    def run(self):
        while True:
            data = self.socket.recv(1024)
            # 에코를 막았을 때 돌아오는 응답
            if not data or data == b'\xff\xf4\xff\xfd\x06':
                self.socket.shutdown()
                self.socket.close()
                break
            line = data.decode()
            if '\r\n' in line:
                line = line.replace("\r\n", "")
                self.onInput(line)
            line += line
            # try:
            # except:
            #     print("except")
            #     break

        self.socket.close()

    def onInput(self, input):
        if self.state == state_ask_user_name:
            self.user_name = input
            self.state = state_ask_password
            self.send(f'{self.user_name} 님 암호를 입력하세요')
        elif self.state == state_ask_password:
            if self.user_name in user_password and user_password[self.user_name] == input:
                self.send('로그인 성공')
                self.state = state_lobby
                users_in_lobby.append(self)
            else:
                self.state = state_ask_user_name
                self.send('틀린 암호입니다\n이름을 입력하세요')
        elif self.state == state_lobby:
            self.broadcast(input)

    def broadcast(self, message):
        for user in users_in_lobby:
            if user != self:
                user.send(message)
