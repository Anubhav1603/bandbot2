```
!봇 [명령어] [인자1] [인자2]..
```

# 모듈


봇이 처음 시작할때 module_xxxx 형태의 폴더들을 인식하고, 각 폴더의 xxxx.py 파일을 동적 임포트한 뒤에 Module 클래스의 인스턴스를 생성후 저장한다.

형태의 채팅을 인식시 [명령어]에 해당하는 문자열을 갖고있는 인스턴스의 run() 메소드를 호출하고 리턴.

# 예제
* 단일채팅 응답 모듈
  * [example.py](example.py) 파일 참조
* Delay 및 다중채팅 응답 모듈
  * [example1.py](example1.py) 파일 참조
* Image 및 다중명령어 모듈
  * [example2.py](example2.py) 파일 참조

## 인자
* params: 인식한 채팅을 공백으로 split한 리스트
* usr_i: 호출한 유저 닉네임

## 인터페이스 상세
* [band.py](https://github.com/kohs100/band.py#return-value) 참조.

## 테스트 방법
```
python testmodule.py
```