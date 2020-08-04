import random

command = ["개그"]

GAG_CACHE = []

def Com(params, usr_i):
	global GAG_CACHE
	if len(GAG_CACHE) == 0:
		f = open("module_gag/gag_list.txt", "r", encoding = "utf-8")
		GAG_CACHE = f.readlines().copy()
		f.close()
	gagnum = random.randrange(len(GAG_CACHE))
	return GAG_CACHE[gagnum]
