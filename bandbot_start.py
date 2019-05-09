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
		msgWrite.send_keys("지원되는 명령어 : ")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("!" + param.NAME + " 밀리이벤, 밀리이벤컷, 주사위 , 시어터, 라이브런")
		msgWrite.send_keys(Keys.ENTER)


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

			str_i = str_i_pre[len(param.NAME)+2:]

			if(len(str_i) == 0):			#!param.NAME
				bothelp(msgWrite, False)

			elif(str_i[0:4] == "밀리이벤"):												#!param.NAME 밀리이벤~
				if len(str_i) == 4:														#!param.NAME 밀리이벤
					try:
						events.Info(msgWrite)
					except:
						msgWrite.send_keys("matsurihi.me에서 응답하지 않습니다.")
						msgWrite.send_keys(Keys.ENTER)

				elif len(str_i) == 5 and str_i[4] == "컷":								#!param.NAME 밀리이벤컷
					try:
						events.Cut(msgWrite, 0)
					except:
						msgWrite.send_keys("matsurihi.me에서 응답하지 않습니다.")
						msgWrite.send_keys(Keys.ENTER)
				else:																	#!param.NAME 밀리이벤컷~
					try:
						res = parse("밀리이벤컷 {}", str_i)
						res = int(res[0])
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
			
			elif(str_i[0:3] == "주사위"):
				try:
					res = parse("주사위 {}", str_i)
					res_parse = parse("{numdice}D{maxdice}", res[0])
					if int(res_parse["numdice"]) >= 11 or int(res_parse["maxdice"]) > 99999999:
						raise ValueError
					dice.Roll(msgWrite, int(res_parse["maxdice"]), int(res_parse["numdice"]))
				except ValueError:
					dice.Err(msgWrite, True)
				except:
					dice.Err(msgWrite, False)

			elif(str_i[0:2] == "투어"):
				try:
					res = parse("투어 {isWork} {Stamina} {Score}", str_i)
					workdic = {"영업런":True, "라이브런":False}
					isWork = workdic[res["isWork"]]
					pstcalc.Tour(msgWrite, int(res["Stamina"]), int(res["Score"]), isWork)
				except:
					pstcalc.Err(msgWrite)
			elif(str_i[0:3] == "시어터"):
				try:
					res = parse("시어터 {isWork} {Stamina} {Score}", str_i)
					workdic = {"영업런":True, "라이브런":False}
					isWork = workdic[res["isWork"]]
					pstcalc.Theater(msgWrite, int(res["Stamina"]), int(res["Score"]), isWork)
				except:
					pstcalc.Err(msgWrite)
			else:
				bothelp(msgWrite, True)
		else:
			recent_chat = len(list_input)
