import json
import requests
import parse
import time

import teletoken

command = ["밀리이벤", "밀리이벤컷", "밀리예측컷"]

def Com(params, usr_i):
	paramnum = len(params)
	newEvent = eventObj()
	try:
		if params[1] == '밀리이벤':
			return newEvent.getInfo()

		elif params[1] == '밀리이벤컷':
			if paramnum == 3:
				return newEvent.getCut(int(params[2]))
			elif paramnum == 2:
				return newEvent.getCut()

		elif params[1] == "밀리예측컷":
			if paramnum == 3:
				return newEvent.getPrecut(int(params[2]))
			elif paramnum == 2:
				return newEvent.getPrecut()
				
		return Err(False)
			
	except:
		return Err(True)

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

dicType = {1:"TST", 2:"밀리코레", 3:"PSTheater", 4:"PSTour", 5:"주년이벤트", 6:"WORKING☆", 7:"만우절 이벤트", 9:"밀리코레", 10:"PSTwinstage"}
cutEvents = [3, 4, 10]

class eventObj():
	def __init__(self):
		json_info = reqjson('https://api.matsurihi.me/mltd/v1/events')
		self.rawdata = json_info[-1]	#get last event

		self.typenum = self.rawdata["type"]	#get type
		#1:theater show time
		#2:millicore
		#3:theater
		#4:tour
		#5:anniversary
		#6:working
		#7:aprilfool
		#9:millicore(boxtype)
		#10:twin stage

		rawname = self.rawdata["name"]
		self.pureName = rawname[rawname.find("～")+1:-1]
		self.strName = dicType[self.typenum] + " " + self.pureName
	
	def getInfo(self):		
		responseChat = ""

		if self.typenum in cutEvents:
			responseChat += self.strName + "\n" \
			"시작시각 : " + timeparser(self.rawdata["schedule"]["beginDate"]) + "\n" \
			"후반개시 : " + timeparser(self.rawdata["schedule"]["boostBeginDate"]) + "\n" \
			"종료시각 : " + timeparser(self.rawdata["schedule"]["endDate"])
		
		elif self.typenum == 5:
			responseChat += self.strName + "\n" \
			"시작시각 : " + timeparser(self.rawdata["schedule"]["beginDate"]) + "\n" \
			"종료시각 : " + timeparser(self.rawdata["schedule"]["pageEndDate"])

		elif self.typenum in dicType.keys():
			responseChat += self.strName + "\n" \
			"시작시각 : " + timeparser(self.rawdata["schedule"]["beginDate"]) + "\n" \
			"드롭종료 : " + timeparser(self.rawdata["schedule"]["endDate"]) + "\n" \
			"가챠종료 : " + timeparser(self.rawdata["schedule"]["pageEndDate"])

		else:
			responseChat += "알려지지 않은 이벤트 진행중"

		return responseChat
		
	def getPrecut(self, border = 0):
		bot = None
		msg = None
		try:
			bot = teletoken.getBot()
			msg = bot.getUpdates()[-1].message
		except:
			return "텔레그램 연결이 원활하지 않습니다."

		if not self.typenum in dicType.keys():
			return "알려지지 않은 이벤트 진행중.\n타입코드 " + self.typenum
		
		if not self.typenum in cutEvents:
			return "랭킹이벤트 진행중이 아닙니다."

		time_now = int(time.strftime("%Y%m%d%H%M"))
		boost_event = timeparser_int(self.rawdata["schedule"]["boostBeginDate"])
		end_event = timeparser_int(self.rawdata["schedule"]["endDate"])
		#boost_event = 201905140152
		#end_event = 202005140152

		responseChat = "밀리이벤트 현재컷 정보\n"
		responseChat += self.strName + "\n"
		if time_now < end_event and time_now > boost_event:
			res = parse.parse("예측컷\n{}\n{}\n{}\n{}\n{}\n{}", msg.text)
			if res is None or res[0] != self.pureName:
				return "아직 예측컷 정보가 없습니다."
			else:
				responseChat = ""
				cut2500 = res[1].split()[1]
				cut5000 = res[2].split()[1]
				cut10000 = res[3].split()[1]
				cut25000 = res[4].split()[1]
				cut50000 = res[5].split()[1]
				
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
	
	def getCut(self, border = 0):
		responseChat = "밀리이벤트 현재컷 정보\n"

		if not self.typenum in dicType.keys():
			return "알려지지 않은 이벤트 진행중.\n타입코드 " + self.typenum
		
		if not self.typenum in cutEvents:
			return "랭킹이벤트 진행중이 아닙니다."

		json_cut = reqjson("https://api.matsurihi.me/mltd/v1/events/"+str(self.rawdata["id"])+"/rankings/logs/eventPoint/100,2500,5000,10000,25000,50000")
		timedata = timeparser(json_cut[0]["data"][-1]["summaryTime"])

		responseChat += self.strName + "\n"

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
