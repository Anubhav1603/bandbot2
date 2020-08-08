import pwnlib.util.safeeval
from API.timeout import TimeoutDeco

command = ["연산"]

def SafeEvaluation(sick):
    # AVG + [2,3,4] == 3
    class AVG:
        def __add__(self, lst_input):
            return sum(lst_input) / len(lst_input)
    
    class LTS:
        def __add__(self, lv):
            if lv >= 700:
                return 240
            elif lv >= 586:
                return 221 + (lv-586) / 6
            elif lv >= 426:
                return 189 + (lv-426) / 5
            elif lv >= 150:
                return 120 + (lv-150) / 4
            elif lv >= 60:
                return 60 + (lv-60) / 3
            elif lv >= 2:
                return 61 + (lv-2) / 2

    cmdDict = {"AVG": AVG(), "LTS":LTS()}

    try:
        result = pwnlib.util.safeeval.values(sick, cmdDict)
        result = str(result)

    except Exception as e:
        print(e)
        return "calc.py: 잘못된 식"
    else:
        return result


def Com(params, usr_i):
    paramNum = len(params)

    if paramNum > 2:
        sick = " ".join(params[2:])
        print(sick)

        decorated = TimeoutDeco(5, "calc.py: 너무 오래걸립니다.", SafeEvaluation)

        return decorated(sick)
    else:
        return "calc.py: 사용법\n"\
               "!봇 연산 [계산식]"
