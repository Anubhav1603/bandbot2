import pwnlib.util.safeeval

command = ["연산"]

class avg:
    def __add__(self, lst_input):
        try:
            return sum(lst_input) / len(lst_input)
        except:
            raise ValueError


def Com(params, usr_i):
    paramNum = len(params)

    if paramNum > 2:
        print(" ".join(params[2:]))
        try:
            sick = " ".join(params[2:])
            return str(pwnlib.util.safeeval.values(sick, {'avg' : avg()}))

        except Exception as e:
            print(e)
            return "calc.py: 잘못된 식"
            
    else:
        return "calc.py: 사용법\n"\
               "!봇 연산 [계산식]"