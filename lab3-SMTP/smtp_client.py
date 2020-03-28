from socket import *
import base64
import sys
import os

def img2base64(path):
    # 将图片转换为Base64编码
    with open(path, "rb") as f:
        base64_data = base64.b64encode(f.read())
        return base64_data
    return 0


msg = "\r\nI love computer networks!\r\n"  # 正文前需要空一行
endmsg = "\r\n.\r\n"  # 正文结束标志

mailserver = "smtp.163.com"  # 网易邮箱smtp服务

clientSocket = socket(AF_INET, SOCK_STREAM)
address = gethostbyname("smtp.163.com")
clientSocket.connect((address,25))

recv = clientSocket.recv(1024).decode()
if recv[:3] != '220':
    print('没有收到220应答，连接失败')
else:
    print(recv)

heloCommand = 'HELO BoB\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()

if recv1[:3] != '250':
    print('没有收到250应答，HELO握手失败')
else:
    print(recv1)

loginCommand = 'auth login\r\n'
clientSocket.send(loginCommand.encode())
recv2 = clientSocket.recv(1024).decode()
if recv2[:3] != '334':
    print('没有收到334应答，请求登录失败')
else:
    print(recv2)

username = 'MTg2NTIwNTg2OTNAMTYzLmNvbQ==\r\n'
password = os.environ.get('MAIL_PASSWD') + '\r\n'  # 使用环境变量隐藏密码, 要注意BASE64编码是可以直接解密的
clientSocket.send(username.encode())
recv_tmp = clientSocket.recv(1024).decode()
clientSocket.send(password.encode())
recv3 = clientSocket.recv(1024).decode()
if recv3[:3] != '235':
    print('没有收到235应答，登录失败了.')
else:
    print(recv3)

mailFrom = 'mail from:<18652058693@163.com>\r\n'
rcptTo = 'rcpt to:<njuszj@qq.com>\r\n'
clientSocket.send(mailFrom.encode())
recv_tmp = clientSocket.recv(1024).decode()
clientSocket.send(rcptTo.encode())
recv_tmp = clientSocket.recv(1024).decode()

clientSocket.send('data\r\n'.encode())
recv_tmp = clientSocket.recv(1024).decode()
clientSocket.send('from:18652058693@163.com\r\n'.encode())
clientSocket.send('to:njuszj@qq.com\r\n'.encode())
clientSocket.send('subject:my smtp lab\r\n'.encode())
# 发送正文
clientSocket.send(msg.encode())
if len(sys.argv) == 2:
    # 如果有图片参数，发送图片编码
    filename = sys.argv[1]
    img = img2base64(filename)
    for i in range(0,len(img), 1000):
        clientSocket.send(img[i:i+1000])
# 发送正文结束的标志
clientSocket.send(endmsg.encode())
recv_tmp = clientSocket.recv(1024).decode()
print(recv_tmp)
clientSocket.send('quit\r\n'.encode())
recv4 = clientSocket.recv(1024).decode()
print(recv4)