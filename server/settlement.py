import json

def settle(idname): #i~1-7
    f = open(idname + 'game.json', 'r')
    game = json.load(f)
    i = game['bipai']
    c1 = game['player'+str(i)][0]
    c2 = game['player'+str(i)][1]
    cards = list(game['fcard'])
    cards.append(c1)
    cards.append(c2)
    cardcolor,cardnum = zip(*cards)
    #判断出现最多的数字和花色
    maxcolor = max(set(cardcolor),key=cardcolor.count)
    maxcolor_num = cardcolor.count(maxcolor)
    num_numsort = list(set(cardnum))
    num_numsort.sort(key=cardnum.count,reverse=True)
    maxnum_num = cardnum.count(num_numsort[0])
    maxnum_num2 = cardnum.count(num_numsort[1])
    maxnum_num3 = cardnum.count(num_numsort[2])
    #判断顺子
    numsort = list(set(cardnum))
    shunzimax = -1
    if len(numsort) >= 5:
        numsort.sort(reverse=True)
        #注意A可以凑10JQKA也可以A2345
        if numsort[0] == 13:
            numsort.append(-1)
        for k in range(len(numsort)-4):
            if numsort[k] - numsort[k+4] == 4:
                shunzimax = numsort[k]
                break
    #同花顺
    thshunzimax = -1
    if maxcolor_num >= 5:
        thcards = list(filter(lambda x : x[0]==maxcolor , cards))
        thcardcolor,thcardnum = zip(*thcards)
        thnumsort = list(set(thcardnum))
        thnumsort.sort(reverse=True)
        if shunzimax != -1:
            if thnumsort[0] == 13:
                thnumsort.append(-1)
            for k in range(len(thnumsort)-4):
                if thnumsort[k] - thnumsort[k+4] == 4:
                    thshunzimax = thnumsort[k]
                    break
    #给这副牌评分，越前越重要
    score = [0,0,0,0,0,0]
    if thshunzimax != -1:
        #9同花顺
        score[0] = 9
        score[1] = thshunzimax
        msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为同花顺！！！'
    elif maxnum_num == 4:
        #8四条
        score[0] = 8
        score[1] = num_numsort[0]
        score[2] = max(num_numsort[1:])
        msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为四条！！！'
    elif maxnum_num == 3:
        #7葫芦
        if maxnum_num2 == 3:
            score[0] = 7
            score[1] = max(num_numsort[0],num_numsort[0])
            msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为葫芦！！！'
        elif maxnum_num2 == 2:
            if maxnum_num3 == 2:
                score[0] = 7
                score[1] = num_numsort[0]
                score[2] = max(num_numsort[1],num_numsort[2])
                msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为葫芦！！！'
            elif maxnum_num3 == 1:
                score[0] = 7
                score[1] = num_numsort[0]
                score[2] = num_numsort[1]
                msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为葫芦！！！'
        elif maxnum_num2 == 1:
        #4三条    
            score[0] = 4
            score[1] = max(num_numsort[0],num_numsort[0])
            score[2] = max(num_numsort[1:])
            msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为三条！！！'
    elif maxcolor_num >= 5:
        #6同花
        score[0] = 6
        score[1] = thnumsort[0]
        score[2] = thnumsort[1]
        score[3] = thnumsort[2]
        score[4] = thnumsort[3]
        score[5] = thnumsort[4]
        msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为同花！！！'
    elif shunzimax != -1:
        #5顺子
        score[0] = 5
        score[1] = shunzimax
        msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为顺子！！！'
    elif maxnum_num == 2:
        if maxnum_num2 == 2:
        #3两对
            if maxnum_num3 == 2:
                score[0] = 3
                teplist = num_numsort[0:3]
                teplist.sort(reverse=True)
                score[1] = teplist[0]
                score[2] = teplist[1]
                score[3] = max(num_numsort[3:])
                msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为两对！！！'
            elif maxnum_num3 == 1:
                score[0] = 3
                score[1] = max(num_numsort[0:2])
                score[2] = min(num_numsort[0:2])
                score[3] = max(num_numsort[2:])
                msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为两对！！！'
        #2一对
        elif maxnum_num2 == 1:
            score[0] = 2
            score[1] = num_numsort[0]
            teplist = num_numsort[1:]
            teplist.sort(reverse=True)
            score[2] = teplist[0]
            score[3] = teplist[1]
            score[4] = teplist[2]
            msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为一对！！！'
    else:
        #1高牌
        score[0] = 1
        score[1] = numsort[0]
        score[2] = numsort[1]
        score[3] = numsort[2]
        score[4] = numsort[3]
        score[5] = numsort[4]
        msg = '玩家'+str(i)+'，手牌为'+jiexi(c1)+'和'+jiexi(c2)+'，最终牌型为高牌！！！'
    game['score'][i-1] = score
    game['bipai'] = i + 1
    status = game['sp'+str(i)][0]
    betnum = game['sp'+str(i)][1]
    if status == 0:
        msg2 = '该玩家当前状态为fold，总下注为'+str(betnum)
    elif status == 1:
        msg2 = '该玩家当前状态为持牌，总下注为'+str(betnum)
    elif status == 2:
        msg2 = '玩家（您）当前状态为持牌，总下注为'+str(betnum)
    elif status == 3:
        msg2 = '玩家（您）当前状态为fold，总下注为'+str(betnum)
    if i == 6:
        nextstatu = 9999
    else:
        nextstatu = 999
    with open(idname + 'game.json', 'w') as file:
        json.dump(game, file)
    return([msg+'\n'+msg2+',按回车继续',nextstatu])

