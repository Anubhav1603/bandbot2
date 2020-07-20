import json, requests, re
from bs4 import BeautifulSoup

command = ["카드"]

idolDict = {"하루카": 1, "치하야": 2, "미키": 3,
            "유키호": 4, "야요이": 5, "마코토": 6,
            "이오리": 7, "타카네": 8, "리츠코": 9,
            "아즈사": 10, "아미": 11, "마미": 12,
            "히비키": 13, "미라이": 14, "시즈카": 15,
            "츠바사": 16, "코토하": 17, "엘레나": 18,
            "미나코": 19, "메구미": 20, "마츠리": 21,
            "세리카": 22, "아카네": 23, "안나": 24,
            "미치코": 25, "유리코": 26, "사요코": 27,
            "아리사": 28, "우미": 29, "이쿠": 30,
            "토모카": 31, "에밀리": 32, "시호": 33,
            "아유무": 34, "히나타": 35, "카나": 36,
            "나오": 37, "치즈루": 38, "코노미": 39,
            "타마키": 40, "후카": 41, "미야": 42,
            "노리코": 43, "미즈키": 44, "카렌": 45,
            "리오": 46, "스바루": 47, "레이카": 48,
            "모모코": 49, "줄리아": 50, "츠무기": 51,
            "카오리": 52, "로코": 25, "날개": 16, 
            "금붕어": 51, "바지락": 17, "미래": 15,
            "미라": 15, "성모": 31, "아이미": 50,
            "검젤좋": 33, "갈젤좋": 42, "공주": 21,
            "축제": 21, "공룡": 26,}

rarityDict = {1: "N", 2: "R", 3: "SR", 4: "SSR"}
rrarityDict = {"N": 1, "R": 2, "SR": 3, "SSR": 4}


def reqjson(URL): return requests.get(URL).json()

URL = "https://api.matsurihi.me/mltd/v1/cards?idolId=%d"

URL_DB = "https://imas.gamedbs.jp/mlth/chara/show/%d"

def isInteger(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def GetCardName(cardObj):
        resp = "["
        resp += str(cardObj["id"])
        resp += "] "
        resp += cardObj["name"]
        return resp
        
def GetCardList(idolNum, rarity):
    res = reqjson(URL % idolNum)
    idolName = res[0]["name"]
    nameLen = len(idolName)
    response = ""

    if rarity == 1:
        for cardObj in res:
            if cardObj["rarity"] == rarity:
                response += GetCardName(cardObj)
                response += "\n"
    else:
        for cardObj in res:
            if cardObj["rarity"] == rarity:
                response += GetCardName(cardObj)[:-(nameLen + 1)]
                response += "\n"
    
    return response[:-1]
    
def GetCardInfo(idolNum, rarity, cardId):
    res = reqjson(URL % idolNum)
    idolName = res[0]["name"]
    cardName = ""

    for cardObj in res:
        if cardObj["rarity"] == rarity and cardObj["id"] == cardId:
            cardName = cardObj["name"]
    
    res = requests.get(URL_DB % idolNum)
    soup = BeautifulSoup(res.text, "html.parser")
    soup_links = soup.findAll("a", title = "詳細を表示")

    if cardName == idolName:
        return soup_links[0].attrs["href"]

    nameLen = len(idolName)
    cardName = cardName[:-(nameLen + 1)]

    for link in soup_links[1:]:
        if link.contents[2] == cardName:
            return link.attrs["href"]

    return "cardinfo.py: 카드를 찾을 수 없습니다."
            
def Com(params, usr_i):
    paramNum = len(params)

    if paramNum == 4:
        if params[2] in idolDict:
            if params[3] in rrarityDict:
                return GetCardList(idolDict[params[2]],
                                   rrarityDict[params[3]])
            else:
                return "cardinfo.py: 잘못된 레어리티"
        else:
            return "cardinfo.py: 잘못된 아이돌 이름"
    elif paramNum == 5:
        if params[2] in idolDict:
            if params[3] in rrarityDict:
                if isInteger(params[4]):
                    return GetCardInfo(idolDict[params[2]],
                                       rrarityDict[params[3]],
                                       int(params[4]))
                else:
                    return "cardinfo.py: 잘못된 id"
            else:
                return "cardinfo.py: 잘못된 레어리티"
        else:
            return "cardinfo.py: 잘못된 아이돌 이름"
    else:
        return "cardinfo.py: 사용법:\n" \
               "!봇 카드 [이름] [N|R|SR|SSR]\n" \
               "!봇 카드 [이름] [N|R|SR|SSR] [id]"