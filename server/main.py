# 非阻塞模块
import socketserver
import random
import json
import aiplayerbet
import settlement
import printtable
# 首先我们需要定义一个类
class my_socket_server(socketserver.BaseRequestHandler):
    # 首先执行setup方法，然后执行handle方法，最后执行finish方法
    # 如果handle方法报错，则会跳过
    # setup与finish无论如何都会执行
    # 一般只定义handle方法即可
    def __init__(self, request, client_address, server):
        self.ip = ""            # ip地址
        self.port = 0           # 端口
        self.client_addrstr = ['example']   # 链接客户端地址
        self.client_socket = [] # socket链接对象
        super().__init__(request, client_address, server)

    def setup(self):
        self.ip = self.client_address[0].strip()     # 获取客户端的ip
        self.port = self.client_address[1]           # 获取客户端的port
        print(self.ip+":"+str(self.port)+"连接到服务器！")
        self.client_addrstr.append(self.client_address) # 保存到队列中
        self.client_socket.append(self.request)      # 保存套接字socket
        pass
    def handle(self):
        # 定义连接变量
        conn = self.request
        # 发送消息定义
        msg0 = '欢迎打开德州扑克游戏，服务器已成功连接，当前游戏仍处于测试阶段，存在大量bug或服务器不稳定问题，请谅解\n'
        with open("updateinfo.txt", "r") as f:  #打开文本
            data = f.read()   #读取文本
        msg2 = data
        msg3 = '\n\033[0;31;m重要提醒：\n1.由于服务器承载问题，每次返回结果需要一定的时间，请不要快速连续点击回车，务必等待系统提示您输入要发送的信息时再单击回车进入下一步，否则可能会导致服务器通讯断开\n2.线上多人联机模式仍在开发中，当前版本稳定性较差，因此不予开放\033[0m\n'       
        msgf = '\033[0;32;m游戏已启动，请输入用户名\033[0m'
        # 发送消息
        msg = msg0 + msg2 +msg3 + msgf
        conn.send(msg.encode())
        #声明
        status = 1
        tep = 0
        idname = 0

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
            else:
                returnlist = dzpk(data.decode(),status,tep,idname)
                #第一个是信息
                print(returnlist[0])
                conn.send(str(returnlist[0]).encode())
                #第二个是状态
                status = returnlist[1]
                #第三是暂时变量
                tep = returnlist[2]
                #第四个是id
                idname = returnlist[3]
            #记录登录信息
            if tep == 'gamein':
                f = open('onlineplayer.json', 'r')
                onlinep = json.load(f)
                onlinep.update({str(self.client_address):idname})
                with open('onlineplayer.json', 'w') as file:
                    json.dump(onlinep, file)
            elif tep == 'logout' or tep == 'gameout':
                f = open('onlineplayer.json', 'r')
                onlinep = json.load(f)
                onlinep.pop(str(self.client_address))
                with open('onlineplayer.json', 'w') as file:
                    json.dump(onlinep, file) 
        conn.close()
 
    def finish(self):
        f = open('onlineplayer.json', 'r')
        onlinep = json.load(f)
        for address in list(onlinep.keys()):
            if not (address in self.client_addrstr):
                onlinep.pop(address)
        with open('onlineplayer.json', 'w') as file:
            json.dump(onlinep, file)
        pass

