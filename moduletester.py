from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from time import sleep

import start



if __name__ == "__main__":
	driver, msgWrite = start.initLogin()

	len_chat, i_chat, i_user = start.HTMLget(driver)
	recent_chat = len(i_chat)

	commands, mods = start.Modules()
	while(True):
		len_chat, i_chat, i_user = start.HTMLget(driver)

		for i in range(recent_chat-len_chat,0):
			str_i = i_chat[i].text
			usr_i = i_user[i].text
			print(usr_i + ":" + str_i)
		
			start.newChat(usr_i, str_i)

		recent_chat = len_chat

		sleep(0.5)