import requests

from module_pstcut.main import UpdateCache, PlotBorder
from extensions import ModuleBase

IMG_PATH = "module_pstcut/border_%s.png"

def chat(msg): return [("chat", msg)]
def image(path): return [("image", path)]

class Module(ModuleBase):
    commands = ["밀리역대컷"]

    def __init__(self):
        print("Downloading JP fonts...")
        resFont = requests.get("https://si.ster.email/dl/NotoSansCJKjp.otf")
        f = open("module_pstcut/NotoSansCJKjp.otf", "wb")
        f.write(resFont.content)
        f.close()
        print("downloaded.")

    def run(self, params, usr_i):
        paramnum = len(params)

        if paramnum == 3:
            if params[2] in ["시어터", "투어"]:
                PSType = "theater" if params[2] == "시어터" else "tour"
                UpdateCache(PSType)
                PlotBorder(PSType)
                return image(IMG_PATH % PSType)
            else:
                return chat("pstcut.py: 사용법\n!봇 밀리역대컷 [투어|시어터]")
        else:
            return chat("pstcut.py: 사용법\n!봇 밀리역대컷 [투어|시어터]")