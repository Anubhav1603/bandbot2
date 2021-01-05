from extensions import ModuleBase, single_chat

class Module(ModuleBase):
	commands = ["역계산"]

	@single_chat
	def run(self, params, usr_i):
		paramnum = len(params)
		guide = "pstcalc_r.py: 사용법\n!봇 역계산 [시어터|투어|튠] [영업런|라이브런] [레벨] [주얼]"

		if paramnum == 6:
			try:
				workdic = {"영업런": True, "라이브런": False}
				isWork = workdic[params[3]]
				stamina = LevelToStamina(int(params[4]))
				score = int(params[5])
				
				if params[2] == "시어터":
					return calcTheater(stamina, score, isWork)

				elif params[2] == "투어":
					return calcTour(stamina, score, isWork)

				elif params[2] == "튠":
					return calcTune(stamina, score, isWork)
			except:
				return guide
		else:
			return guide

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

def calcTheater(genki, jewel, isWork):
	stamina = (jewel / 50) * genki
	score = stamina * 11.28611

	if isWork:
		score *= 0.7

	return "획득pt: %.1f" % score
	
def calcTour(genki, jewel, isWork):
	'''
	라이브런
	스테 300 -> MM 10판 + 이벤곡 3판(5배수)
	MM 10판: 푸시코스 기준 1400pt
	이벤곡 5배수 3판: 144 * 5 * 3 = 2160pt
	스테 300당 3560pt.
	영업런
	스테 300 -> MM영업 10판 + 이벤곡 3판(5배수)
	MM영업 10판: 480pt ~ 820pt -> 600pt 가정.
	이벤곡 5배수 3판: 144 * 5 * 3 = 2160pt
	스테 300당 2760pt.
	'''
	stamina = (jewel / 50) * genki
	if isWork:
		score = stamina / 300 * 2760
	else:
		score = stamina / 300 * 3560

	return "획득pt: %.1f" % score

def calcTune(genki, jewel, isWork):
	'''
	라이브런
	스테 300 -> MM 10판 + 재화 750개
	MM 10판 -> 750pt
	재화 750개 -> x4.2: 3024pt
	스테 300당 3774pt.
	영업런
	스테 300 -> 10배율 1판 + 재화 525개
	10배율 1판 -> 525pt
	재화 525개 -> x4.2: 2205pt
	스테 300당 2730pt.
	'''
	stamina = (jewel / 50) * genki
	if isWork:
		score = stamina / 300 * 2730
	else:
		score = stamina / 300 * 3774

	return "획득pt: %.1f" % score