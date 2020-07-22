import csv, platform

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

    if paramNum >= 3:
        if params[2] == "갱신":
            f = open("bandbot_miraji_dict.csv", encoding = "utf-8")
            rdr = csv.reader(f)
            CSV_CACHE = list(rdr)
            f.close()
            return "miraji.py: 미라지 갱신완료"
        
        req_miraji = params[2:]
        invalid_miraji = []

        for miraji in req_miraji:
            is_invalid = True
            for elem in CSV_CACHE:
                if miraji == elem[0]:
                    is_invalid = False
                    break
            if is_invalid:
                invalid_miraji.append(miraji)
        
        if len(invalid_miraji) != 0:
            return "miraji.py: 미라지가 없습니다: " + " ".join(invalid_miraji)
        
        response = []
        for miraji in req_miraji:
            for elem in CSV_CACHE:
                if miraji == elem[0]:
                    if platform.system() == "Windows":
                        response.append("REQUEST_IMAGE_images/" + elem[1])
                    else:
                        response.append("REQUEST_IMAGE_images\\" + elem[1])
        
        return "\n".join(response)
    else:
        return "miraji.py: 사용법\n"\
               "!봇 미라 [미라지명]"