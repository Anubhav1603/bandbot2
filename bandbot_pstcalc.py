from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import param

def Calc(msgWrite, paramnum, param):
	if paramnum == 5:
		if params[1] == "시어터":	#EX) !계산 시어터 영업런 160 300000
			try:
				workdic = {"영업런":True, "라이브런":False}
				isWork = workdic[params[2]]
				Theater(msgWrite, int(params[3]), int(params[4]), isWork)
			except:
				Err(msgWrite)

		elif params[1] == "투어":	#EX) !계산 시어터 영업런 160 300000
			try:
				workdic = {"영업런":True, "라이브런":False}
				isWork = workdic[params[2]]
				Tour(msgWrite, int(params[3]), int(params[4]), isWork)
			except:
				Err(msgWrite)
		else:
			Err(msgWrite)
	else:
		Err(msgWrite)

def Theater(msgWrite, Stamina, Score, isWork):
	if isWork:
		WorkResult = (Score/((170.0/60.0*0.7)+(170.0/60.0*0.7)*1074.0/360.0)/Stamina*50.0)
		WorkYen = (WorkResult*9800.0/8400.0)
		msgWrite.send_keys("계산 결과입니다..")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("필요한 쥬엘은 " + "%.2f"%WorkResult + "개")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("G셋충전시 " + "%.2f"%WorkYen +"엔")
		msgWrite.send_keys(Keys.ENTER)
	else:
		Result = (Score/(170.0/60.0+170.0/60.0*1074.0/360.0)/Stamina*50.0)
		Yen = (Result*9800.0/8400.0)
		msgWrite.send_keys("계산 결과입니다..")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("필요한 쥬엘은 " + "%.2f"%Result + "개")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("G셋충전시 " + "%.2f"%Yen +"엔")
		msgWrite.send_keys(Keys.ENTER)
	
def Tour(msgWrite, Stamina, Score, isWork):
	if isWork:
		WorkResult = (Score/281.0/Stamina*1500.0)
		WorkYen = (WorkResult*9800.0/8400.0)
		msgWrite.send_keys("계산 결과입니다..")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("필요한 쥬엘은 " + "%.2f"%WorkResult + "개")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("G셋충전시 " + "%.2f"%WorkYen +"엔")
		msgWrite.send_keys(Keys.ENTER)
	else:
		Result = (Score/326.0/Stamina*1500.0)
		Yen = (Result*9800.0/8400.0)
		msgWrite.send_keys("계산 결과입니다..")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("필요한 쥬엘은 " + "%.2f"%Result + "개")
		msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
		msgWrite.send_keys("G셋충전시 " + "%.2f"%Yen +"엔")
		msgWrite.send_keys(Keys.ENTER)

def Err(msgWrite):
	msgWrite.send_keys("pstcalc.py:")
	msgWrite.send_keys("잘못된 계산기 명령입니다.")
	msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
	msgWrite.send_keys("사용법 : ")
	msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
	msgWrite.send_keys("!계산 [시어터|투어] [영업런|라이브런] [원기통] [목표점수]")
	msgWrite.send_keys(Keys.ENTER)