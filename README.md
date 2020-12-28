# Bandbot

## 개요

[band.py](https://github.com/kohs100/band.py) 모듈을 사용해 구현된 워너비어스타 밴드 챗봇
  
## 명령어

### 밀리이벤 관련

```text
!봇 밀리이벤
!봇 밀리이벤컷
!봇 밀리역대컷 [시어터|투어]
!봇 밀리예측컷
!봇 계산 [시어터|투어|튠] [영업런|라이브런] [레벨] [목표득점]
```

* 밀리이벤
  * 현재 진행중인 이벤트 정보
* 밀리이벤컷
  * 현재 진행중인 이벤트 컷
* 밀리역대컷
  * 현재 선택한 유형의 이벤트가 진행중일 경우, 최근 10개 동일유형 이벤트의 2500위 보더 상승 추이를 현재 이벤트 진행도까지 그래프로 보여줌. (최종보더 순으로 정렬됨)
  * 현재 선택한 유형의 이벤트가 진행중이 아닐 경우, 최근 10개 해당유형 이벤트의 2500위 보더 상승 추이를 최종보더 순으로 정렬하여 그래프로 보여줌.
* 밀리예측컷
  * [@Alneys_al](https://twitter.com/alneys_al) 에 올라오는 예측컷 정보를 크롤링해서 보여줌.
* 계산
  * 목표득점만큼의 포인트를 얻는데 필요한 주얼 갯수와 값을 계산해줌.
  
### 그외

```text
!봇 연산 [식]
!봇 개그
!봇 주사위 [주사위갯수] [주사위크기]
!봇 미라지 [미라지이름]
!봇 마크서버 [서버주소]
```

* 연산
  * 파이썬 식을 연산한 결과를 반환
* 미라지
  * [미라지 목록](http://si.ster.email/dl/miraji/images/miraji_dict.csv)
* 마크서버
  * 마크서버 상태체크

## 모듈 기여

[모듈 개발 가이드](_module_example/readme.md)

## 이벤트 달력

<iframe src="https://calendar.google.com/calendar/embed?height=400&amp;wkst=1&amp;bgcolor=%23ffffff&amp;ctz=Asia%2FSeoul&amp;src=ajgxcm90NTZrMDdxZHIwYzlvaDhyOTNyaWdAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&amp;color=%23a2845e&amp;showTitle=1&amp;title=MLTD%20Events&amp;showPrint=0&amp;showNav=1&amp;showCalendars=0&amp;showDate=1&amp;showTabs=0&amp;showTz=1" style="border:solid 1px #777" width="600" height="400" frameborder="0" scrolling="no"></iframe>