def dzpk(msg,status,tep,idname):
    #输入账号
    if status == 1:
        try:
            f = open(msg+'.json', 'r')
        except:
            returnlist = ['没有这个账号，请重新输入',1,0,0]
            return returnlist
        thezhanghao = json.load(f)
        returnlist = ['用户存在，请输入密码',2,thezhanghao['password'],thezhanghao['name']]
        return returnlist
    elif status == 2:
        if str(msg) == str(tep):
            returnlist = ['密码正确，输入1查看余额，输入2回去登录',3,0,idname]
        else:
            #tep变成了0
            returnlist = ['密码错误，请重新输入账号',1,0,0]
        return returnlist
    elif status == 3:
        if str(msg) == '1' or str(msg) == 'enter':
            f = open(idname+'.json', 'r')
            thezhanghao = json.load(f)
            yue = thezhanghao['cash']
            if yue>1000:
                returnlist = ['当前余额为：'+str(yue)+',输入1开始单人游戏，输入其他自动退出',4,yue,idname] 
            else:
                returnlist = ['当前余额为：'+str(yue)+',不足1000，回到登录界面，请输入账号',1,0,0] 
        else :
            returnlist = ['请输入账号',1,0,0] 
        return returnlist
    elif status == 4:
        #初始化牌局
        if str(msg) == '1':
            f = open('onlineplayer.json', 'r')
            onlinep = json.load(f)
            if idname in onlinep.values():
                returnlist = ['该账号已经处于登陆状态，如有疑问请联系管理员\n请重新输入账号',1,0,0]
            else:
                myseat = startgame(tep,idname)
                msg = '你的位置是'+str(myseat)+"，1号位为小盲自动下注10，2号位为大盲自动下注20，按回车继续"
                returnlist = [msg,5,'gamein',idname]
        else:
            returnlist =['退出到开始界面，请输入账号',1,'logout',0]
        return returnlist
    elif status == 5:
        #盲注轮
        ret = blindbet(idname)
        returnlist = [ret[1],ret[0],ret[2],idname]
        return returnlist
    elif status == 105:
        #玩家操作
        ret = bet_player(msg,tep,idname)
        if ret[1] == 000:
            returnlist = [ret[0],5,0,idname]
        elif ret[1] == 999:
            returnlist = [ret[0],999,0,idname]
        return returnlist
    elif status == 6:
        #看牌
        f = open(idname + 'game.json', 'r')
        game = json.load(f)
        real = game['real']
        msg = '您的底牌是'+jiexi(game['player'+str(real)][0])+'和'+jiexi(game['player'+str(real)][1])+'，回车继续'
        returnlist = [msg,7,0,idname]
        return returnlist
    elif status == 7:
        #开始第一轮下注
        ret = firstbet(idname)
        returnlist = [ret[1],ret[0],ret[2],idname]
        return returnlist
    elif status == 107:
        #玩家操作
        ret = bet_player(msg,tep,idname)
        if ret[1] == 000:
            returnlist = [ret[0],7,0,idname]
        elif ret[1] == 999:
            returnlist = [ret[0],999,0,idname]
        return returnlist
    elif status == 8:
        #翻牌
        f = open(idname + 'game.json', 'r')
        game = json.load(f)
        cards = game['fcard']
        msg = '翻牌结果：'+jiexi(cards[0])+','+jiexi(cards[1])+' 和'+jiexi(cards[2])+'，回车继续'
        returnlist = [msg,9,0,idname]
        return returnlist
    elif status == 9:
        #第二轮加注
        ret = secondbet(idname)
        returnlist = [ret[1],ret[0],ret[2],idname]
        return returnlist
    elif status == 109:
        #玩家操作
        ret = bet_player(msg,tep,idname)
        if ret[1] == 000:
            returnlist = [ret[0],9,0,idname]
        elif ret[1] == 999:
            returnlist = [ret[0],999,0,idname]
        return returnlist
    elif status == 10:
        #翻turn牌
        f = open(idname + 'game.json', 'r')
        game = json.load(f)
        cards = game['fcard']
        msg = '翻turn牌，当前公共牌为'+jiexi(cards[0])+','+jiexi(cards[1])+'，'+jiexi(cards[2])+' 和'+jiexi(cards[3])+'，回车继续'
        returnlist = [msg,11,0,idname]
        return returnlist
    elif status == 11:
        #第三轮加注
        ret = thirdbet(idname)
        returnlist = [ret[1],ret[0],ret[2],idname]
        return returnlist
    elif status == 111:
        #玩家操作
        ret = bet_player(msg,tep,idname)
        if ret[1] == 000:
            returnlist = [ret[0],11,0,idname]
        elif ret[1] == 999:
            returnlist = [ret[0],999,0,idname]
        return returnlist
    elif status == 12:
        #翻river牌
        f = open(idname + 'game.json', 'r')
        game = json.load(f)
        cards = game['fcard']
        msg = '翻river牌，当前公共牌为'+jiexi(cards[0])+','+jiexi(cards[1])+'，'+jiexi(cards[2])+','+jiexi(cards[3])+'和'+jiexi(cards[4])+'，回车继续'
        returnlist = [msg,13,0,idname]
        return returnlist
    elif status == 13:
        #第四轮加注
        ret = finalbet(idname)
        returnlist = [ret[1],ret[0],ret[2],idname]
        return returnlist
    elif status == 113:
        #玩家操作
        ret = bet_player(msg,tep,idname)
        if ret[1] == 000:
            returnlist = [ret[0],13,0,idname]
        elif ret[1] == 999:
            returnlist = [ret[0],999,0,idname]
        return returnlist
    elif status == 999:
        #结算程序
        ret = settlement.settle(idname)
        returnlist = [ret[0],ret[1],0,idname]
        return returnlist
    elif status == 9999:
        ret = settlement.finalsettle(idname)
        returnlist = [ret,3,'gameout',idname]
        return returnlist
    else:
        returnlist = ['初始化，请输入账号',1,0,0]
        return returnlist 

