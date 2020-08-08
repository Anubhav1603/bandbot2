# API
나 편하려고 만든것들

## API.telegram
```
from API.telegram import Bot

token = "봇 토큰"
chat_id = "채팅 id"

bot = Bot(token, chat_id)

bot.sendMessage("Hello, World!")

try:
    newChat = bot.getUpdates()
    print(newChat)
except:
    print("최근 채팅이 없습니다.")

```

## API.timeout
```
from API.timeout import TimeoutDeco

def loop(num):
    return num**num**num

timeout_func = TimeoutDeco(5, "TIMEOUT", loop)

print(timeout_func(2))          => 16
print(timeout_func(29910))      => TIMEOUT
```

## API.time
```
from API.time import *

now = TimeISO()
later = "2020-08-07T03:00:00+09:00"

print(now)
# 2020-08-07T00:42:42+09:00

print(StrfTimeISO(now))
# 8월 7일 00:42

print(DeltaTimeISO(start, end))
# 2.2883333333333336
# Unit: Hour
