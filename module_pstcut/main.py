import requests
import glob
import timeAPI
import csv
import datetime
import parse

from matplotlib import pyplot as plt

URL = "https://api.matsurihi.me/mltd/v1/events"
BURL = "https://api.matsurihi.me/mltd/v1/events/%d/rankings/logs/eventPoint/2500"
CPATH = "module_pstcut/cache_%s/%s.csv"

RESCENT_NUM = 10

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

    # plt.rc('font', family = "MS Gothic")
    plt.rc('font', family = "fonts-noto-cjk")
    plt.figure(figsize=(12,8))

    max_x = 0

    for event in resRecent:
        eventName = parse.parse("{}～{}～", event["name"])[1]

        with open(CPATH % (PSType, event["id"])) as f:
            fc = list(csv.reader(f))
            fc_T = list(zip(*fc))
            x_vals = [float(x) for x in fc_T[0]]
            y_vals = [int(x) for x in fc_T[1]]

            if max_x < x_vals[-1]:
                max_x = x_vals[-1]

            plt.plot(x_vals, y_vals)
            legendList.append(eventName)

    plt.legend(legendList)
    plt.title("PS" + PSType + " border")
    plt.xlabel("Time(Hr)")
    plt.ylabel("Score(Pt)")
    plt.grid(True, axis='both', color='gray', alpha=0.7, linestyle='--')

    maxTick = int(max_x) // 24 + 1
    plt.xticks([24 * x for x in range(maxTick)])
    plt.savefig("module_pstcut/border_%s.png" % PSType, dpi = 150, bbox_inches='tight')
