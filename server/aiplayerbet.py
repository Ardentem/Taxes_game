import json
import random

def aibet_first(circle,card1,card2):
    if circle < 2:
        betnum = 10#愿意加注多少
    else:
        betnum = 0
    if card1[1] == card2[1]:
        #对子
        if circle == 0:
            betnum = betnum + 30
        elif circle == 1:
            betnum = betnum + 40
        elif circle == 2:
            betnum = betnum + 30
    if card1[0] == card2[0]:
        #同花
        if circle == 0:
            betnum = betnum + 30
        elif circle == 1:
            betnum = betnum + 20
        elif circle == 2:
            betnum = betnum + 20
    #大牌
    if card1[1] > 9:
        if circle == 0:
            betnum = betnum + 10
    if card1[1] > 11:
        if circle < 3:
            betnum = betnum + 20
    if card2[1] > 9:
        if circle == 0:
            betnum = betnum + 10
    if card2[1] > 11:
        if circle < 3:
            betnum = betnum + 20
    return(betnum)

def aibet_second(circle,card1,card2,card3,card4,card5):
    betnum = 0
    numlist = [card1[1],card2[1],card3[1],card4[1],card5[1]]
    numlist.sort()
    # 暂时还没写
    return(9999)

def aibet_third(circle,card1,card2,card3,card4,card5,card6):
    betnum = 0
    numlist = [card1[1],card2[1],card3[1],card4[1],card5[1],card6[1]]
    numlist.sort()
    # 暂时还没写
    return(9999)