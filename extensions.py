import importlib, glob
from timeoutAPI import TimeoutDeco

class extnMods():
    def __init__(self):
        self.mods = []

        modules = glob.glob("mod_*")
        for module in modules:
            module_name = module + "." + module[4:]
            mod = importlib.import_module(module_name)
            self.mods.append(mod.recvChat)

    def sendChat(self, str_i, usr_i):
        retVal = []
        for mod in self.mods:
            retVal.append(mod(str_i, usr_i))
        return retVal

class extnModules():
    emptyCall = 1
    wrongCommand = 2

    def __init__(self, timeout):
        self.timeout = timeout

        self.coms = []
        self.commands = []

        modules = glob.glob("module_*")
        for module in modules:
            module_name = module + "." + module[7:]
            mod = importlib.import_module(module_name)
            self.coms.append(mod.Com)
            self.commands.append(mod.command)

    def findModule(self, command_i, params, usr_i):
        for i, command in enumerate(self.commands):
            if command_i in command:
                return self.executeModule(self.coms[i], params, usr_i)

        return extnModules.wrongCommand
    
    def executeModule(self, foundCom, params, usr_i):
        decorated = TimeoutDeco(self.timeout, "TimeoutError", foundCom)
        try:
            ret = decorated(params, usr_i)
        except:
            return "ModuleError"
        else:
            if type(ret) != str:
                return "TypeError"
            elif len(ret) == 0:
                return "NullReturnError"
            else:
                return ret

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
            return self.findModule(params[1], params, usr_i)