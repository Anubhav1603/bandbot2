import datetime

def TimeISO():
    dtz = datetime.timedelta(hours=9)
    tnow = datetime.datetime.now(tz=dtz)
    tnow = tnow.replace(microsecond=0)
    return tnow.isoformat()

def StrfTimeISO(dateinfo):
    year = dateinfo[0:4]
    month = dateinfo[5:7]
    day = dateinfo[8:10]
    hour = dateinfo[11:13]
    minute = dateinfo[14:16]
    return month+'월 '+day+'일 '+hour+":"+minute