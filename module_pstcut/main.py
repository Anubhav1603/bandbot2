import requests
import glob
import API.time
import csv
import datetime
import parse

from matplotlib import pyplot as plt
from matplotlib import font_manager as fm

URL = "https://api.matsurihi.me/mltd/v1/events"
BURL = "https://api.matsurihi.me/mltd/v1/events/%d/rankings/logs/eventPoint/2500"
CPATH = "module_pstcut/cache_%s/%s.csv"

RESCENT_NUM = 10

print("Downloading JP fonts...")
resFont = requests.get("https://si.ster.email/dl/NotoSansCJKjp.otf")
f = open("module_pstcut/NotoSansCJKjp.otf", "wb")
f.write(resFont.content)
f.close()
print("downloaded.")


def PickFilename(fPath):
    pos = fPath.rfind("/") + 1
    return fPath[pos:]

def UpdateCSV(PSType, id):
    print(BURL%id)
    res = requests.get(BURL % id)
    print(res.json())
    data = res.json()[0]["data"]
    data = list(data)

    timeInit = data[0]["summaryTime"]
    for i, row in enumerate(data):
        data[i]["summaryTime"] = API.time.DeltaTimeISO(timeInit, row["summaryTime"])

    with open(CPATH % (PSType, id), mode = "w", newline='') as f:
        fc = csv.writer(f)
        for border in data:
            fc.writerow((border["summaryTime"], int(border["score"])))
    
def UpdateCache(PSType):
    caches = glob.glob(CPATH.format(PSType, "*"))
    caches = list(caches)
    for i, elem in enumerate(caches):
        caches[i] = elem.replace("\\", "/")
        caches[i] = PickFilename(caches[i])

    reqBody = {"type" : PSType}
    res = requests.get(URL, reqBody).json()
    resRecent = res[-RESCENT_NUM:]

    for elem in resRecent:
        if not str(elem["id"]) + ".csv" in caches:
            UpdateCSV(PSType, elem["id"])
        elif elem == resRecent[-1]:
            UpdateCSV(PSType, elem["id"])

def PlotBorder(PSType):
    reqBody = {"type" : PSType}
    res = requests.get(URL, reqBody).json()
    resRecent = res[-RESCENT_NUM:]

    legendList = []

    prop = fm.FontProperties(fname = 'module_pstcut/NotoSansCJKjp.otf')
    plt.figure(figsize=(12, 8))

    timenow = API.time.TimeISO()
    resInEvent = requests.get(URL + "?at=\"%s\"" % timenow).json()

    inEvent = False

    if len(resInEvent) == 0: inEvent = False
    else: 
        if PSType == "theater":
            if resInEvent[0]["type"] == 3:
                inEvent = True
            else:
                inEvent = False
        elif PSType == "tour":
            if resInEvent[0]["type"] == 4:
                inEvent = True
            else:
                inEvent = False

    max_x = 0

    if inEvent:
        print("NOW IN EVENTs")
        for event in resRecent:
            eventName = parse.parse("{}～{}～", event["name"])[1]
            event["purename"] = eventName

            with open(CPATH % (PSType, event["id"])) as f:
                fc = list(csv.reader(f))
                fc_T = list(zip(*fc))
                x_vals = [float(x) for x in fc_T[0]]
                y_vals = [int(x) for x in fc_T[1]]

                event["border"] = (x_vals, y_vals)

        nowEvent = resRecent[-1]
        pastEvent = resRecent[:-1]

        x_maxnum = len(nowEvent["border"][0])
        max_x = nowEvent["border"][0][-1]
        
        pastEvent.sort(key = lambda x: x["border"][1][-1])

        for event in pastEvent:
            x_vals = event["border"][0]
            y_vals = event["border"][1]
            if len(x_vals) > x_maxnum:
                x_vals = x_vals[:x_maxnum]
                y_vals = y_vals[:x_maxnum]
            plt.plot(x_vals, y_vals)
            legend = "[최종 %d점, %.0f시간] " % (event["border"][1][-1], event["border"][0][-1]) + event["purename"]
            legendList.append(legend)
        
        x_vals = nowEvent["border"][0]
        y_vals = nowEvent["border"][1]
        beginDate = nowEvent["schedule"]["beginDate"]
        endDate = nowEvent["schedule"]["endDate"]
        deltaDate = API.time.DeltaTimeISO(beginDate, endDate)

        plt.plot(x_vals, y_vals)
        legend = "[현재 %d점, %.0f시간] " % (y_vals[-1], deltaDate) + nowEvent["purename"]
        legendList.append(legend)
        
    else:
        print("NOT IN EVENT")
        for i, event in enumerate(resRecent):
            eventName = parse.parse("{}～{}～", event["name"])[1]
            event["purename"] = eventName

            with open(CPATH % (PSType, event["id"])) as f:
                fc = list(csv.reader(f))
                fc_T = list(zip(*fc))
                x_vals = [float(x) for x in fc_T[0]]
                y_vals = [int(x) for x in fc_T[1]]
                
                if max_x < x_vals[-1]: max_x = x_vals[-1]

                event["border"] = (x_vals, y_vals)

        resRecent.sort(key = lambda x: x["border"][1][-1])

        for event in resRecent:
            x_vals = event["border"][0]
            y_vals = event["border"][1]
            plt.plot(x_vals, y_vals)
            legend = "[최종 %d점, %.0f시간] " % (event["border"][1][-1], event["border"][0][-1]) + event["purename"]
            legendList.append(legend)

    plt.legend(legendList, prop=prop)
    plt.title("PS" + PSType + " border")
    plt.xlabel("Time(Hr)")
    plt.ylabel("Score(Pt)")
    plt.grid(True, axis='both', color='gray', alpha=0.7, linestyle='--')

    maxTick = int(max_x) // 24 + 1
    plt.xticks([24 * x for x in range(maxTick)])
    plt.savefig("module_pstcut/border_%s.png" % PSType, dpi = 150, bbox_inches='tight')
