from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import random

import param


def Roll(msgWrite, dicemax, dicenum):
	for i in range(dicenum):
		dice=random.randrange(1,dicemax+1)
		msgWrite.send_keys("[주사위]"+str(i+1)+" 값: "+str(dice))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
	msgWrite.send_keys(Keys.ENTER)

def Err(msgWrite, isToomany):
	if isToomany:
		msgWrite.send_keys("[" + param.NAME + "] 너무 많은 주사위입니다.")
		msgWrite.send_keys(Keys.ENTER)
	else:
		msgWrite.send_keys("[" + param.NAME + "] 잘못된 주사위 명령입니다.")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("사용법 : ")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("!" + param.NAME + " 주사위 (주사위갯수)D(최대값)")
		msgWrite.send_keys(Keys.ENTER)