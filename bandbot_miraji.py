import csv, glob

command = ["미라"]

CSV_CACHE = []

def UpdateCSV():
    global CSV_CACHE
    f = open("bandbot_miraji_dict.csv", encoding = "utf-8")
    rdr = csv.reader(f)
    CSV_CACHE = list(rdr)
    f.close()
    for elem in CSV_CACHE:
        if len(elem) != 2:
            return False
    return True

def CheckCSV():
    file_list = glob.glob("images/*.*")

    for i, elem in enumerate(file_list):
        file_list[i] = elem.replace("\\", "/")
    
    for elem in CSV_CACHE:
        if not elem[1] in file_list:
            return False
    return True

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
            is_invalid = True
            for elem in CSV_CACHE:
                if miraji == elem[0]:
                    is_invalid = False
                    response.append("REQUEST_IMAGE_" + elem[1])
                    break
            if is_invalid:
                invalid_miraji.append(miraji)
        
        if len(invalid_miraji) != 0:
            return "miraji.py: 미라지가 없습니다: " + " ".join(invalid_miraji)
        
        return "\n".join(response)
    else:
        return "miraji.py: 사용법\n"\
               "!봇 미라 [미라지명]"