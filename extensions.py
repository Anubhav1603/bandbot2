import glob
import importlib

class extnMods():
    def __init__(self):
        self.mods = []

        modules = glob.glob("bandbotMod_*.py")
        for module in modules:
            module_name = module[:-3]
            mod = importlib.import_module(module_name)
            self.mods.append(mod.recvChat)

    def sendChat(self, str_i, usr_i):
        for mod in self.mods:
            return mod(str_i, usr_i)


class extnModules():
    emptyCall = 1
    wrongCommand = 2

    def __init__(self):
        self.mods = []
        self.commands = []

        modules = glob.glob("bandbot_*.py")
        for module in modules:
            module_name = module[:-3]
            mod = importlib.import_module(module_name)
            self.mods.append(mod)
            self.commands.append(mod.command)

    def find_and_execute(self, command_i, params, usr_i):
        for i, command in enumerate(self.commands):
            if command_i in command:
                return self.mods[i].Com(params, usr_i)

        return extnModules.wrongCommand

    def strfModules(self):
        responseChat = ""
        for command in self.commands:
            for com in command:
                responseChat += com + ", "
        return responseChat[:-2]

    def commandSel(self, params, usr_i):
        if len(params) == 1:
            return extnModules.emptyCall
        else:
            return self.find_and_execute(params[1], params, usr_i)