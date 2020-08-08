# 모듈
봇이 시작할때 module_xxxx 형태의 폴더들을 모듈로써 인식하고, 각 모듈의 xxxx.py 파일을 동적 임포트한다.
```
!봇 [명령어] [인자1] [인자2]..
```
형태의 채팅을 인식시 [명령어]에 해당하는 문자열을 갖고있는 모듈의 Com() 함수를 호출하고 응답 prefix에 리턴값을 붙여서 출력.

```
command = ["예시"]

def Com(params, usr_i):
    return "응답 to " + usr_i
```

```
ㅎㅅㅋ: !봇 예시
응답:   [밴드봇] ㅎㅅㅋ         # 응답 prefix
        응답 to ㅎㅅㅋ
```

## 인자
* params: 인식한 채팅을 공백으로 split한 리스트
* usr_i: 호출한 유저 닉네임

## 이미지 전송
```
command = ["이미지"]

def Com(params, usr_i):
    return "REQUEST_IMAGE_filepath.jpg"
```
[example.py](https://github.com/kohs100/bandbot2/blob/master/_module_example/example.py "ref") 파일 참조

## 테스트 방법
모듈과 필요 파일들을 start.py와 같은 디렉토리에 놓고
```
python start.py --test
```