def startgame(tep,idname):
    f = open('game0.json', 'r')
    game = json.load(f)
    game['cash'] = tep
    real = random.randint(1,6)
    game['real'] = real
    cardall = []
    for i in range(4):
        for j in range(13):
            cardall.append((i,j))
    gamecard = random.sample(cardall,17)
    game['player6'][0] = gamecard[0]
    game['player6'][1] = gamecard[1]
    game['player1'][0] = gamecard[2]
    game['player1'][1] = gamecard[3]
    game['player2'][0] = gamecard[4]
    game['player2'][1] = gamecard[5]
    game['player3'][0] = gamecard[6]
    game['player3'][1] = gamecard[7]
    game['player4'][0] = gamecard[8]
    game['player4'][1] = gamecard[9]
    game['player5'][0] = gamecard[10]
    game['player5'][1] = gamecard[11]
    game['fcard'][0] = gamecard[12]
    game['fcard'][1] = gamecard[13]
    game['fcard'][2] = gamecard[14]
    game['fcard'][3] = gamecard[15]
    game['fcard'][4] = gamecard[16]
    #玩家状态是 2
    game['sp'+str(real)][0] = 2
    game['sp1'][1] = 10
    game['sp2'][1] = 20
    game['pool'] = 30
    with open(idname + 'game.json', 'w') as file:
        json.dump(game, file)
    return(game['real'])

def jiexi(card):
    color = ['黑桃','红桃','梅花','方块']
    number = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    return(color[card[0]]+number[card[1]])

