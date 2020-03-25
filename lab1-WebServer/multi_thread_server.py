# 处理多次请求

from socket import *
import time
import sys
import threading

# 建立列表保存客户端连接socket
connection_pool = [None] * 50
index = 0


# 将基础代码中的处理消息的部分封装成函数
# 并添加线程启动/结束的信息
def recvClient(connectionSocket):
    print(threading.current_thread().getName() + ' 线程启动')
    try:
        message = connectionSocket.recv(1024)  # 读取消息(请求)
        print('收到请求 ',message[0:30])
        filename = message.split()[1]  # 获取文件名
        f = open(filename[1:])  # 过滤斜杠
        outputdata = f.read()   # 读取内容
        # 发送HTTP请求头
        connectionSocket.send("HTTP/1.1 201 OK\r\n\r\n".encode('utf-8'))
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode('utf-8'))
        connectionSocket.send("\r\n".encode('utf-8'))
        print('返回了资源页面')
    except:
        # 发送404消息
        f = open("404.html")
        outputdata = f.read()
        connectionSocket.send("HTTP/1.1 404 NOT OK\r\n\r\n".encode('utf-8'))
        connectionSocket.send(outputdata.encode('utf-8'))
        print('返回了404页面')
    finally:
        connectionSocket.close()
    print(threading.current_thread().getName() + ' 线程结束')


serverSocket = socket(AF_INET, SOCK_STREAM)
host = '0.0.0.0'
port = 12345
serverSocket.bind((host, port))  # 绑定地址
serverSocket.listen(5)  # 开始监听
print('多线程网络服务器开始监听...')
while index < 50:
    connection_pool[index], addr = serverSocket.accept()
    index += 1
    # 创建新的线程
    t = threading.Thread(target=recvClient, args=(connection_pool[index-1], ))
    t.start()
    print('主线程继续监听...')
    


