from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import json
import requests
import parse
import time

import param
import teletoken

command = ["밀리이벤","밀리이벤컷","밀리예측컷"]

def Com(driver, msgWrite, paramnum, params, usr_i):
	if params[1] == '밀리이벤':
		InfoCom(msgWrite)

	elif params[1] == '밀리이벤컷':
		CutCom(msgWrite, paramnum, params)

	elif params[1] == "밀리예측컷":
		PreCutCom(msgWrite, paramnum, params)

def reqjson(URL):
	return requests.get(URL).json()

def timeparser(dateinfo):
	year = dateinfo[0:4]
	month = dateinfo[5:7]
	day = dateinfo[8:10]
	hour = dateinfo[11:13]
	minute = dateinfo[14:16]
	return month+'월'+day+'일 '+hour+":"+minute

def timeparser_int(dateinfo):
	year = dateinfo[0:4]
	month = dateinfo[5:7]
	day = dateinfo[8:10]
	hour = dateinfo[11:13]
	minute = dateinfo[14:16]
	return int(year+month+day+hour+minute)

def Err(msgWrite, isComm):
	msgWrite.send_keys("events.py:")
	if isComm:
		msgWrite.send_keys("matsurihi.me에서 응답하지 않습니다.")
		msgWrite.send_keys(Keys.ENTER)
	else:
		msgWrite.send_keys("잘못된 명령어 사용")
		msgWrite.send_keys(Keys.ENTER)



def PreCutCom(msgWrite, paramnum, params):
	try:
		if paramnum == 3:
			PreCut(msgWrite, int(params[2]))
		elif paramnum == 2:
			PreCut(msgWrite)
		else:
			Err(msgWrite, False)
	except:
		Err(msgWrite, True)

def PreCut(msgWrite, border = 0):
	json_info = reqjson('https://api.matsurihi.me/mltd/v1/events')
	json_info = json_info[-1]

	event_type = json_info["type"]
	#event_type = 3

	event_name = json_info["name"]
	event_name = event_name[event_name.find("～")+1:-1]
	#event_name = "プリムラ"


	if event_type == 3 or event_type == 4:
		time_now = int(time.strftime("%Y%m%d%H%M"))
		boost_event = timeparser_int(json_info["schedule"]["boostBeginDate"])
		end_event = timeparser_int(json_info["schedule"]["endDate"])
		#boost_event = 201905140152
		#end_event = 202005140152
		if time_now < end_event and time_now > boost_event:
			bot = teletoken.getBot()
			msg = bot.getUpdates()[-1].message
			res = parse.parse("예측컷\n{}\n{}\n{}\n{}\n{}\n{}", msg.text)

			if res is None or res[0] != event_name:
				msgWrite.send_keys("아직 예측컷 정보가 없습니다.")
				msgWrite.send_keys(Keys.ENTER)
			else:
				cut2500 = res[1][5:]
				cut5000 = res[2][5:]
				cut10000 = res[3][6:]
				cut25000 = res[4][6:]
				cut50000 = res[5][7:]
				msgWrite.send_keys("PSTheater "+event_name)
				msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
				if border == 2500 or border == 0:
					msgWrite.send_keys("2500위 : "+cut2500)
					msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
				if border == 5000 or border == 0:
					msgWrite.send_keys("5000위 : "+cut5000)
					msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
				if border == 10000 or border == 0:
					msgWrite.send_keys("10000위 : "+cut10000)
					msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
				if border == 25000 or border == 0:
					msgWrite.send_keys("25000위 : "+cut25000)
					msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
				if border == 50000 or border == 0:
					msgWrite.send_keys("50000위 : "+cut50000)
					msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
				msgWrite.send_keys(msg.date.strftime("%m.%d %H:%M")+" 기준")
				msgWrite.send_keys(Keys.ENTER)
		else:
			msgWrite.send_keys("후반전이 시작하지 않았거나 이미 끝난 이벤트입니다.")
			msgWrite.send_keys(Keys.ENTER)
	else:
		msgWrite.send_keys("현재 PST이벤트 진행중이 아닙니다.")
		msgWrite.send_keys(Keys.ENTER)


def InfoCom(msgWrite):
	try:
		Info(msgWrite)
	except:
		Err(msgWrite, True)

def Info(msgWrite):
	json_info = reqjson('https://api.matsurihi.me/mltd/v1/events')
	json_info = json_info[-1]

	msgWrite.send_keys("밀리이벤트 정보")
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

def CutCom(msgWrite, paramnum, params):
	try:
		if paramnum == 3:
			Cut(msgWrite, int(params[2]))
		elif paramnum == 2:
			Cut(msgWrite)
		else:
			Err(msgWrite, False)
	except:
		Err(msgWrite, True)

def Cut(msgWrite, border = 0):
	json_info = reqjson('https://api.matsurihi.me/mltd/v1/events')
	json_info = json_info[-1]

	msgWrite.send_keys("밀리이벤트 현재컷 정보")
	msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
	if json_info["type"] == 3 or json_info["type"] == 4:
		json_cut = reqjson("https://api.matsurihi.me/mltd/v1/events/"+str(json_info["id"])+"/rankings/logs/eventPoint/100,2500,5000,10000,25000,50000")
		timedata = timeparser(json_cut[0]["data"][-1]["summaryTime"])
		event_name=json_info["name"]
		if json_info["type"] == 3 :
			msgWrite.send_keys("PSTheater "+event_name[event_name.find("～")+1:-1])
		else:
			msgWrite.send_keys("PSTour "+event_name[event_name.find("～")+1:-1])
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 100 or border == 0:
			cut100 = str(int(json_cut[0]["data"][-1]["score"]))
			msgWrite.send_keys("100위 : "+cut100)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 2500 or border == 0:
			cut2500 = str(int(json_cut[1]["data"][-1]["score"]))
			msgWrite.send_keys("2500위 : "+cut2500)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 5000 or border == 0:
			cut5000 = str(int(json_cut[2]["data"][-1]["score"]))
			msgWrite.send_keys("5000위 : "+cut5000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 10000 or border == 0:
			cut10000 = str(int(json_cut[3]["data"][-1]["score"]))
			msgWrite.send_keys("10000위 : "+cut10000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 25000 or border == 0:
			cut25000 = str(int(json_cut[4]["data"][-1]["score"]))
			msgWrite.send_keys("25000위 : "+cut25000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		if border == 50000 or border == 0:
			cut50000 = str(int(json_cut[5]["data"][-1]["score"]))
			msgWrite.send_keys("50000위 : "+cut50000)
			msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys(timedata+" 기준")
		msgWrite.send_keys(Keys.ENTER)
	else:
		msgWrite.send_keys("현재 PST이벤트 진행중이 아닙니다.")
		msgWrite.send_keys(Keys.ENTER)