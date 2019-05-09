from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import json
import requests

import param

def reqjson(URL):
	return requests.get(URL).json()

def timeparser(dateinfo):
	month = dateinfo[5:7]
	day = dateinfo[8:10]
	hour = dateinfo[11:13]
	minute = dateinfo[14:16]
	return month+'월'+day+'일 '+hour+":"+minute

def Info(msgWrite):
	json_info = reqjson('https://api.matsurihi.me/mltd/v1/events')
	json_info = json_info[-1]

	msgWrite.send_keys("[" + param.NAME + "]밀리이벤트 정보")
	msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
	event_name=json_info["name"]
	if(json_info["type"] == 3):
		msgWrite.send_keys("PSTheater "+event_name[event_name.find("～")+1:-1])
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)

		msgWrite.send_keys("시작시각 : "+timeparser(json_info["schedule"]["beginDate"]))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("후반개시 : "+timeparser(json_info["schedule"]["boostBeginDate"]))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("종료시각 : "+timeparser(json_info["schedule"]["endDate"]))
		msgWrite.send_keys(Keys.ENTER)

	elif(json_info["type"] == 4):
		msgWrite.send_keys("PSTour "+event_name[event_name.find("～")+1:-1])
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)

		msgWrite.send_keys("시작시각 : "+timeparser(json_info["schedule"]["beginDate"]))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("후반개시 : "+timeparser(json_info["schedule"]["boostBeginDate"]))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("종료시각 : "+timeparser(json_info["schedule"]["endDate"]))
		msgWrite.send_keys(Keys.ENTER)
	elif(json_info["type"] == 2):
		msgWrite.send_keys("MILLION LIVE COLLECTION")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)

		msgWrite.send_keys("시작시각 : "+timeparser(json_info["schedule"]["beginDate"]))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("드롭종료 : "+timeparser(json_info["schedule"]["endDate"]))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("가챠종료 : "+timeparser(json_info["schedule"]["pageEndDate"]))
		msgWrite.send_keys(Keys.ENTER)
	elif(json_info["type"] == 6):
		msgWrite.send_keys("WORKING☆ "+event_name[event_name.find("～")+1:-1])
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)

		msgWrite.send_keys("시작시각 : "+timeparser(json_info["schedule"]["beginDate"]))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("드롭종료 : "+timeparser(json_info["schedule"]["endDate"]))
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("가챠종료 : "+timeparser(json_info["schedule"]["pageEndDate"]))
		msgWrite.send_keys(Keys.ENTER)
	else:
		msgWrite.send_keys("알려지지 않은 이벤트 진행중")
		msgWrite.send_keys(Keys.ENTER)

def Cut(msgWrite, border):
	json_info = reqjson('https://api.matsurihi.me/mltd/v1/events')
	json_info = json_info[-1]

	msgWrite.send_keys("[" + param.NAME + "]밀리이벤트 현재컷 정보")
	msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
	if(json_info["type"] == 3):
		json_cut = reqjson("https://api.matsurihi.me/mltd/v1/events/"+str(json_info["id"])+"/rankings/logs/eventPoint/100,2500,5000,10000,25000,50000")
		cut100 = str(int(json_cut[0]["data"][-1]["score"]))
		cut2500 = str(int(json_cut[1]["data"][-1]["score"]))
		cut5000 = str(int(json_cut[2]["data"][-1]["score"]))
		cut10000 = str(int(json_cut[3]["data"][-1]["score"]))
		cut25000 = str(int(json_cut[4]["data"][-1]["score"]))
		cut50000 = str(int(json_cut[5]["data"][-1]["score"]))
		timedata = timeparser(json_cut[0]["data"][-1]["summaryTime"])
		event_name=json_info["name"]
		msgWrite.send_keys("PSTheater "+event_name[event_name.find("～")+1:-1])
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 1 or border == 0:
			msgWrite.send_keys("100위 : "+cut100)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 2 or border == 0:
			msgWrite.send_keys("2500위 : "+cut2500)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 3 or border == 0:
			msgWrite.send_keys("5000위 : "+cut5000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 4 or border == 0:
			msgWrite.send_keys("10000위 : "+cut10000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 5 or border == 0:
			msgWrite.send_keys("25000위 : "+cut25000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 6 or border == 0:
			msgWrite.send_keys("50000위 : "+cut50000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys(timedata+" 기준")
		msgWrite.send_keys(Keys.ENTER)

	elif(json_info["type"] == 4):
		json_cut = reqjson("https://api.matsurihi.me/mltd/v1/events/"+str(json_info["id"])+"/rankings/logs/eventPoint/100,2500,5000,10000,25000,50000")
		cut100 = str(int(json_cut[0]["data"][-1]["score"]))
		cut2500 = str(int(json_cut[1]["data"][-1]["score"]))
		cut5000 = str(int(json_cut[2]["data"][-1]["score"]))
		cut10000 = str(int(json_cut[3]["data"][-1]["score"]))
		cut25000 = str(int(json_cut[4]["data"][-1]["score"]))
		cut50000 = str(int(json_cut[5]["data"][-1]["score"]))
		timedata = timeparser(json_cut[0]["data"][-1]["summaryTime"])

		event_name=json_info["name"]
		msgWrite.send_keys("PSTour "+event_name[event_name.find("～")+1:-1])
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 1 or border == 0:
			msgWrite.send_keys("100위 : "+cut100)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 2 or border == 0:
			msgWrite.send_keys("2500위 : "+cut2500)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 3 or border == 0:
			msgWrite.send_keys("5000위 : "+cut5000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 4 or border == 0:
			msgWrite.send_keys("10000위 : "+cut10000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 5 or border == 0:
			msgWrite.send_keys("25000위 : "+cut25000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 6 or border == 0:
			msgWrite.send_keys("50000위 : "+cut50000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys(timedata+" 기준")
		msgWrite.send_keys(Keys.ENTER)
	else:
		msgWrite.send_keys("현재 PST이벤트 진행중이 아닙니다.")
		msgWrite.send_keys(Keys.ENTER)