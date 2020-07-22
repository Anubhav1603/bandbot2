import random, codecs

command = ["개그"]

def Com(params, usr_i):
	f = codecs.open("bandbot_gag_list.txt", 'r', encoding = 'utf-8')
	lines = f.readlines()
	gagnum = random.randrange(0,363)
	return lines[gagnum]
