import csv

command = ["미라"]

CSV_CACHE = []

def Com(params, usr_i):
    global CSV_CACHE
    paramNum = len(params)

    if len(CSV_CACHE) == 0:
        f = open("bandbot_miraji_dict.csv", encoding = "utf-8")
        rdr = csv.reader(f)
        CSV_CACHE = list(rdr)
        f.close()

    if paramNum == 3:
        if params[2] == "갱신":
            f = open("bandbot_miraji_dict.csv", encoding = "utf-8")
            rdr = csv.reader(f)
            CSV_CACHE = list(rdr)
            f.close()
            return "miraji.py: 미라지 갱신완료"
            
        for elem in CSV_CACHE:
            if params[2] == elem[0]:
                return "REQUEST_IMAGE_" + elem[1]
        return "miraji.py: 미라지가 없습니다."
    else:
        return "miraji.py: 사용법\n"\
               "!봇 미라 [미라지명]"