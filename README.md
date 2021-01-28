# Bandbot

## 개요

[band.py](https://github.com/kohs100/band.py) 모듈을 사용해 구현된 워너비어스타 밴드 챗봇
  
## 명령어

### 밀리이벤 관련

```text
!봇 밀리이벤
!봇 밀리이벤컷
!봇 밀리역대컷 [시어터|투어] [100|2500]
!봇 밀리예측컷
!봇 계산 [시어터|투어|튠] [영업런|라이브런] [레벨] [목표득점]
!봇 역계산 [시어터|투어|튠] [영업런|라이브런] [레벨] [가용주얼]
```

* 밀리이벤
  * 현재 진행중인 이벤트 정보
* 밀리이벤컷
  * 현재 진행중인 이벤트 컷
* 밀리역대컷
  * 현재 선택한 유형의 이벤트가 진행중일 경우, 최근 10개 동일유형 이벤트의 100위 또는 2500위 보더 상승 추이를 현재 이벤트 진행도까지 그래프로 보여줌. (최종보더 순으로 정렬됨)
  * 현재 선택한 유형의 이벤트가 진행중이 아닐 경우, 최근 10개 해당유형 이벤트의 100위 또는 2500위 보더 상승 추이를 최종보더 순으로 정렬하여 그래프로 보여줌.
* 밀리예측컷
  * [@Alneys_al](https://twitter.com/alneys_al) 에 올라오는 예측컷 정보를 크롤링해서 보여줌. (보통 후반전 시작 이후에 집계됨)
* 계산
  * 목표득점만큼의 포인트를 얻는데 필요한 주얼 갯수와 값을 계산해줌.
* 역계산
  * 가용주얼을 사용해서 얻을 수 있는 포인트를 계산해줌.
  
### 그외

```text
!봇 연산 [식]
!봇 개그
!봇 주사위 [주사위갯수] [주사위크기]
!봇 미라 [미라지이름]
!봇 마크서버 [서버주소]
```

* 연산
  * 파이썬 식을 연산한 결과를 반환
* 미라
  * [미라지 목록](https://bot.ster.email/miraji.html)
  * alias: 미라지, 미라티콘으로도 사용 가능
* 마크서버
  * 마크서버 상태체크

### 리디렉션 기능
```text
!봇 [명령어] [인자1] [인자2] > [갠챗|텔레그램|...]
```
* 갠챗
  * 개인채팅으로 명령어 실행 결과를 보내줌
* TODO: 텔레그램등 기타 출력 스트림 추가 예정

### 최근 변경
* [kohs100/bandbot2:11](https://hub.docker.com/r/kohs100/bandbot2)
  * Performance logging을 통한 ws통신 후킹으로 채팅인식방식 변경
  * 닉네임 변경과 관계 없이 유저구분 가능
  
* [kohs100/bandbot2:12](https://hub.docker.com/r/kohs100/bandbot2)
  * 개인채팅 리디렉션 기능 추가
  * 역계산 모듈 추가
  * 연산모듈 오류 수정

* [kohs100/bandbot2:13](https://hub.docker.com/r/kohs100/bandbot2)
  * 밀리역대컷 모듈 100위 그래프 추가
  * impllicit wait 모두 제거

* [kohs100/bandbot2:14](https://hub.docker.com/r/kohs100/bandbot2)
  * 밀리이벤컷 100위/2500위 보더만 표시하도록 변경

### 알려진 이슈


## 모듈 기여

[모듈 개발 가이드](https://github.com/kohs100/bandbot2/tree/master/_module_example)