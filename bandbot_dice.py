import random

command = ["주사위"]

def Com(params, usr_i):
	paramnum = len(params)
	if paramnum == 4:
		try:
			dicenum = int(params[2])
			dicesize = int(params[3])
		except:
			response = "dice.py: 잘못된 주사위 명령입니다.\n"
			response += "사용법 : !봇 주사위 [주사위갯수] [최대값]"
			return response
		
		if dicenum >= 1 and dicenum <= 10:
			if dicesize >= 1 and dicenum <= 99999999:
				response = []
				for i in range(dicenum):
					diceval = random.randint(1, dicesize)
					response.append("[주사위%d] %d" % (i + 1, diceval))
				return "\n".join(response)
			else:
				return "dice.py: 잘못된 주사위 크기(최대 8자리)"
		else:
			return "dice.py: 잘못된 주사위 갯수(최대 10개)"

	else:
		response = "dice.py: 잘못된 주사위 명령입니다.\n"
		response += "사용법 : !봇 주사위 [주사위갯수] [최대값]"
		return response