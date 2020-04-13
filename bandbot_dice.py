import random
import parse

command = ["주사위"]

def Com(params, usr_i):
	paramnum = len(params)
	if paramnum == 3:
		try:
			res = parse.parse("{}D{}", params[2])
			if int(res[0]) >= 11 or int(res[1]) > 99999999:
				raise ValueError
			return Roll(int(res[1]), int(res[0]))
		except ValueError:
			return Err(True)
		except:
			return Err(False)
	else:
		return Err(False)

def Roll(dicemax, dicenum):
	responseChat = ""

	sum = 0
	for i in range(dicenum):
		dice = random.randrange(1,dicemax + 1)
		sum += dice
		responseChat += "[주사위]" + str(i + 1) + " 값: " + str(dice) + "\n"
	responseChat += "[주사위]합계: " + str(sum)
	
	return responseChat

def Err(isToomany):
	responseChat = "dice.py: "
	if isToomany:
		responseChat += "너무 많은 주사위입니다."
	else:
		responseChat += """\
		잘못된 주사위 명령입니다.
		사용법 : !봇 주사위 (주사위갯수)D(최대값)
		"""

	return responseChat