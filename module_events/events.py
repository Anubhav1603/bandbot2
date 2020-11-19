import requests
import parse
from API.time import TimeISO, StrfTimeISO
from twitter_scraper import get_tweets

PRECUTF = "{}\nイベントpt ボーダー 予想 ({})\n\n2500位 {}\n5000位 {}\n10000位 {}\n25000位 {}\n50000位 {}\n{}"
URL = 'https://api.matsurihi.me/mltd/v1/events/'

BORDER_SUFFIX = "%d/rankings/logs/eventPoint/100,2500,5000,10000,25000,50000"

dicType = {1: "TST", 2: "밀리코레", 3: "PSTheater", 4: "PSTour",
           5: "주년이벤트", 6: "WORKING☆", 7: "만우절 이벤트",
		   9: "밀리코레", 10: "PSTwinstage", 11: "PSTune", 12: "PSTwinstage"}

cutEvents = [3, 4, 10, 11, 12]

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

        return "events.py: 잘못된 명령어 사용"

    except Exception as e:
        print(e)
        return "events.py: matsurihi.me에서 응답하지 않습니다."

class eventObj():
    def __init__(self):
        timeNow = TimeISO()
        reqBody = {"at":timeNow}
        res = requests.get(URL, data = reqBody)
        eventNow = res.json()

        if len(eventNow) == 1:
            self.rawdata = eventNow[0]
            self.onEvent = True
        else:
            self.onEvent = False
            return

        self.typenum = self.rawdata["type"]  # get type
        rawname = self.rawdata["name"]
        parsedname = parse.parse("{}～{}～", rawname)
        self.pureName = parsedname[1]
        self.strName = dicType[self.typenum] + " " + self.pureName

    def getInfo(self):
        if not self.onEvent:
            return "현재 진행중인 이벤트가 없습니다."

        responseChat = ""

        if self.typenum in cutEvents:
            responseChat += self.strName + "\n" \
                "시작시각 : " + StrfTimeISO(self.rawdata["schedule"]["beginDate"]) + "\n" \
                "후반개시 : " + StrfTimeISO(self.rawdata["schedule"]["boostBeginDate"]) + "\n" \
                "종료시각 : " + StrfTimeISO(self.rawdata["schedule"]["endDate"])

        elif self.typenum == 5:
            responseChat += self.strName + "\n" \
                "시작시각 : " + StrfTimeISO(self.rawdata["schedule"]["beginDate"]) + "\n" \
                "후반개시 : " + StrfTimeISO(self.rawdata["schedule"]["boostBeginDate"]) + "\n" \
                "종료시각 : " + StrfTimeISO(self.rawdata["schedule"]["endDate"])

        elif self.typenum in dicType.keys():
            responseChat += self.strName + "\n" \
                "시작시각 : " + StrfTimeISO(self.rawdata["schedule"]["beginDate"]) + "\n" \
                "드롭종료 : " + StrfTimeISO(self.rawdata["schedule"]["endDate"]) + "\n" \
                "가챠종료 : " + StrfTimeISO(self.rawdata["schedule"]["pageEndDate"])

        else:
            return "알려지지 않은 이벤트 진행중"

        return responseChat

    def getPrecut(self, border=0):
        if not self.onEvent:
            return "현재 진행중인 이벤트가 없습니다."
        if not self.typenum in dicType.keys():
            return "알려지지 않은 이벤트 진행중.\n타입코드 " + str(self.typenum)
        if not self.typenum in cutEvents:
            return "랭킹이벤트 진행중이 아닙니다."

        res = get_tweets("alneys_al", pages = 1)
        res = list(res)[:5]
        parsed = None
        for tweet in res:
            if "イベントpt ボーダー 予想 (" in tweet['text']:
                parsed = parse.parse(PRECUTF, tweet['text'])
                break

        if parsed == None:
            print("NoCutError: Parse Failed")
            return "아직 예측컷 정보가 없습니다."

        parsed = list(parsed)

        if parsed[0] != self.pureName:
            print("NoCutError: pureName dismatch")
            return "아직 예측컷 정보가 없습니다."

        responseChat = "밀리이벤트 예측컷 정보\n"
        responseChat += self.strName + "\n"

        if border == 2500 or border == 0:
            responseChat += "2500위 : " + parsed[2] + "\n"
        if border == 5000 or border == 0:
            responseChat += "5000위 : " + parsed[3] + "\n"
        if border == 10000 or border == 0:
            responseChat += "10000위 : " + parsed[4] + "\n"
        if border == 25000 or border == 0:
            responseChat += "25000위 : " + parsed[5] + "\n"
        if border == 50000 or border == 0:
            responseChat += "50000위 : " + parsed[6] + "\n"

        responseChat += parsed[1] + " 기준"

        return responseChat

    def getCut(self, border=0):
        if not self.onEvent:
            return "현재 진행중인 이벤트가 없습니다."

        responseChat = "밀리이벤트 현재컷 정보\n"

        if not self.typenum in dicType.keys():
            return "알려지지 않은 이벤트 진행중.\n타입코드 " + self.typenum

        if not self.typenum in cutEvents:
            return "랭킹이벤트 진행중이 아닙니다."

        res = requests.get(URL + BORDER_SUFFIX % self.rawdata["id"])
        json_cut = res.json()
        timedata = StrfTimeISO(json_cut[0]["data"][-1]["summaryTime"])

        responseChat += self.strName + "\n"

        if border == 100 or border == 0:
            cut = str(int(json_cut[0]["data"][-1]["score"]))
            responseChat += "100위 : " + cut + "\n"
        if border == 2500 or border == 0:
            cut = str(int(json_cut[1]["data"][-1]["score"]))
            responseChat += "2500위 : " + cut + "\n"
        if border == 5000 or border == 0:
            cut = str(int(json_cut[2]["data"][-1]["score"]))
            responseChat += "5000위 : " + cut + "\n"
        if border == 10000 or border == 0:
            cut = str(int(json_cut[3]["data"][-1]["score"]))
            responseChat += "10000위 : " + cut + "\n"
        if border == 25000 or border == 0:
            cut = str(int(json_cut[4]["data"][-1]["score"]))
            responseChat += "25000위 : " + cut + "\n"
        if border == 50000 or border == 0:
            cut = str(int(json_cut[5]["data"][-1]["score"]))
            responseChat += "50000위 : " + cut + "\n"

        responseChat += timedata + " 기준"
        return responseChat
