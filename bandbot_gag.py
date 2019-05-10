from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import random
import codecs

import param


def Gag(msgWrite):
	f = codecs.open("gag.txt",'r', encoding='utf-8')
	lines = f.readlines()
	gagnum = random.randrange(0,360)
	msgWrite.send_keys("[" + param.NAME + "] " + lines[gagnum])
	msgWrite.send_keys(Keys.ENTER)
