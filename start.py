from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import datetime
import param
import teletoken
import sys
import glob
import importlib

from time import sleep, strftime, time

class bandChat():
	def get_msgWrite(self):
		startsec = time()
		while(True):
			try:
				self.msgWrite = self.driver.find_element_by_class_name("commentWrite")
			except:
				if(time() > startsec+20):
					now = datetime.datetime.now()
					print("CHAT LOAD ERROR at " + now.isoformat())
					raise chatError
					exit()
				continue
			break
		sleep(1)
		print("[" + param.NAME + "] " + param.version + " boot success")

	def __init__(self, isTest):
		self.chatURL = param.testchatURL if isTest else param.chatURL
		self.isTest = isTest

		chromeOptions = {"debuggerAddress":"127.0.0.1:9222"}
		capabilities = {"chromeOptions":chromeOptions}
		print("Driver initializing...")
		self.driver = webdriver.Remote("http://127.0.0.1:33333", capabilities)
		print("Driver initialized.")

		self.driver.get(self.chatURL)
		print("Get login page completed.")
		self.driver.implicitly_wait(3)

		self.driver.find_element_by_css_selector(".uBtn.-icoType.-phone").click()
		print("Get PhonenumberPage completed.")
		self.driver.implicitly_wait(3)

		Phonenumber = input("전화번호 입력 :")
		self.driver.find_element_by_id("input_local_phone_number").send_keys(Phonenumber)
		self.driver.find_element_by_css_selector(".uBtn.-tcType.-confirm").click()
		print("Get PasswordPage completed.")
		self.driver.implicitly_wait(3)

		Password = input("비밀번호 입력 :")
		self.driver.find_element_by_id("pw").send_keys(Password)
		self.driver.find_element_by_css_selector(".uBtn.-tcType.-confirm").click()
		print("Get SMSPage completed.")
		self.driver.implicitly_wait(8)
		try:
			print(self.driver.find_element_by_id("hintNumberDiv").text)
			sleep(20)
		except NoSuchElementException:
			pw_band = input("인증번호: ")
			self.driver.find_element_by_id("code").send_keys(str(pw_band))
			self.driver.find_element_by_css_selector("button.uBtn.-tcType.-confirm").click();
			print("Driver get completed.")

		self.get_msgWrite()

	def loginRefresh(self):
		self.driver.refresh()

		self.get_msgWrite()
		self.driver.implicitly_wait(30)

		if self.isTest:
			self.chatPrint("[" + param.NAME + "] 새로고침 완료")

	def chatPrint(self, str_i):
		lines = str_i.split("\n")
		for chat in lines:
			self.msgWrite.send_keys(chat)
			self.msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		self.msgWrite.send_keys(Keys.ENTER)

	def HTMLget(self):
		soup = BeautifulSoup(self.driver.page_source, 'html.parser')
		chatlist = soup.find_all("span", class_="txt")
		userlist = soup.find_all("button", class_="author")
		return len(chatlist), chatlist, userlist

class extnModules():
	emptyCall = 1
	wrongCommand = 2

	def __init__(self, guide):
		self.mods = []
		self.commands = []

		modules = glob.glob("bandbot_*.py")
		for module in modules:
			module_name = module[:-3]
			mod = importlib.import_module(module_name)
			self.mods.append(mod)
			self.commands.append(mod.command)

		self.guide = guide + self.strfModules()

	def find_and_execute(self, command_i, params, usr_i):
		for i, command in enumerate(self.commands):
			if command_i in command:
				return self.mods[i].Com(params, usr_i)

		return extnModules.wrongCommand

	def strfModules(self):
		responseChat = ""
		for command in self.commands:
			for com in command:
				responseChat += com + ", "
		return responseChat[:-2]

	def commandSel(self, params, usr_i):
		if len(params) == 1: return extnModules.emptyCall
		else: return self.find_and_execute(params[1], params, usr_i)

def sendAlarm(usr_i, str_i):
	alarm_keywords = ["촉수","ㅎㅅㅋ","히사코"]
	for keyword in alarm_keywords:
		if keyword in str_i:
			bot = teletoken.getBot()
			msg = strftime("%H:%M ") + usr_i + " is calling you.\n" + str_i
			teletoken.sendChat(bot, msg)

	alarm_users = ["레몬스타"]
	for keyuser in alarm_users:
		if keyuser == usr_i:
			bot = teletoken.getBot()
			msg = "senpai alert" + strftime("%H:%M ") + str_i
			teletoken.sendChat(bot, msg)

