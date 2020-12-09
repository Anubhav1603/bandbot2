import requests as r
import parse
from bs4 import BeautifulSoup
from API.time import TimeISO

from API.princess import *
from extensions import ModuleBase, single_chat

PRECUTF = "{}イベントpt ボーダー 予想 ({})☆4{}☆3{}☆2{}☆1{}#ミリシタ#ミリシタボーダー\n"

class Module(ModuleBase):
    commands = ["밀리예측컷"]

    @single_chat
    def run(self, params, usr_i):
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

def error(msg):
    return "mlprecut.py: " + msg

def getPrecut(border = 0):
    try:
        enow = Event()

    except PrincessError as e:
        print(e)
        return "mlprecut.py: " + str(e)

    except Exception as e:
        print(e)
        return "mlprecut.py: 처리되지 않은 예외"
        
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

    if parsed[0] != enow.purename:
        print("purename dismatch")
        return error("아직 예측컷 정보가 없습니다.")
    
    responseChat = "예측컷 정보\n"
    responseChat += enow.strname + "\n"

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