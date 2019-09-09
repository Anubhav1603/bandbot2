from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import random
from parse import parse
import param

command = ["주사위"]

def Com(driver, msgWrite, paramnum, params, usr_i):
	if paramnum == 2:
		try:
			res = parse("{}D{}", params[1])
			if int(res[0]) >= 11 or int(res[1]) > 99999999:
				raise ValueError
			Roll(msgWrite, int(res[1]), int(res[0]))
		except ValueError:
			Err(msgWrite, True)
		except:
			Err(msgWrite, False)
	else:
		Err(msgWrite, False)

def Roll(msgWrite, dicemax, dicenum):
	for i in range(dicenum):
		dice=random.randrange(1,dicemax+1)
		msgWrite.send_keys("[주사위]"+str(i+1)+" 값: "+str(dice))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
	msgWrite.send_keys(Keys.ENTER)

def Err(msgWrite, isToomany):
	msgWrite.send_keys("dice.py:")
	if isToomany:
		msgWrite.send_keys("너무 많은 주사위입니다.")
		msgWrite.send_keys(Keys.ENTER)
	else:
		msgWrite.send_keys("잘못된 주사위 명령입니다.")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("사용법 : ")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("!주사위 (주사위갯수)D(최대값)")
		msgWrite.send_keys(Keys.ENTER)