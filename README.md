# Bandbot
Python bandbot2

# Dependencies (For native run)
## Python
* Python version must be higher then 3.7
```
$ sudo apt-get install python3.7 python3.7-dev python3-pip
$ python3.7 -m pip install -r requirements.txt
```
```
$ sudo apt-get install python3.8 python3.8-dev python3-pip
$ python3.8 -m pip install -r requirements.txt
```

## Google Chrome
* https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo dpkg -i google-chrome*.deb
```

## chromedriver
* https://chromedriver.chromium.org/

## BAND Account
* Should be able to login with phone number

# 사용법
* [Docker image(Recommended)](docker-bandbot)

* Native run
```
$ python start.py
$ python start.py --test
```

