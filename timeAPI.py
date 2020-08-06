import datetime

def TimeISO():
    dt = datetime.timedelta(hours=9)
    dtz = datetime.timezone(dt)
    tnow = datetime.datetime.now(tz=dtz)
    tnow = tnow.replace(microsecond=0)
    return tnow.isoformat()

def StrfTimeISO(dateISO):
    # year = dateISO[0:4]
    month = dateISO[5:7]
    day = dateISO[8:10]
    hour = dateISO[11:13]
    minute = dateISO[14:16]
    return month+'월 '+day+'일 '+hour+":"+minute

def DeltaTimeISO(start, end):
    start = datetime.datetime.fromisoformat(start)
    end = datetime.datetime.fromisoformat(end)
    delta = end - start
    return delta.total_seconds() / 3600