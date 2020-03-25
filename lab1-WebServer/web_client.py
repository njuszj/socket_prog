from socket import *
import sys
import time

if len(sys.argv) < 3:
    print('参数不足')
    sys.exit()

address = sys.argv[1]  # 通过sys的argv函数获取参数
port = int(sys.argv[2])
filename = sys.argv[3]
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((address, port))

message = 'GET /' + filename  # 使用GET方法

clientSocket.send(message.encode('utf-8'))  # 发送请求
page = ''
while True:
    recv = clientSocket.recv(1024).decode('utf-8')
    page += recv
    if not recv:
        clientSocket.close()      # 当没有消息时关闭连接
        break  

print(page) 