def blindbet(idname):#返回值是list，[下一步status，msg,tep]
    f = open(idname + 'game.json', 'r')
    game = json.load(f)
    #如果所有人加注相等，盲注轮结束
    betlist = []
    for i in range(1,7):
        if game['sp'+str(i)][0] != 0:
            betlist.append(game['sp'+str(i)][1])
    if len(set(betlist)) == 1:
        #下一轮枪手位开始
        game['now'] = 3
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        msg = printtable.printtablestr(0,idname)
        return([6,msg + '盲注轮结束，回车进入下一轮',0])
    else:
        maxbet = max(set(betlist))
    now = game['now']
    #先修改json中的now
    if now == 6:
        game['now'] = 1
    else:
        game['now'] = now + 1
    pool = game['pool']
    if game['sp'+str(now)][0] == 0:
        msgout = str(now)+'号位玩家已放弃，回车继续'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([5,msgout,0])
    if game['sp'+str(now)][0] == 1:
        #电脑玩家操作，无脑跟注
        before = game['sp'+str(now)][1]
        game['sp'+str(now)][1] = maxbet
        game['pool'] = pool + maxbet - before
        msgout = '当前轮到'+str(now)+'号位玩家，选择跟注，场上最高下注为'+str(maxbet)+'，回车继续'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([5,msgout,0])
    if game['sp'+str(now)][0] == 2:
        nowbet = game['sp'+str(now)][1]
        game['bet'] = nowbet
        msgout = '当前轮到玩家('+str(now)+'号位）下注，您已经下注'+str(nowbet)+',您需要跟注至少'+str(maxbet - nowbet)+'，请输入跟注额，如果输入小于最小值会直接弃牌，如果额外加注不能加50以上'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([105,msgout,maxbet-nowbet])   

def bet_player(msg,min,idname):
    f = open(idname + 'game.json', 'r')
    game = json.load(f)
    real = game['real']
    if msg == 'enter':
        nowbet = game['sp'+str(real)][1]
        game['sp'+str(real)][1] = nowbet + min 
        game['bet'] = nowbet + min
        pool = game['pool']
        game['pool'] = pool + min
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return(['回车自动跟注',000])
    try:
        playerbet = int(msg)
    except:
        #玩家已fold
        game['sp'+str(real)][0] = 3
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return(['您选择弃牌，回车直接查看本局结果',999])
    if playerbet < min:
        #结算程序999
        game['sp'+str(real)][0] = 3
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return(['您选择弃牌，回车直接查看本局结果',999])
    else:
        if playerbet > min + 50:
            playerbet = min + 50
        nowbet = game['sp'+str(real)][1]
        game['sp'+str(real)][1] = nowbet + playerbet 
        game['bet'] = nowbet + playerbet
        pool = game['pool']
        game['pool'] = pool + playerbet
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        #000表示game continue
        return(['加注成功，您当前总下注为'+str(nowbet + playerbet)+'，按回车键继续',000])
    
def firstbet(idname):
    #至少要转一圈
    f = open(idname + 'game.json', 'r')
    game = json.load(f)
    circle = game['circle']
    #如果所有人加注相等， 第一轮结束
    betlist = []
    for i in range(1,7):
        if game['sp'+str(i)][0] != 0:
            betlist.append(game['sp'+str(i)][1])
    if len(betlist) == 1:
        return([999,'只有一人持牌，游戏结束，回车结算',0])
    if len(set(betlist)) == 1:
        if circle >= 1:
            #下一轮枪手位开始
            game['now'] = 3
            game['circle'] = 0
            with open(idname + 'game.json', 'w') as file:
                json.dump(game, file)
            msg = printtable.printtablestr(1,idname)
            return([8,msg + '第一轮结束，回车进入下一轮',0])
    maxbet = max(set(betlist))
    now = game['now']
    #先修改json中的now
    if now == 6:
        game['now'] = 1
    elif now == 2:
        game['now'] = now + 1
        game['circle'] = circle + 1
    else:
        game['now'] = now + 1
    pool = game['pool']
    if game['sp'+str(now)][0] == 0:
        msgout = str(now)+'号位玩家已放弃，回车继续'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([7,msgout,0])
    if game['sp'+str(now)][0] == 1:
        #电脑玩家操作，看牌决定
        before = game['sp'+str(now)][1]
        card1 = game['player'+str(now)][0]
        card2 = game['player'+str(now)][1]
        betnum = aiplayerbet.aibet_first(circle,card1,card2)
        if before >= 130 and before + betnum < maxbet:
            #一定跟
            game['sp'+str(now)][1] = maxbet
            game['pool'] = pool + maxbet - before
            msgout = '当前轮到'+str(now)+'号位玩家，选择跟注，场上最高下注为'+str(maxbet)
        elif before + betnum < maxbet:
            msgout = '当前轮到'+str(now)+'号位玩家，选择放弃，回车继续'
            game['sp'+str(now)][0] = 0
        elif before + betnum <= maxbet + 20:
            game['sp'+str(now)][1] = maxbet
            game['pool'] = pool + maxbet - before
            msgout = '当前轮到'+str(now)+'号位玩家，选择跟注，场上最高下注为'+str(maxbet)
        else:
            if before + betnum >= maxbet + 50:
            #限制最大加注
                betnum = maxbet + 50 -before
            game['sp'+str(now)][1] = before + betnum
            game['pool'] = pool + betnum
            msgout = '当前轮到'+str(now)+'号位玩家，选择加注'+str(betnum)+'，场上最高下注为'+str(before + betnum)       
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([7,msgout,0])
    if game['sp'+str(now)][0] == 2:
        nowbet = game['sp'+str(now)][1]
        game['bet'] = nowbet
        msgout = '当前轮到玩家('+str(now)+'号位）下注，您已经下注'+str(nowbet)+',您需要跟注至少'+str(maxbet - nowbet)+'，请输入跟注额，如果输入小于最小值会直接弃牌，如果额外加注不能加50以上'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([107,msgout,maxbet-nowbet]) 

