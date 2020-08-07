command=["계산"]

def LevelToStamina(lv):
	if lv >= 700:
		return 240
	elif lv >= 586:
		return 221 + (lv-586) / 6
	elif lv >= 426:
		return 189 + (lv-426) / 5
	elif lv >= 150:
		return 120 + (lv-150) / 4
	elif lv >= 60:
		return 60 + (lv-60) / 3
	elif lv >= 2:
		return 61 + (lv-2) / 2
	

def Com(params, usr_i):
	paramnum = len(params)
	guide = "pstcalc.py: 사용법\n\
!봇 계산 [시어터|투어|튠] [영업런|라이브런] [레벨] [목표점수]"

	if paramnum == 6:
		try:
			workdic = {"영업런":True, "라이브런":False}
			isWork = workdic[params[3]]
			stamina = LevelToStamina(int(params[4]))
			score = int(params[5])
			
			if params[2] == "시어터":	#EX) !봇 계산 시어터 영업런 160 300000
				return calcTheater(stamina, score, isWork)

			elif params[2] == "투어":	#EX) !봇 계산 투어 영업런 160 300000
				return calcTour(stamina, score, isWork)

			elif params[2] == "튠":
				return calcTune(stamina, score, isWork)
		except:
			return guide
	else:
		return guide

def calcTheater(genki, score, isWork):
	if isWork:
		Result = score/((170.0/60.0*0.7)+(170.0/60.0*0.7)*1074.0/360.0)/genki*50.0
		Yen = Result*9800.0/8400.0
	else:
		Result = (score/(170.0/60.0+170.0/60.0*1074.0/360.0)/genki*50.0)
		Yen = (Result*9800.0/8400.0)
	return "계산 결과입니다.\n필요주얼: %.2f\nG셋충전시: %.2f엔" % (Result, Yen)
	
def calcTour(genki, score, isWork):
	if isWork:
		Result = score/281.0/genki*1500.0
		Yen = Result*9800.0/8400.0
	else:
		Result = score/326.0/genki*1500.0
		Yen = Result*9800.0/8400.0
	return "계산 결과입니다.\n필요주얼: %.2f\nG셋충전시: %.2f엔" % (Result, Yen)

def calcTune(genki, score, isWork):
	jaehwa = score * 140 / 537
	if isWork:
		genkiUsage = jaehwa * 300 / 525
	else:
		genkiUsage = jaehwa * 30 / 75

	jewelUsage = genkiUsage * 50 / genki
	moneyUsage = jewelUsage * 9800 / 8400
	return "계산 결과입니다.\n필요주얼: %.2f\nG셋충전시: %.2f엔" % (jewelUsage, moneyUsage)