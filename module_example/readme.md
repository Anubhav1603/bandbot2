# 모듈과 모드
## 모듈
봇이 시작할때 bandbot_xxxx.py 형태의 파일들을 모듈로써 인식
각 모듈들의 command 리스트들을 모두 로드하고
```
!봇 [명령어] [인자1] [인자2]..
```
형태의 채팅을 인식시 [명령어]에 해당하는 문자열을 갖고있는 모듈의 Com() 함수 호출

```
def Com(params, usr_i):
    return "응답 to " + usr_i
```
* params
인식한 채팅을 split(" ") 한 리스트

* usr_i
호출한 유저 닉네임

## 모드
채팅창에 올라오는 모든 채팅에 대해 호출되는 모듈

# 모듈 테스트 방법
모듈과 필요 파일들을 start.py와 같은 디렉토리에 놓고
```
python start.py --simple-test
```