if not __name__ == "__main__":
	pass

elif len(sys.argv) == 1:
	print("***BANDBOT STARTED IN SERVICE MODE***")
	print("***BANDBOT STARTED IN SERVICE MODE***")
	print("***BANDBOT STARTED IN SERVICE MODE***")
	print("Auto refreshing enabled for long-term service.")
	if input("Continue? (Y)") != "Y": exit()
	
	chatRoom = bandChat(False)
	guide = param.NAME + " ver." + param.version + "\n" \
			"https://github.com/kohs100/bandbot2\n" \
			"지원되는 명령어 : \n!봇 + "
	loadedModules = extnModules()

	timeFlag = int(strftime("%M")) < 30

	len_chat, i_chat, i_user = chatRoom.HTMLget()
	recent_chat = len(i_chat)

	while(True):
		if (int(strftime("%M")) < 30 and timeFlag) or (int(strftime("%M")) >= 30 and not timeFlag):
			timeFlag = not timeFlag
			chatRoom.loginRefresh()

		len_chat, i_chat, i_user = chatRoom.HTMLget()

		for i in range(recent_chat-len_chat,0):
			str_i = i_chat[i].text
			usr_i = i_user[i].text
			print(usr_i + ":" + str_i)

			if str_i[:2] == "!봇":
				params = str_i.split(" ")
				if params[0] == "!봇":
					prefixChat = "[" + param.NAME + "] " + usr_i + "\n"
					responseChat = loadedModules.commandSel(params, usr_i)

					if responseChat == extnModules.wrongCommand:
						chatRoom.chatPrint(prefixChat + guide + loadedModules.strfModules())
					elif responseChat == extnModules.emptyCall:
						chatRoom.chatPrint(prefixChat + "잘못된 명령입니다.")
					else:
						chatRoom.chatPrint(prefixChat + responseChat)

			sendAlarm(usr_i, str_i)

		recent_chat = len_chat

		sleep(0.5)

elif sys.argv[1] == "--test":
	print("***BANDBOT STARTED IN TEST MODE***")
	print("***BANDBOT STARTED IN TEST MODE***")
	print("***BANDBOT STARTED IN TEST MODE***")
	print("Auto refreshing disabled for debugging.")
	print("Long-term operation cannot be guaranteed. Use at your own risk.")
	if input("Continue? (Y)") != "Y": exit()

	chatRoom = bandChat(True)
	guide = param.NAME + " ver." + param.version + "\n" \
			"https://github.com/kohs100/bandbot2\n" \
			"지원되는 명령어 : \n!봇 + "
	loadedModules = extnModules(guide)

	len_chat, i_chat, i_user = chatRoom.HTMLget()
	recent_chat = len(i_chat)

	while(True):
		len_chat, i_chat, i_user = chatRoom.HTMLget()

		for i in range(recent_chat-len_chat,0):
			str_i = i_chat[i].text
			usr_i = i_user[i].text
			print(usr_i + ":" + str_i)

			if str_i[:2] == "!봇":
				params = str_i.split(" ")
				if params[0] == "!봇":
					prefixChat = "[" + param.NAME + "] " + usr_i + "\n"
					responseChat = loadedModules.commandSel(params, usr_i)
					chatRoom.chatPrint(prefixChat + responseChat)

			sendAlarm(usr_i, str_i)

		recent_chat = len_chat

		sleep(0.5)

elif sys.argv[1] == "--simple-test":
	print("***BANDBOT STARTED IN SIMPLE TEST MODE***")
	print("***BANDBOT STARTED IN SIMPLE TEST MODE***")
	print("***BANDBOT STARTED IN SIMPLE TEST MODE***")
	print("this mode tests 3rd-party extensions only")
	print("test username is \"QwErTyTeSt\".")
	print("type \"!exit\" to exit\n")

	loadedModules = extnModules()

	while True:
		str_i = input("test chat: ")
		usr_i = "QwErTyTeSt"
		if str_i == "!exit": break

		print("chatResponse start--------------------\n")
		if str_i[:2] == "!봇":
			params = str_i.split(" ")
			if params[0] == "!봇":
				prefixChat = "[" + param.NAME + "] " + usr_i + "\n"
				responseChat = commandSel(params, usr_i, loadedModules)
				print(prefixChat + responseChat)
		print("\nchatResponse end:--------------------\n")