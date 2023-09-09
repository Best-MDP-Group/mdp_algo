from socket import *

s = socket(AF_INET, SOCK_STREAM)
# connect to server
s.connect(('192.168.31.31', 8000))
print("connected to server")

while True:
    send = bytes("hello world!", 'utf-8')
    s.send(send)
    msg = s.recv(1024)
    if not msg:
        break
    print("Message from server : " + msg.decode("utf-8"))



