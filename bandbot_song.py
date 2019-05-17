from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pathlib
import zipfile
import os
import csv

def makezip(pathmusic):
	zip_temp = zipfile.ZipFile('Music_pre.zip','w')
	zip_temp.write(pathmusic, pathmusic, compress_type=zipfile.ZIP_STORED)
	zip_temp.close()
	zip_temp = zipfile.ZipFile('Music.zip','w')
	zip_temp.write('Music_pre.zip', compress_type=zipfile.ZIP_STORED)
	zip_temp.close()

def uploadZip(msgWrite, driver, musicname):
	f = open('songdb.csv', 'r', encoding='utf-8')
	rdr = csv.reader(f)

	isFailed = True
	for data in rdr:
		if musicname == data[0]:
			makezip(data[1])
			isFailed = False
			break;
	if isFailed:
		msgWrite.send_keys("음악을 찾을수 없습니다.")
		msgWrite.send_keys(Keys.ENTER)
		return
	driver.find_element_by_css_selector("input._fileUploadBtn").send_keys("Music.zip")
	msgWrite.send_keys("음악파일을 찾았습니다.")
	msgWrite.send_keys(Keys.ENTER)

def cd(dir_user, msgWrite, dirtos):
	dir_user_back = dir_user

	dirto=dirtos[0]
	for word in dirtos[1:]:
		dirto = dirto + " " + word

	if dirto == "..":
		dir_user = dir_user / ".."
		msgWrite.send_keys("cd: Success")
		msgWrite.send_keys(Keys.ENTER)
		return dir_user

	isSuccess = False
	for lsname in list(dir_user.glob("*")):
		if dirto == lsname.name:
			dir_user = dir_user / dirto
			isSuccess = True
			break

	if not isSuccess:
		msgWrite.send_keys("cd: Wrong name")
		msgWrite.send_keys(Keys.ENTER)
		return dir_user_back
	elif not dir_user.is_dir():
		msgWrite.send_keys("cd: Not a directory")
		msgWrite.send_keys(Keys.ENTER)
		return dir_user_back


	msgWrite.send_keys("cd: Success")
	msgWrite.send_keys(Keys.ENTER)
	return dir_user

def ls(dir_user, msgWrite):
	msgWrite.send_keys("ls: Listing files...")
	msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
	for lsname in list(dir_user.glob("*")):
		if lsname.is_dir():
			msgWrite.send_keys("<DIR>")
		msgWrite.send_keys(lsname.name)
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
	msgWrite.send_keys("ls: Listing end")
	msgWrite.send_keys(Keys.ENTER)

def pwd(dir_user, msgWrite):
	msgWrite.send_keys("pwd: " + dir_user._str)
	msgWrite.send_keys(Keys.ENTER)

def dl(dir_user, msgWrite, driver, filename):
	driver.find_element_by_css_selector("input._fileUploadBtn").send_keys("Music.zip")

def Err(msgWrite, isWrong):
	msgWrite.send_keys("잘못된 명령어 사용법입니다.")
	msgWrite.send_keys(Keys.ENTER)