def finalsettle(idname):
    f = open(idname + 'game.json', 'r')
    game = json.load(f)
    scorelist = []
    nfscorelist = []
    msg0 = '五张公共牌为'+jiexi(game['fcard'][0])+'，'+jiexi(game['fcard'][1])+'，'+jiexi(game['fcard'][2])+'，'+jiexi(game['fcard'][3])+'，'+jiexi(game['fcard'][4])+'\n'
    for i in range(6):
        scores = game['score'][i]
        statu = game['sp'+str(i+1)][0]
        score = 4826809*scores[0] + 371293*scores[1] + 28561*scores[2] + 2197*scores[3] + 169*scores[4] + 13*scores[5]
        scorelist.append(score)
        if statu == 1 or statu == 2:
            nfscorelist.append(score)
        else:
            nfscorelist.append(0)
    vwinner = [i+1 for i, x in enumerate(scorelist) if x==max(scorelist)]
    winner = [i+1 for i,x in enumerate(nfscorelist) if x==max(nfscorelist)]
    real = game['real']
    realplayerstatu = game['sp'+str(real)][0]
    if realplayerstatu == 3:
        msg = '您选择了放弃，本局游戏实际上牌最大的人是玩家'+str(vwinner)[1:-1]
        msg2 = ''
    elif realplayerstatu == 2:
        msg = '本局游戏实际上牌最大的人是玩家'+str(vwinner)[1:-1]
        msg2 = '\n本局游戏的最后胜利者为玩家'+str(winner)[1:-1]
    pool = game['pool']
    bet = game['bet']
    ff = open(idname+'.json', 'r')
    account = json.load(ff)
    if len(winner) == 1:
        if real in winner:
            msg3 ='\n当前全部的奖池为'+str(pool)+'，恭喜您获得了全部的奖池'
            cash = account['cash']
            account['cash'] = cash + pool - bet
            msg4 = '\n您的本轮收益为'+str(pool-bet)
        else:
            msg3 = '\n当前全部的奖池为'+str(pool)+'，很遗憾不是您的'
            cash = account['cash']
            account['cash'] = cash - bet
            msg4 = '\n您的本轮损失为'+str(bet)
    elif len(winner) > 1:
        winnernum = len(winner)
        if real in winner:
            msg3 ='\n当前全部的奖池为'+str(pool)+'，恭喜您获得了部分奖池'
            cash = account['cash']
            account['cash'] = cash + pool / winnernum - bet
            msg4 = '\n您的本轮收益为'+str(pool / winnernum - bet)
        else:
            msg3 = '\n当前全部的奖池为'+str(pool)+'，很遗憾不是您的'
            cash = account['cash']
            account['cash'] = cash - bet
            msg4 = '\n您的本轮损失为'+str(bet)
    with open(idname+'.json', 'w') as file:
        json.dump(account, file)
    return(msg0+msg+msg2+msg3+msg4+'\n回车继续')
    
def jiexi(card):
    color = ['黑桃','红桃','梅花','方块']
    number = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    return(color[card[0]]+number[card[1]])
