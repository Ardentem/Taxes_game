# 非阻塞模块
import socketserver
import time
# 首先我们需要定义一个类
class my_socket_server(socketserver.BaseRequestHandler):
    # 首先执行setup方法，然后执行handle方法，最后执行finish方法
    # 如果handle方法报错，则会跳过
    # setup与finish无论如何都会执行
    # 一般只定义handle方法即可
    def setup(self):
        pass
    def handle(self):
        # 定义连接变量
        conn = self.request
        # 提示信息
        print("连接成功")
        # 发送消息定义
        msg = "欢迎打开德州扑克游戏，服务器已成功连接，当前游戏仍处于测试阶段，存在大量bug或服务器不稳定问题，请谅解\n游戏最后更新时间为2023-07-03-21:49\n游戏启动失败，回车继续"
        # 发送消息
        conn.send(msg.encode())
        #声明
        global timestr
        # 进入循环，不断接收客户端消息
        while True:
            # 接收客户端消息
            data = conn.recv(4096)
            # 打印消息
            print(data.decode())
            if data == b'mustexit':
                msg = '强制退出'
                conn.send(msg.encode())
                status = 1
                tep = 0
                idname = 0
                break
            #第一个是信息
            msg = '很遗憾，作者正在对服务器进行升级维护，本次维护开始时间为'+timestr+'，如果维护时间过长，请联系作者'
            print(msg)
            conn.send(msg.encode())
    def finish(self):
        pass

if __name__=="__main__":
    # 提示信息
    timestr = time.ctime()
    print("正在等待接收数据。。。。。。")
    # 创建多线程实例
    #记录初始全局变量
    status = 1
    tep = 0
    idname = 0
    #server = socketserver.TCPServer(('172.27.183.206', 8080), my_socket_server)
    server = socketserver.ThreadingTCPServer(('172.27.183.206', 8080), my_socket_server)
    # 开启多线程，等待连接
    server.serve_forever()