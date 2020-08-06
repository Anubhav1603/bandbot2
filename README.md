# Bandbot
Python bandbot

# Dependencies
## 파이썬 버전
* 파이썬 버전이 반드시 3.7 이상이어야함 (3.6 이하에는 datetime.datetime.fromisoformat()이 없음)

## 구글 크롬
* https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

## chromedriver
* https://chromedriver.chromium.org/
* PATH를 통해 실행할 수 있어야함(/usr/bin/ 등)

## Noto Sans CJK JP
* https://www.google.co.kr/get/noto/help/cjk/
```
$ sudo apt-get install fonts-noto-cjk
```

# 사용법
```
python start.py
python start.py --test
```