import requests as r
import parse
from bs4 import BeautifulSoup
from API.time import TimeISO

from module_events.events import cutEvents, dicType

command = ["밀리예측컷"]
URL = 'https://api.matsurihi.me/mltd/v1/events/'
PRECUTF = "{}イベントpt ボーダー 予想 ({})☆4  {}☆3  {}☆2  {}☆1  {}#ミリシタ#ミリシタボーダー\n"

def error(msg):
    return "mlprecut.py: " + msg

def Com(params, usr_i):
    paramnum = len(params)
    try:
        if params[1] == "밀리예측컷":
            if paramnum == 3:
                return getPrecut(int(params[2]))
            elif paramnum == 2:
                return getPrecut()

        return error("잘못된 명령어 사용")

    except Exception as e:
        print(e)
        return error("크롤링 실패")

def getEvent():
    timeNow = TimeISO()
    req = {"at": timeNow}
    res = r.get(URL, data=req)
    return res.json()

def getPrecut(border = 0):
    enow = getEvent()
    if not enow:
        return error("진행중인 이벤트 없음")
    else:
        enow = enow[0]
    
    typenum = enow["type"]

    if not typenum in dicType.keys():
        return error("알려지지 않은 이벤트 진행중\n타입코드 %d"%typenum)
    if not typenum in cutEvents:
        return error("비PST이벤트 진행중(%d)"%typenum)

    rawname = enow["name"]
    parsedname = parse.parse("{}～{}～", rawname)
    purename = parsedname[1]
    strname = dicType[typenum] + " " + purename

    res = r.get("https://syndication.twitter.com/timeline/profile?screen_name=alneys_al")
    res = res.json()["body"]
    soup = BeautifulSoup(res, 'html.parser')
    ts = soup.find_all("p", {'class', 'timeline-Tweet-text'})
    for t in ts:
        if "イベントpt ボーダー 予想 (" in t.text:
            parsed = parse.parse(PRECUTF, t.text)
            break
    
    if parsed == None:
        print("Parse Failed")
        print(t.text)
        return error("아직 예측컷 정보가 없습니다.")
    
    parsed = list(parsed)

    if parsed[0] != purename:
        print("purename dismatch")
        return error("아직 예측컷 정보가 없습니다.")
    
    responseChat = "밀리이벤트 예측컷 정보\n"
    responseChat += strname + "\n"

    if border == 2500 or border == 0:
        responseChat += "2500위 : " + parsed[2] + "\n"
    if border == 5000 or border == 0:
        responseChat += "5000위 : " + parsed[3] + "\n"
    if border == 10000 or border == 0:
        responseChat += "10000위 : " + parsed[4] + "\n"
    if border == 25000 or border == 0:
        responseChat += "25000위 : " + parsed[5] + "\n"

    responseChat += parsed[1] + " 기준"

    return responseChat