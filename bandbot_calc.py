import pwnlib.util.safeeval
from timeoutAPI import TimeoutDeco

command = ["연산"]

def SafeEvaluation(sick):
    # avg + [2,3,4] == 3
    class avg:
        def __add__(self, lst_input):
            return sum(lst_input) / len(lst_input)

    try:
        result = pwnlib.util.safeeval.values(sick, {'avg': avg()})
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
