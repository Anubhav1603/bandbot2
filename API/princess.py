import requests as r
import parse

from API.time import TimeISO, StrfTimeISO

URL = 'https://api.matsurihi.me/mltd/v1/events/'

BORDER_SUFFIX = "%d/rankings/borders"
BORDER_CUT_SUFFIX = "%d/rankings/logs/eventPoint/%s"

TYPEDIC = {1: "TST", 2: "밀리코레", 3: "PSTheater", 4: "PSTour",
           5: "주년이벤트", 6: "WORKING☆", 7: "만우절 이벤트",
		   9: "밀리코레", 10: "PSTwinstage", 11: "PSTune", 12: "PSTwinstage",
           13: "PSTale"}

SKIP_NAME = [1, 2, 6, 9]

def jsonify(res):
    if res.status_code == 200:
        return res.json()
    else:
        print("GET Failed for: ")
        print(res.request.url)
        if res.status_code == 429:
            raise TooManyRequestsError
        else:
            print("HTTP 상태코드: ", res.status_code)
            raise APIConnectionError

class PrincessError(Exception):
    pass

class NoEventError(PrincessError):
    def __init__(self):
        super().__init__("진행중인 이벤트 없음")

class APIConnectionError(PrincessError):
    def __init__(self):
        super().__init__("API 연결 실패")

class TooManyRequestsError(PrincessError):
    def __init__(self):
        super().__init__("잠시후 다시 시도해주세요")

class WrongEventTypeError(PrincessError):
    def __init__(self):
        super().__init__("랭킹이벤트가 아닙니다.")

class UnknownEventTypeError(PrincessError):
    def __init__(self):
        super().__init__("알려지지 않은 이벤트 타입")

class APIException(PrincessError):
    def __init__(self):
        super().__init__("쿼리 파싱 실패")

class Event():
    def __init__(self, now=True):
        eventnow = None

        # Retrieve event information from PRINCESS API
        if now:
            time_ISO = TimeISO()
            res = r.get(URL+'?at='+time_ISO)
            eventnow = jsonify(res)
            if len(eventnow) != 1:
                print(eventnow)
                raise NoEventError
        else:
            res = r.get(URL)
            eventnow = jsonify(res)

        eventnow = eventnow[0]

        # Parse response
        try:
            self.eid = int(eventnow['id'])
            self.type = int(eventnow['type'])
            self.rawname = eventnow['name']
            self.schedule = eventnow['schedule']
            start = self.rawname.index('～') + 1
            temp = self.rawname[start:]
            end = temp.index('～')
            self.purename = temp[:end]
        except (ValueError, KeyError):
            raise APIException
    
        # Event type check
        if self.type not in TYPEDIC:
            raise UnknownEventTypeError
        else:
            self.strname = TYPEDIC[self.type]
            if self.type not in SKIP_NAME:
                self.strname += " " + self.purename
    
    def get_info_formatted(self):
        # 후반이 존재하는 이벤트의 경우
        if "boostBeginDate" in self.schedule:
            response = self.strname + "\n" \
                "시작 " + StrfTimeISO(self.schedule["beginDate"]) + "\n" \
                "후반 " + StrfTimeISO(self.schedule["boostBeginDate"]) + "\n" \
                "종료 " + StrfTimeISO(self.schedule["endDate"])

        # 후반이 없는 이벤트의 경우
        else:
            response = self.strname + "\n" \
                "시작시각 " + StrfTimeISO(self.schedule["beginDate"]) + "\n" \
                "드롭종료 " + StrfTimeISO(self.schedule["endDate"]) + "\n" \
                "가챠종료 " + StrfTimeISO(self.schedule["pageEndDate"])
        
        return response
    
    def get_cut_formatted(self):
        res = r.get(URL + BORDER_SUFFIX % self.eid)
        print(res.request.url)
        res = jsonify(res)

        if "eventPoint" in res:
            blist = res['eventPoint']
            blist_str = list(map(str, blist))
        else:
            raise WrongEventTypeError

        FURL = URL + BORDER_CUT_SUFFIX % (self.eid, ','.join(blist_str))
        
        res = r.get(FURL)
        res = jsonify(res)
        
        response = self.strname + '\n'
        for border in res:
            rank = border['rank']
            data = border['data']
            if 50 <= rank <= 50000:
                if data:
                    score = int(data[-1]['score'])
                    response += f"{rank}위: {score}\n"
        
        return response[:-1]