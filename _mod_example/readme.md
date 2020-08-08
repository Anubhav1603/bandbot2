# 모드
* 봇이 시작할때 mod_xxxx 형태의 폴더들을 모드로써 인식하고, 각 모듈의 xxxx.py 파일을 동적 임포트한다.
* 모든 채팅을 모드로 전달하며, 모드는 채팅형태의 응답이 불가능

```
import csv
from API.time import TimeISO()

def recvChat(usr_i, str_i):
    with f as open("chatlog.csv", "w", encoding="utf-8", newline=""):
        fc = csv.writer(f)
        fc.writerow([TimeISO(), usr_i, str_i])
```

## 인자
* usr_i: 유저 닉네임
* str_i: 채팅 내용

## 테스트 방법
모드와 필요 파일들을 start.py와 같은 디렉토리에 놓고
```
python start.py --test
```