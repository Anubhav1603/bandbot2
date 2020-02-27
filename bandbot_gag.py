import random
import codecs

command = ["개그"]

def Com(params, usr_i):
	f = codecs.open("gag.txt",'r', encoding='utf-8')
	lines = f.readlines()
	gagnum = random.randrange(0,360)
	return lines[gagnum]
