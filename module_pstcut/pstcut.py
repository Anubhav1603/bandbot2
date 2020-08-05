import requests
import glob
import timeAPI
import csv
import datetime

URL = "https://api.matsurihi.me/mltd/v1/events"
BURL = "https://api.matsurihi.me/mltd/v1/events/%d/rankings/logs/eventPoint/2500"
CPATH = "module_pstcut/cache_%s/%s.csv"

command = ["밀리역대컷"]

def PickFilename(fPath):
    pos = fPath.rfind("/") + 1
    return fPath[pos:]

def UpdateCSV(PSType, id):
    res = requests.get(BURL % id)
    data = res.json()[0]["data"]
    data = list(data)

    timeInit = data[0]["summaryTime"]
    for i, row in enumerate(data):
        data[i]["summaryTime"] = timeAPI.DeltaTimeISO(timeInit, row["summaryTime"])

    with open(CPATH % (PSType, id), mode = "w") as f:
        fc = csv.writer(f)
        for border in data:
            fc.writerow([border["summaryTime"], border["score"]])
    
def UpdateCache(PSType):
    caches = glob.glob(CPATH.format(PSType, "*"))
    caches = list(caches)
    for i, elem in enumerate(caches):
        caches[i] = elem.replace("\\", "/")
        caches[i] = PickFilename(caches[i])

    reqBody = {"type" : PSType}
    res = requests.get(URL, reqBody).json()
    resRecent = res[-8:]

    for elem in resRecent:
        if not str(elem["id"]) + ".csv" in caches:
            UpdateCSV(PSType, elem["id"])
        elif elem == resRecent[-1]:
            UpdateCSV(PSType, elem["id"])
    

def PlotBorder(PSType):
    pass
                



def Com(params, usr_i):
    paramnum = len(params)

    if paramnum == 3:
        if params[2] in ["시어터", "투어"]:
            UpdateCache("theater" if params[2] == "시어터" else "tour")
        else:
            return "pstcut.py: 사용법\n!봇 밀리역대컷 [투어|시어터]"
    else:
        return "pstcut.py: 사용법\n!봇 밀리역대컷 [투어|시어터]"