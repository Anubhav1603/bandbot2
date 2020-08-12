import csv
import glob
import API.fsync as fsync

command = ["미라"]

DBENDPOINT = "https://si.ster.email/download/miraji"
DBDIR = "module_miraji/images"

CSV_CACHE = []

def GetDB():
    try:
        fsync.WebStorage(DBENDPOINT, DBDIR)
    except:
        return False
    return True

def UpdateCSV():
    global CSV_CACHE
    with open("module_miraji/images/miraji_dict.csv", "r", encoding = "utf-8") as f:
        rdr = csv.reader(f)
        CSV_CACHE = list(rdr)

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

def Com(params, usr_i):
    global CSV_CACHE
    paramNum = len(params)

    if len(CSV_CACHE) == 0:
        if not GetDB():
            return "miraji.py: DB 동기화 실패"
        if not UpdateCSV():
            return "miraji.py: CSV 무결성검사 실패"
        if not CheckCSV():
            return "miraji.py: 이미지 무결성검사 실패"

    if paramNum >= 3:
        if "갱신" in params:
            if not GetDB():
                return "miraji.py: DB 동기화 실패"
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
