import csv
import glob
import requests

URL = "https://si.ster.email/download/miraji/"

command = ["미라"]

CSV_CACHE = []

def UpdateCSV():
    global CSV_CACHE
    f = open("module_miraji/miraji_dict.csv", "r", encoding = "utf-8")
    rdr = csv.reader(f)
    CSV_CACHE = list(rdr)
    f.close()
    for elem in CSV_CACHE:
        if len(elem) != 2:
            return False
    return True

def CheckCSV():
    file_list = glob.glob("module_miraji/images/*.*")
    
    for i, elem in enumerate(file_list):
        file_list[i] = elem.replace("\\", "/")
        file_list[i] = file_list[i][14:]

    for elem in CSV_CACHE:
        if not elem[1] in file_list:
            return False
    return True

def RetrieveCSV():
    global CSV_CACHE

    res = requests.get(URL + "miraji_dict.csv")
    f = open("module_miraji/miraji_dict.csv", mode = "w", encoding = "utf-8")
    f.write(res.text)
    f.close()

    f = open("module_miraji/miraji_dict.csv", mode = "r", encoding = "utf-8")
    rdr = csv.reader(f)
    CSV_CACHE = list(rdr)
    f.close()

    file_list = glob.glob("module_miraji/images/*.*")
    for i, elem in enumerate(file_list):
        file_list[i] = elem.replace("\\", "/")
        file_list[i] = file_list[i][14:]
    
    for elem in CSV_CACHE:
        if not elem[1] in file_list:
            res = requests.get(URL + elem[1])
            f = open("module_miraji/" + elem[1], mode = "wb")
            f.write(res.content)
    
def Com(params, usr_i):
    global CSV_CACHE
    paramNum = len(params)

    if len(CSV_CACHE) == 0:
        if not UpdateCSV():
            return "miraji.py: CSV 무결성검사 실패"
        if not CheckCSV():
            return "miraji.py: 이미지 무결성검사 실패"

    if paramNum >= 3:
        if "갱신" in params:
            if not UpdateCSV():
                return "miraji.py: CSV 무결성검사 실패"
            if not CheckCSV():
                return "miraji.py: 이미지 무결성검사 실패"
            return "miraji.py: 미라지 갱신 성공"

        req_miraji = params[2:]
        invalid_miraji = []
        response = []

        for miraji in req_miraji:
            if len(miraji) == 0:
                continue
            is_invalid = True
            for elem in CSV_CACHE:
                if miraji == elem[0]:
                    is_invalid = False
                    response.append("REQUEST_IMAGE_module_miraji/" + elem[1])
                    break
            if is_invalid:
                invalid_miraji.append(miraji)

        if len(invalid_miraji) != 0:
            return "miraji.py: 미라지가 없습니다: " + " ".join(invalid_miraji)

        return "\n".join(response)
    else:
        return "miraji.py: 사용법\n!봇 미라 [미라지명]..."
