import importlib
import glob

from abc import ABC, abstractmethod
from multiprocessing import Process

def single_chat(method):
    def imethod(*args, **kwargs):
        res = method(*args, **kwargs)
        return [("chat", res)]
    return imethod

class ModuleBase(ABC):
    @property
    @abstractmethod
    def commands(self): pass

    @abstractmethod
    def run(self, params, usr_i): pass

class ModLoadError(Exception):
    def __init__(self):
        super().__init__("모드 로딩 실패")

class ModuleLoadError(Exception):
    def __init__(self):
        super().__init__("모듈 로딩 실패")

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
    empty_call = 1
    wrong_command = 2

    def __init__(self):
        self.commands = {}

        modules = glob.glob("module_*")
        for module in modules:
            module_name = module + "." + module[7:]
            mod = importlib.import_module(module_name)
            importlib.reload(mod)

            module_instance = mod.Module()

            for comm in module_instance.commands:
                if comm in self.commands:
                    print("Duplicated command:", comm)
                    raise ModuleLoadError
                else:
                    self.commands[comm] = module_instance

    def strfModules(self):
        return ", ".join(self.commands.keys())

    def commandSel(self, params, usr_i):
        command = params[1]
        if command in self.commands:
            try:
                res = self.commands[command].run(params, usr_i)
                for r in res:
                    if r[0] not in ['chat', 'image', 'delay', 'change']:
                        print("Wrong Response type:", r)
                        raise Exception
                return res
            except Exception as e:
                print(e)
                return [("chat", "모듈 에러")]
        else:
            return extnModules.wrong_command