from multiprocessing import Process, Queue

def IFunction(OFunction, q, args, kwargs):
    ret = OFunction(*args, **kwargs)
    q.put(ret)

def TimeoutDeco(timeout, timeoutRet, OFunction):
    def WrapperFunction(*args, **kwargs):
        q = Queue()
        p = Process(target = IFunction, args = (OFunction, q, args, kwargs))
        p.start()

        p.join(timeout)

        if p.is_alive():
            p.terminate()
            p.join()
            return timeoutRet

        try:
            return q.get_nowait()
        except:
            return timeoutRet
    
    return WrapperFunction