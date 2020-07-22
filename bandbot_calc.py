import pwnlib.util.safeeval
from multiprocessing import Process, Queue

command = ["연산"]

def SafeEvaluation(sick, q): 
    class avg:
        def __add__(self, lst_input):
            try:
                return sum(lst_input) / len(lst_input)
            except:
                raise ValueError

    try:
        result = pwnlib.util.safeeval.values(sick, {'avg' : avg()})
        result = str(result)

    except Exception as e:
        print(e)
        q.put("잘못된 식")
        return
    else:
        q.put(result)
        return

def Com(params, usr_i):
    paramNum = len(params)

    if paramNum > 2:
        sick = " ".join(params[2:])
        print(sick)

        q = Queue()
        p = Process(target = SafeEvaluation, args = (sick, q))
        p.start()

        p.join(5)

        if p.is_alive():
            p.terminate()
            p.join()

        if q.empty():
            return "calc.py: 너무 오래걸립니다."
        else:
            return q.get()
    else:
        return "calc.py: 사용법\n"\
               "!봇 연산 [계산식]"