def secondbet(idname):
    #至少要转一圈
    f = open(idname + 'game.json', 'r')
    game = json.load(f)
    circle = game['circle']
    #如果所有人加注相等， 第二轮结束
    betlist = []
    for i in range(1,7):
        if game['sp'+str(i)][0] != 0:
            betlist.append(game['sp'+str(i)][1])
    if len(betlist) == 1:
        return([999,'游戏结束，回车结算',0])
    if len(set(betlist)) == 1:
        if circle >= 1:
            #下一轮枪手位开始
            game['now'] = 3
            game['circle'] = 0
            with open(idname + 'game.json', 'w') as file:
                json.dump(game, file)
            msg = printtable.printtablestr(2,idname)
            return([10,msg + '第二轮结束，回车进入下一轮',0])
    maxbet = max(set(betlist))
    now = game['now']
    #先修改json中的now
    if now == 6:
        game['now'] = 1
    elif now == 2:
        game['now'] = now + 1
        game['circle'] = circle + 1
    else:
        game['now'] = now + 1
    pool = game['pool']
    if game['sp'+str(now)][0] == 0:
        msgout = str(now)+'号位玩家已放弃，回车继续'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([9,msgout,0])
    if game['sp'+str(now)][0] == 1:
        #电脑玩家操作，看牌决定
        before = game['sp'+str(now)][1]
        card1 = game['player'+str(now)][0]
        card2 = game['player'+str(now)][1]
        card3 = game['fcard'][0]
        card4 = game['fcard'][1]
        card5 = game['fcard'][2]
        betnum = aiplayerbet.aibet_second(circle,card1,card2,card3,card4,card5)
        #这一步ai的逻辑还没写
        #if before >= 130 and before + betnum < maxbet:
        if betnum > 8000:
            #一定跟
            game['sp'+str(now)][1] = maxbet
            game['pool'] = pool + maxbet - before
            msgout = '当前轮到'+str(now)+'号位玩家，选择跟注，场上最高下注为'+str(maxbet)
        elif before + betnum < maxbet:
            msgout = '当前轮到'+str(now)+'号位玩家，选择放弃，回车继续'
            game['sp'+str(now)][0] = 0
        elif before + betnum <= maxbet + 20:
            game['sp'+str(now)][1] = maxbet
            game['pool'] = pool + maxbet - before
            msgout = '当前轮到'+str(now)+'号位玩家，选择跟注，场上最高下注为'+str(maxbet)
        else:
            if before + betnum >= maxbet + 50:
            #限制最大加注
                betnum = maxbet + 50 -before
            game['sp'+str(now)][1] = before + betnum
            game['pool'] = pool + betnum
            msgout = '当前轮到'+str(now)+'号位玩家，选择加注'+str(betnum)+'，场上最高下注为'+str(before + betnum)       
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([9,msgout,0])
    if game['sp'+str(now)][0] == 2:
        nowbet = game['sp'+str(now)][1]
        game['bet'] = nowbet
        msgout = '当前轮到玩家('+str(now)+'号位）下注，您已经下注'+str(nowbet)+',您需要跟注至少'+str(maxbet - nowbet)+'，请输入跟注额，如果输入小于最小值会直接弃牌，如果额外加注不能加50以上'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([109,msgout,maxbet-nowbet]) 
    
