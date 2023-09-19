# %%
import socket
import time
# 服务端为TCP方式，客户端也采用TCP方式，默认参数即为TCP
client = socket.socket()
# 访问服务器的IP和端口
ip_port= ('47.113.200.47', 8080)
# 连接主机
client.connect(ip_port)
print('服务器响应需要时间，请静等几秒')
# 定义发送循环信息
while True:
    # 接收主机信息 每次接收缓冲区1024个字节
    data = client.recv(1024)
    # 打印接收数据
    print(data.decode())
    msg_input = input("请输入发送的消息：")
    if msg_input == '':
        msg_input = 'enter'
    client.send(msg_input.encode())
    if msg_input =='mustexit':
        break
    time.sleep(1)
# %%



