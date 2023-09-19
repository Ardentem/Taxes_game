import json
def strjiexi(card):
    color = ['♠','♥','♣','♦']
    number = [' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10',' J',' Q',' K',' A']
    return(color[card[0]]+number[card[1]])

def printtablestr(i,idname): #0盲注轮，1底牌轮，2翻牌轮，3转牌轮，4河牌轮
    f = open(idname + 'game.json', 'r')
    game = json.load(f)
    call = '\033[0;32;m{call}\033[0m'
    fold = '\033[0;31;m{fold}\033[0m'
    playerlist = [' (AI)',' (AI)',' (AI)',' (AI)',' (AI)',' (AI)']
    statuslist = [fold,call,call,fold]#对应0123
    playerlist[game['real']-1] = '\033[0;33;m(you)\033[0m'
    real = game['real']
    mycard1 = '***'
    mycard2 = '***'
    if i > 0:
        mycard1 = strjiexi(game['player'+str(real)][0])
        mycard2 = strjiexi(game['player'+str(real)][1])
    fcard1 = '***'
    fcard2 = '***'
    fcard3 = '***'
    fcard4 = '***'
    fcard5 = '***'
    if i > 1:
        fcard1 = strjiexi(game['fcard'][0])
        fcard2 = strjiexi(game['fcard'][1])
        fcard3 = strjiexi(game['fcard'][2])
    if i > 2:
        fcard4 = strjiexi(game['fcard'][3])
    if i > 3:
        fcard5 = strjiexi(game['fcard'][4])
    msg0 = '当前场上状态为：'
    msg1 = '                smallblind          bigblind'
    msg2 = '                player1{}        player2{}    '.format(playerlist[0],playerlist[1])
    msg3 = '                bet:%4d            bet:%4d       '%(game['sp1'][1],game['sp2'][1])
    msg4 = '                {}                {}             '.format(statuslist[game['sp1'][0]],statuslist[game['sp2'][0]])
    msg5 = ''
    msg6 = 'player6{}       {}   {}   {}   {}   {}        player3{}'.format(playerlist[5],fcard1,fcard2,fcard3,fcard4,fcard5,playerlist[2])
    msg7 = 'bet:%4d             Your Cards:  {}  {}            bet:%4d'.format(mycard1,mycard2)%(game['sp6'][1],game['sp3'][1])
    msg8 = '{}                       Pool:%5d                 {}'.format(statuslist[game['sp6'][0]],statuslist[game['sp3'][0]])%(game['pool'])
    msg9 = ''
    msg10 = '                player5{}        player4{}    '.format(playerlist[4],playerlist[3])
    msg11 = '                bet:%4d            bet:%4d       '%(game['sp5'][1],game['sp4'][1])
    msg12 = '                {}                {}             '.format(statuslist[game['sp5'][0]],statuslist[game['sp4'][0]])
    finalmsg = msg0+'\n'+msg1+'\n'+msg2+'\n'+msg3+'\n'+msg4+'\n'+msg5+'\n'+msg6+'\n'+msg7+'\n'+msg8+'\n'+msg9+'\n'+msg10+'\n'+msg11+'\n'+msg12+'\n'
    return(finalmsg)

def printtablestr_online(i,idname): #0盲注轮，1底牌轮，2翻牌轮，3转牌轮，4河牌轮 -1开局轮
    f = open(idname + 'onlinegame.json', 'r')
    game = json.load(f)
    call = '\033[0;32;m{call}\033[0m'
    fold = '\033[0;31;m{fold}\033[0m'
    playerlist = [' (AI)',' (AI)',' (AI)',' (AI)',' (AI)',' (AI)']
    real = game['real']
    realplayerlist = game['playerlist']
    statuslist = [fold,call,call,fold]#对应0123
    for i in range(len(realplayerlist)):
        playerlist[real[i]] = '\033[0;33;m('+ str(realplayerlist[i]) +')\033[0m'
    fcard1 = '***'
    fcard2 = '***'
    fcard3 = '***'
    fcard4 = '***'
    fcard5 = '***'
    if i > 1:
        fcard1 = strjiexi(game['fcard'][0])
        fcard2 = strjiexi(game['fcard'][1])
        fcard3 = strjiexi(game['fcard'][2])
    if i > 2:
        fcard4 = strjiexi(game['fcard'][3])
    if i > 3:
        fcard5 = strjiexi(game['fcard'][4])
    msg0 = '当前场上状态为：'
    msg1 = '                smallblind          bigblind'
    msg2 = '                player1{}        player2{}    '.format(playerlist[0],playerlist[1])
    msg3 = '                bet:%4d            bet:%4d       '%(game['sp1'][1],game['sp2'][1])
    msg4 = '                {}                {}             '.format(statuslist[game['sp1'][0]],statuslist[game['sp2'][0]])
    msg5 = ''
    msg6 = 'player6{}       {}   {}   {}   {}   {}        player3{}'.format(playerlist[5],fcard1,fcard2,fcard3,fcard4,fcard5,playerlist[2])
    msg7 = 'bet:%4d                                            bet:%4d'%(game['sp6'][1],game['sp3'][1])
    msg8 = '{}                       Pool:%5d                 {}'.format(statuslist[game['sp6'][0]],statuslist[game['sp3'][0]])%(game['pool'])
    msg9 = ''
    msg10 = '                player5{}        player4{}    '.format(playerlist[4],playerlist[3])
    msg11 = '                bet:%4d            bet:%4d       '%(game['sp5'][1],game['sp4'][1])
    msg12 = '                {}                {}             '.format(statuslist[game['sp5'][0]],statuslist[game['sp4'][0]])
    finalmsg = msg0+'\n'+msg1+'\n'+msg2+'\n'+msg3+'\n'+msg4+'\n'+msg5+'\n'+msg6+'\n'+msg7+'\n'+msg8+'\n'+msg9+'\n'+msg10+'\n'+msg11+'\n'+msg12+'\n'
    return(finalmsg)