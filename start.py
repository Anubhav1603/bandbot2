from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from parse import parse
from time import strftime,sleep

import param
import init
import teletoken

def Modules():
	import glob
	import importlib
	mods = []
	commands = []
	modules = glob.glob("bandbot_*.py")
	for module in modules:
		module_name = parse("{}.py",module)
		mod = importlib.import_module(module_name[0])
		mods.append(mod)
		commands.append(mod.command)
	return commands, mods


def bothelp(msgWrite, isWrong, commands):
	if(isWrong):
		msgWrite.send_keys("잘못된 명령어입니다.")
		msgWrite.send_keys(Keys.ENTER)
	else:
		msgWrite.send_keys(param.version)
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("https://github.com/kohs100/bandbot2")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("지원되는 명령어 : ")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("!봇 + ")
		for command in commands:
			for com in command:
				msgWrite.send_keys(", "+com)

		msgWrite.send_keys(Keys.ENTER)


def HTMLget(driver):
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	chatlist = soup.find_all("span", class_="txt")
	userlist = soup.find_all("button", class_="author")
	return len(chatlist), chatlist, userlist


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
def CommandSel(driver, msgWrite, paramnum, params, usr_i, commands, mods):
	if params[0] == '!봇' and paramnum == 1:
		bothelp(msgWrite, False, commands)
		return
	elif params[0] != '!봇':
		return

	msgWrite.send_keys("[" + param.NAME + "] ")
	msgWrite.send_keys(usr_i)
	msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)

	isCommand = False
	for i in range(0, len(commands)):			#commands = list of module.command(list of commands)
		if params[1] in commands[i]:
			mods[i].Com(driver, msgWrite, paramnum, params, usr_i)
			isCommand = True
	if not isCommand:
		bothelp(msgWrite, True, commands)





if __name__ == "__main__":
	timeFlag = int(strftime("%M")) < 30

	driver, msgWrite = init.loginRefresh(True)

	len_chat, i_chat, i_user = HTMLget(driver)
	recent_chat = len(i_chat)

	commands, mods = Modules()

	while(True):
		if (int(strftime("%M")) < 30 and timeFlag) or (int(strftime("%M")) >= 30 and not timeFlag):
			timeFlag = not timeFlag
			driver, msgWrite = init.loginRefresh(True)

		len_chat, i_chat, i_user = HTMLget(driver)

		for i in range(recent_chat-len_chat,0):
			str_i = i_chat[i].text
			usr_i = i_user[i].text
			print(usr_i + ":" + str_i)
		
			if str_i[:2] == "!봇 ":
				paramnum, params = bandparse(str_i)
				CommandSel(driver, msgWrite, paramnum, params, usr_i, commands, mods)
			
			alarm_keywords=["촉수","ㅎㅅㅋ"]
			for keyword in alarm_keywords:
				if keyword in str_i:
					bot = teletoken.getBot()
					msg = strftime("%H:%M ") + usr_i + " is calling you.\n" + str_i
					teletoken.sendChat(bot, msg)

			if "레몬스타" == usr_i:
				bot = teletoken.getBot()
				msg = "senpai alert" + strftime("%H:%M ") + str_i
				teletoken.sendChat(bot, msg)

		recent_chat = len_chat

		sleep(0.5)