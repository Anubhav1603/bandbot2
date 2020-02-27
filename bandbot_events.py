import json
import requests
import parse
import time

import teletoken

command = ["밀리이벤", "밀리이벤컷", "밀리예측컷"]

def Com(params, usr_i):
	paramnum = len(params)
	if params[1] == '밀리이벤':
		return InfoCom()

	elif params[1] == '밀리이벤컷':
		return CutCom(paramnum, params)

	elif params[1] == "밀리예측컷":
		return PreCutCom(paramnum, params)

reqjson = lambda URL:requests.get(URL).json()

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
	return int(year + month + day + hour + minute)

def Err(isComm):
	responseChat = "events.py: \n"
	if isComm:
		responseChat += "matsurihi.me에서 응답하지 않습니다."
	else:
		responseChat += "잘못된 명령어 사용"
	return responseChat

def PreCutCom(paramnum, params):
	responseChat = ""
	try:
		if paramnum == 3:
			responseChat = PreCut(int(params[2]))
		elif paramnum == 2:
			responseChat = PreCut()
		else:
			responseChat = Err(False)
	except:
		responseChat = Err(True)

	return responseChat

def PreCut(border = 0):
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
				return "아직 예측컷 정보가 없습니다."
			else:
				cut2500 = res[1].split()[1]
				cut5000 = res[2].split()[1]
				cut10000 = res[3].split()[1]
				cut25000 = res[4].split()[1]
				cut50000 = res[5].split()[1]
				responseChat += "PSTheater " + event_name + "\n"
				if border == 2500 or border == 0:
					responseChat += "2500위 : " + cut2500 + "\n"
				if border == 5000 or border == 0:
					responseChat += "5000위 : " + cut5000 + "\n"
				if border == 10000 or border == 0:
					responseChat += "10000위 : " + cut10000 + "\n"
				if border == 25000 or border == 0:
					responseChat += "25000위 : " + cut25000 + "\n"
				if border == 50000 or border == 0:
					responseChat += "50000위 : " + cut50000 + "\n"
				responseChat += msg.date.strftime("%m.%d %H:%M")+" 기준"
				return responseChat
		else:
			return "후반전이 시작하지 않았거나 이미 끝난 이벤트입니다."
	else:
		return "현재 PST이벤트 진행중이 아닙니다."

def InfoCom():
	try:
		return Info()
	except:
		return Err(True)

def Info():
	json_info = reqjson('https://api.matsurihi.me/mltd/v1/events')
	json_info = json_info[-1]

	responseChat = "밀리이벤트 정보\n"

	event_name=json_info["name"]

	if(json_info["type"] == 3):
		responseChat += "PSTheater " + event_name[event_name.find("～")+1:-1] + "\n" \
		"시작시각 : " + timeparser(json_info["schedule"]["beginDate"]) + "\n" \
		"후반개시 : "+timeparser(json_info["schedule"]["boostBeginDate"]) + "\n" \
		"종료시각 : "+timeparser(json_info["schedule"]["endDate"])
		return responseChat

	elif(json_info["type"] == 4):
		responseChat += "PSTour " + event_name[event_name.find("～")+1:-1] + "\n" \
		"시작시각 : "+timeparser(json_info["schedule"]["beginDate"]) + "\n" \
		"후반개시 : "+timeparser(json_info["schedule"]["boostBeginDate"]) + "\n" \
		"종료시각 : "+timeparser(json_info["schedule"]["endDate"])
		return responseChat

	elif(json_info["type"] == 2 or json_info["type"] == 9):
		responseChat += "MILLION LIVE COLLECTION"
		"시작시각 : "+timeparser(json_info["schedule"]["beginDate"]) + "\n" \
		"드롭종료 : "+timeparser(json_info["schedule"]["endDate"]) + "\n" \
		"가챠종료 : "+timeparser(json_info["schedule"]["pageEndDate"])
		return responseChat

	elif(json_info["type"] == 6):
		responseChat += "WORKING☆ " + event_name[event_name.find("～")+1:-1] + "\n" \
		"시작시각 : "+timeparser(json_info["schedule"]["beginDate"]) + "\n" \
		"드롭종료 : "+timeparser(json_info["schedule"]["endDate"]) + "\n" \
		"가챠종료 : "+timeparser(json_info["schedule"]["pageEndDate"])
		return responseChat

	else:
		responseChat += "알려지지 않은 이벤트 진행중"
		return responseChat

def CutCom(paramnum, params):
	try:
		if paramnum == 3:
			return Cut(int(params[2]))
		elif paramnum == 2:
			return Cut()
		else:
			return Err(False)
	except:
		return Err(True)

def Cut(border = 0):
	json_info = reqjson('https://api.matsurihi.me/mltd/v1/events')
	json_info = json_info[-1]

	responseChat = "밀리이벤트 현재컷 정보\n"

	if json_info["type"] == 3 or json_info["type"] == 4:
		json_cut = reqjson("https://api.matsurihi.me/mltd/v1/events/"+str(json_info["id"])+"/rankings/logs/eventPoint/100,2500,5000,10000,25000,50000")
		timedata = timeparser(json_cut[0]["data"][-1]["summaryTime"])
		event_name=json_info["name"]
		if json_info["type"] == 3 :
			responseChat += "PSTheater " + event_name[event_name.find("～")+1:-1] + "\n"
		else:
			responseChat += "PSTour " + event_name[event_name.find("～")+1:-1] + "\n"

		if border == 100 or border == 0:
			cut100 = str(int(json_cut[0]["data"][-1]["score"]))
			responseChat += "100위 : " + cut100 + "\n"
		if border == 2500 or border == 0:
			cut2500 = str(int(json_cut[1]["data"][-1]["score"]))
			responseChat += "2500위 : " + cut2500 + "\n"
		if border == 5000 or border == 0:
			cut5000 = str(int(json_cut[2]["data"][-1]["score"]))
			responseChat += "5000위 : " + cut5000 + "\n"
		if border == 10000 or border == 0:
			cut10000 = str(int(json_cut[3]["data"][-1]["score"]))
			responseChat += "10000위 : " + cut10000 + "\n"
		if border == 25000 or border == 0:
			cut25000 = str(int(json_cut[4]["data"][-1]["score"]))
			responseChat += "25000위 : " + cut25000 + "\n"
		if border == 50000 or border == 0:
			cut50000 = str(int(json_cut[5]["data"][-1]["score"]))
			responseChat += "50000위 : " + cut50000 + "\n"

		responseChat += timedata + " 기준"
		return responseChat

	else:
		responseChat += "현재 PST이벤트 진행중이 아닙니다."
		return responseChat