def thirdbet(idname):
    #至少要转一圈
    f = open(idname + 'game.json', 'r')
    game = json.load(f)
    circle = game['circle']
    #如果所有人加注相等， 第三轮结束
    betlist = []
    for i in range(1,7):
        if game['sp'+str(i)][0] != 0:
            betlist.append(game['sp'+str(i)][1])
    if len(betlist) == 1:
        return([999,'游戏结束，回车结算',0])
    if len(set(betlist)) == 1:
        if circle >= 1:
            #下一轮枪手位开始
            game['now'] = 3
            game['circle'] = 0
            with open(idname + 'game.json', 'w') as file:
                json.dump(game, file)
            msg = printtable.printtablestr(3,idname)
            return([12,msg+'第三轮结束，回车进入最后一轮',0])
    maxbet = max(set(betlist))
    now = game['now']
    #先修改json中的now
    if now == 6:
        game['now'] = 1
    elif now == 2:
        game['now'] = now + 1
        game['circle'] = circle + 1
    else:
        game['now'] = now + 1
    pool = game['pool']
    if game['sp'+str(now)][0] == 0:
        msgout = str(now)+'号位玩家已放弃，回车继续'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([11,msgout,0])
    if game['sp'+str(now)][0] == 1:
        #电脑玩家操作，看牌决定
        before = game['sp'+str(now)][1]
        card1 = game['player'+str(now)][0]
        card2 = game['player'+str(now)][1]
        card3 = game['fcard'][0]
        card4 = game['fcard'][1]
        card5 = game['fcard'][2]
        card6 = game['fcard'][3]
        betnum = aiplayerbet.aibet_third(circle,card1,card2,card3,card4,card5,card6)
        #这一步ai的逻辑还没写
        #if before >= 130 and before + betnum < maxbet:
        if betnum > 8000:
            #一定跟
            game['sp'+str(now)][1] = maxbet
            game['pool'] = pool + maxbet - before
            msgout = '当前轮到'+str(now)+'号位玩家，选择跟注，场上最高下注为'+str(maxbet)
        elif before + betnum < maxbet:
            msgout = '当前轮到'+str(now)+'号位玩家，选择放弃，回车继续'
            game['sp'+str(now)][0] = 0
        elif before + betnum <= maxbet + 20:
            game['sp'+str(now)][1] = maxbet
            game['pool'] = pool + maxbet - before
            msgout = '当前轮到'+str(now)+'号位玩家，选择跟注，场上最高下注为'+str(maxbet)
        else:
            if before + betnum >= maxbet + 50:
            #限制最大加注
                betnum = maxbet + 50 -before
            game['sp'+str(now)][1] = before + betnum
            game['pool'] = pool + betnum
            msgout = '当前轮到'+str(now)+'号位玩家，选择加注'+str(betnum)+'，场上最高下注为'+str(before + betnum)       
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([11,msgout,0])
    if game['sp'+str(now)][0] == 2:
        nowbet = game['sp'+str(now)][1]
        game['bet'] = nowbet
        msgout = '当前轮到玩家('+str(now)+'号位）下注，您已经下注'+str(nowbet)+',您需要跟注至少'+str(maxbet - nowbet)+'，请输入跟注额，如果输入小于最小值会直接弃牌，如果额外加注不能加50以上'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([111,msgout,maxbet-nowbet]) 

