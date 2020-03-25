from socket import *
import sys
import random

serverSocket = socket(AF_INET, SOCK_STREAM)
host = '0.0.0.0'
port = 12345
print('端口', port)
serverSocket.bind((host, port))  # 绑定地址
serverSocket.listen(5)  # 开始监听

print(serverSocket)

while True:
    #　Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)  # 读取消息(请求)
        print(message)
        filename = message.split()[1]  # 获取文件名
        f = open(filename[1:])  # 过滤斜杠
        outputdata = f.read()   # 读取内容
        print(outputdata)
        # 发送HTTP请求头
        connectionSocket.send("HTTP/1.1 201 OK\r\n\r\n".encode('utf-8'))
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode('utf-8'))
        connectionSocket.send("\r\n".encode('utf-8'))
    except IOError:
        f = open("404.html")
        outputdata = f.read()
        connectionSocket.send("HTTP/1.1 201 OK\r\n\r\n".encode('utf-8'))
        connectionSocket.send(outputdata.encode('utf-8'))
        connectionSocket.send("\r\n".encode('utf-8'))
    except IndexError:
        connectionSocket.send("请求的资源不存在\r\n\r\n".encode('utf-8'))
    finally:
        connectionSocket.close()

serverSocket.close()
sys.exit()

