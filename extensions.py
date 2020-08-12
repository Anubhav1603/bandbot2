import importlib
import glob
from multiprocessing import Process

from API.timeout import TimeoutDeco

class extnMods():
    def __init__(self):
        self.mods = []

        modules = glob.glob("mod_*")
        for module in modules:
            module_name = module + "." + module[4:]
            mod = importlib.import_module(module_name)
            importlib.reload(mod)
            self.mods.append(mod.recvChat)

    def sendChat(self, usr_i, str_i):
        plist = []
        for mod in self.mods:
            p = Process(target = mod, args = (usr_i, str_i))
            p.start()
        
        for p in plist:
            p.join()

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
            importlib.reload(mod)
            self.coms.append(mod.Com)
            self.commands.append(mod.command)

    def _findModule(self, command_i, params, usr_i):
        for i, command in enumerate(self.commands):
            if command_i in command:
                return self._executeModule(self.coms[i], params, usr_i)

        return extnModules.wrongCommand
    
    def _executeModule(self, foundCom, params, usr_i):
        decorated = TimeoutDeco(self.timeout, "TimeoutError", foundCom)
        try:
            ret = decorated(params, usr_i)
        except:
            return "TimeoutException"
        else:
            if ret == None:
                return "ModuleException"
            elif type(ret) != str:
                return "TypeError"
            elif len(ret) == 0:
                return "NullReturnError"
            else:
                return ret

    def strfModules(self):
        allCommand = []
        for command in self.commands:
            for com in command:
                allCommand.append(com)
        return ", ".join(allCommand)

    def commandSel(self, params, usr_i):
        if len(params) == 1:
            return extnModules.emptyCall
        else:
            return self._findModule(params[1], params, usr_i)