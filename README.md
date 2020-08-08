# Bandbot
Python bandbot2

# Dependencies
## 파이썬 버전
* 파이썬 버전이 반드시 3.7 이상이어야함 (3.6 이하에는 datetime.datetime.fromisoformat()이 없음)
```
$ sudo apt-get install python3.7 python3.7-dev python3-pip
$ python3.7 -m pip install -r requirements.txt
```

## 구글 크롬
* https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo dpkg -i google-chrome*.deb
```

## chromedriver
* https://chromedriver.chromium.org/
* PATH를 통해 실행할 수 있어야함(/usr/bin/ 등)

## Noto Sans CJK JP
* https://www.google.co.kr/get/noto/help/cjk/
```
$ sudo apt-get install fonts-noto-cjk
```

## BAND 계정
* 전화번호를 통해 로그인하는 기능밖에 구현되어있지 않음

# 사용법
```
$ python start.py
$ python start.py --test
```