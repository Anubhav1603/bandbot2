import random

from extensions import ModuleBase, single_chat

class Module(ModuleBase):
	commands = ["개그"]
	def __init__(self):
		self.cache = []
	
	@single_chat
	def run(self, params, usr_i):
		if len(self.cache) == 0:
			f = open("module_gag/gag_list.txt", "r", encoding="utf-8")
			self.cache = f.readlines().copy()
			f.close()
		return random.choice(self.cache)[:-1]