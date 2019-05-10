from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import random

import param

def Gag(msgWrite):
	f = open("gag.txt",'r')
	lines = f.readlines()
	gagnum = random.randrange(0,360)
	msgWrite.send_keys("[" + param.NAME + "] " + lines[gagnum])
	msgWrite.send_keys(Keys.ENTER)
