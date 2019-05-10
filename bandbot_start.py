from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

import re
from parse import parse
from time import strftime

import param
import bandbot_events as events
import bandbot_dice as dice
import bandbot_pstcalc as pstcalc
from bandbot_init import *

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
		msgWrite.send_keys("!" + param.NAME + " 밀리이벤, 밀리이벤컷, 주사위 , 시어터, 투어")
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


if __name__ == "__main__":
	timeFlag = True
	if int(strftime("%M")) >= 30:
		timeFlag = False
	else:
		timeFlag = True
	driver, msgWrite = loginRefresh(True)

	compiled_regex = re.compile("^!"+param.NAME)

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	list_input = soup.find_all("span", class_="txt", string=compiled_regex)
	recent_chat = len(list_input)

	while(True):
		if (int(strftime("%M")) < 30 and timeFlag) or (int(strftime("%M")) >= 30 and not timeFlag):
			timeFlag = not timeFlag
			start_flag = True
			driver, msgWrite = loginRefresh(True)

		soup = BeautifulSoup(driver.page_source, 'html.parser')
		list_input = soup.find_all("span", class_="txt", string=compiled_regex)

		if(len(list_input) > recent_chat):
			recent_chat = len(list_input)
			str_i_pre = list_input[-1].text		#str_i가 최신 채팅 내용(!param.NAME으로 시작하는)
			print(str_i_pre)

			paramnum, params = bandparse(str_i_pre)

			if paramnum == 1:
				bothelp(msgWrite, False)

			elif params[1] == '밀리이벤':
				try:
					events.Info(msgWrite)
				except:
					events.Err(msgWrite)
			elif params[1] == '밀리이벤컷':
				if paramnum == 3:
					res = int(params[2])
					try:
						if res == 100:
							events.Cut(msgWrite, 1)
						elif res == 2500:
							events.Cut(msgWrite, 2)
						elif res == 5000:
							events.Cut(msgWrite, 3)
						elif res == 10000:
							events.Cut(msgWrite, 4)
						elif res == 25000:
							events.Cut(msgWrite, 5)
						elif res == 50000:
							events.Cut(msgWrite, 6)
						else:
							raise ValueError
					except:
						bothelp(msgWrite, True)
				elif paramnum == 2:
					try:
						events.Cut(msgWrite, 0)
					except:
						events.Err(msgWrite)
				else:
					bothelp(msgWrite, True)
			elif params[1] == "주사위":
				if paramnum == 3:
					try:
						res = parse("{}D{}", params[2])
						if int(res[0]) >= 11 or int(res[1]) > 99999999:
							raise ValueError
						dice.Roll(msgWrite, int(res[0]), int(res[1]))
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
		else:
			recent_chat = len(list_input)