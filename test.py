from parse import parse

def Modules():
	import glob
	import importlib
	mods = []
	modules = glob.glob("bandbot_*.py")
	for module in modules:
		module_name = parse("{}.py",module)
		print(module_name[0])
		mod = importlib.import_module(module_name[0])
		mods.append(mod)
	return mods

mods = Modules()
print(mods)