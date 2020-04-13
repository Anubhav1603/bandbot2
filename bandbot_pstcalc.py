
command=["계산"]

def Com(params, usr_i):
	paramnum = len(params)
	if paramnum == 6:
		if params[2] == "시어터":	#EX) !봇 계산 시어터 영업런 160 300000
			try:
				workdic = {"영업런":True, "라이브런":False}
				isWork = workdic[params[3]]
				return calcTheater(int(params[4]), int(params[5]), isWork)
			except:
				return Err()

		elif params[2] == "투어":	#EX) !봇 계산 투어  영업런 160 300000
			try:
				workdic = {"영업런":True, "라이브런":False}
				isWork = workdic[params[3]]
				return calcTour(int(params[4]), int(params[5]), isWork)
			except:
				return Err()
		else:
			return Err()
	else:
		return Err()

def calcTheater(Stamina, Score, isWork):
	if isWork:
		WorkResult = (Score/((170.0/60.0*0.7)+(170.0/60.0*0.7)*1074.0/360.0)/Stamina*50.0)
		WorkYen = (WorkResult*9800.0/8400.0)
		return "계산 결과입니다.\n필요한 쥬엘은 " + "%.2f"%WorkResult + "개\nG셋충전시 " + "%.2f"%WorkYen +"엔"
	else:
		Result = (Score/(170.0/60.0+170.0/60.0*1074.0/360.0)/Stamina*50.0)
		Yen = (Result*9800.0/8400.0)
		return "계산 결과입니다.\n필요한 쥬엘은 " + "%.2f"%Result + "개\nG셋충전시 " + "%.2f"%Yen +"엔"
	
def calcTour(Stamina, Score, isWork):
	if isWork:
		WorkResult = (Score/281.0/Stamina*1500.0)
		WorkYen = (WorkResult*9800.0/8400.0)
		return "계산 결과입니다.\n필요한 쥬엘은 " + "%.2f"%WorkResult + "개\nG셋충전시 " + "%.2f"%WorkYen +"엔"
	else:
		Result = (Score/326.0/Stamina*1500.0)
		Yen = (Result*9800.0/8400.0)
		return "계산 결과입니다.\n필요한 쥬엘은 " + "%.2f"%Result + "개\nG셋충전시 " + "%.2f"%Yen +"엔"

def Err():
	responseChat =  """\
	pstcalc.py: 잘못된 계산기 명령입니다.
	사용법 : !계산 [시어터|투어] [영업런|라이브런] [원기통] [목표점수]
	"""
	return responseChat