def finalbet(idname):
    #至少要转一圈
    f = open(idname + 'game.json', 'r')
    game = json.load(f)
    circle = game['circle']
    #如果所有人加注相等， 第三轮结束
    betlist = []
    for i in range(1,7):
        if game['sp'+str(i)][0] != 0:
            betlist.append(game['sp'+str(i)][1])
    if len(betlist) == 1:
        return([999,'游戏结束，回车结算',0])
    if len(set(betlist)) == 1:
        if circle >= 1:
            #比牌
            game['now'] = 1
            game['circle'] = 0
            with open(idname + 'game.json', 'w') as file:
                json.dump(game, file)
            msg = printtable.printtablestr(4,idname)
            return([999,msg+'开始比牌',0])
    maxbet = max(set(betlist))
    now = game['now']
    #先修改json中的now
    if now == 6:
        game['now'] = 1
    elif now == 2:
        game['now'] = now + 1
        game['circle'] = circle + 1
    else:
        game['now'] = now + 1
    pool = game['pool']
    if game['sp'+str(now)][0] == 0:
        msgout = str(now)+'号位玩家已放弃，回车继续'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([13,msgout,0])
    if game['sp'+str(now)][0] == 1:
        #电脑玩家操作，看牌决定
        before = game['sp'+str(now)][1]
        card1 = game['player'+str(now)][0]
        card2 = game['player'+str(now)][1]
        card3 = game['fcard'][0]
        card4 = game['fcard'][1]
        card5 = game['fcard'][2]
        card6 = game['fcard'][3]
        betnum = aiplayerbet.aibet_third(circle,card1,card2,card3,card4,card5,card6)
        #这一步ai的逻辑还没写
        #if before >= 130 and before + betnum < maxbet:
        if betnum > 8000:
            #一定跟
            game['sp'+str(now)][1] = maxbet
            game['pool'] = pool + maxbet - before
            msgout = '当前轮到'+str(now)+'号位玩家，选择跟注，场上最高下注为'+str(maxbet)
        elif before + betnum < maxbet:
            msgout = '当前轮到'+str(now)+'号位玩家，选择放弃，回车继续'
            game['sp'+str(now)][0] = 0
        elif before + betnum <= maxbet + 20:
            game['sp'+str(now)][1] = maxbet
            game['pool'] = pool + maxbet - before
            msgout = '当前轮到'+str(now)+'号位玩家，选择跟注，场上最高下注为'+str(maxbet)
        else:
            if before + betnum >= maxbet + 50:
            #限制最大加注
                betnum = maxbet + 50 -before
            game['sp'+str(now)][1] = before + betnum
            game['pool'] = pool + betnum
            msgout = '当前轮到'+str(now)+'号位玩家，选择加注'+str(betnum)+'，场上最高下注为'+str(before + betnum)       
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([13,msgout,0])
    if game['sp'+str(now)][0] == 2:
        nowbet = game['sp'+str(now)][1]
        game['bet'] = nowbet
        msgout = '当前轮到玩家('+str(now)+'号位）下注，您已经下注'+str(nowbet)+',您需要跟注至少'+str(maxbet - nowbet)+'，请输入跟注额，如果输入小于最小值会直接弃牌，如果额外加注不能加50以上'
        with open(idname + 'game.json', 'w') as file:
            json.dump(game, file)
        return([113,msgout,maxbet-nowbet]) 

if __name__=="__main__":
    # 提示信息
    print("正在等待接收数据。。。。。。")
    # 创建多线程实例

    #server = socketserver.TCPServer(('172.27.183.206', 8080), my_socket_server)
    server = socketserver.ThreadingTCPServer(('172.27.183.206', 8080), my_socket_server)
    # 开启多线程，等待连接
    server.serve_forever()