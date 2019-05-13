from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from parse import parse
from time import strftime,sleep

import param
import bandbot_events as events
import bandbot_dice as dice
import bandbot_pstcalc as pstcalc
import bandbot_init as init
import bandbot_gag as gag

def bothelp(msgWrite, isWrong):
	if isWrong:
		msgWrite.send_keys("[" + param.NAME + "] 잘못된 명령어입니다.")
		msgWrite.send_keys(Keys.ENTER)
	else:
		msgWrite.send_keys("[" + param.NAME + "] " + param.version)
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("https://github.com/kohs100/bandbot2")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("지원되는 명령어 : ")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("!" + param.NAME + " 밀리이벤, 밀리이벤컷, 주사위 , 시어터, 투어, 개그")
		msgWrite.send_keys(Keys.ENTER)

def bandparse(str_i):
	str_i = str_i + ' '

	isBlank = True
	paramctr = 0
	word = ''
	words = []

	for ptr in range(len(str_i)):
		if isBlank and str_i[ptr] == ' ':
			isBlank = True
		elif not isBlank and str_i[ptr] == ' ':
			isBlank = True
			words.append(word)
			word = ''
		elif isBlank and str_i[ptr] != ' ':
			isBlank = False
			paramctr = paramctr + 1
			word = word + str_i[ptr]
		elif not isBlank and str_i[ptr] != ' ':
			isBlank = False
			word = word + str_i[ptr]

	return paramctr, words
#	|
#	|
#	V
def CommandSel(paramnum, params):
	if paramnum == 1:
		bothelp(msgWrite, False)

	elif params[1] == '밀리이벤':
		try:
			events.Info(msgWrite)
		except:
			events.Err(msgWrite, True)

	elif params[1] == '밀리이벤컷':
		try:
			if paramnum == 3:
				events.Cut(msgWrite, int(params[2]))
			elif paramnum == 2:
				events.Cut(msgWrite, 0)
			else:
				bothelp(msgWrite, True)
		except ValueError:
			events.Err(msgWrite, False)
		except:
			events.Err(msgWrite, True)
		
	elif params[1] == "주사위":
		if paramnum == 3:
			try:
				res = parse("{}D{}", params[2])
				if int(res[0]) >= 11 or int(res[1]) > 99999999:
					raise ValueError
				dice.Roll(msgWrite, int(res[1]), int(res[0]))
			except ValueError:
				dice.Err(msgWrite, True)
			except:
				dice.Err(msgWrite, False)
		else:
			dice.Err(msgWrite, False)

	elif params[1] == "시어터":	#EX) !botname 시어터 영업런 160 300000
		if paramnum == 5:
			try:
				workdic = {"영업런":True, "라이브런":False}
				isWork = workdic[params[2]]
				pstcalc.Theater(msgWrite, int(params[3]), int(params[4]), isWork)
			except:
				pstcalc.Err(msgWrite)
		else:
			pstcalc.Err(msgWrite)

	elif params[1] == "투어":	#EX) !botname 시어터 영업런 160 300000
		if paramnum == 5:
			try:
				workdic = {"영업런":True, "라이브런":False}
				isWork = workdic[params[2]]
				pstcalc.Tour(msgWrite, int(params[3]), int(params[4]), isWork)
			except:
				pstcalc.Err(msgWrite)
		else:
			pstcalc.Err(msgWrite)

	elif params[1] == "개그":
		if paramnum == 2:
			gag.Gag(msgWrite)
		else:
			bothelp(msgWrite, True)
	else:
		bothelp(msgWrite, True)

def HTMLget(driver):
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	chatlist = soup.find_all("span", class_="txt")
	userlist = soup.find_all("button", class_="author")
	return len(chatlist), chatlist, userlist

if __name__ == "__main__":
	timeFlag = int(strftime("%M")) < 30

	driver, msgWrite = init.loginRefresh(True)

	len_chat, i_chat, i_user = HTMLget(driver)
	recent_chat = len(i_chat)

	while(True):
		if (int(strftime("%M")) < 30 and timeFlag) or (int(strftime("%M")) >= 30 and not timeFlag):
			timeFlag = not timeFlag
			driver, msgWrite = init.loginRefresh(True)

		len_chat, i_chat, i_user = HTMLget(driver)

		for i in range(recent_chat-len_chat,0):
			print(i_user[i].text + ":" + i_chat[i].text)

			paramnum, params = bandparse(i_chat[i].text)
			if i_chat[i].text[:len(param.NAME)+1] == "!"+param.NAME:
				if i_user[i].text == param.BOT_NICK:
					msgWrite.send_keys("@"+i_user[i].text)
					msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
				else:
					msgWrite.send_keys("@"+i_user[i].text)
					sleep(0.1)
					msgWrite.send_keys(Keys.ENTER)
					msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
				CommandSel(paramnum, params)
		recent_chat = len_chat

		sleep(0.4)