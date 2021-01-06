import requests
import gzip

from module_pstcut.main import UpdateCache, PlotBorder
from extensions import ModuleBase

IMG_PATH = "module_pstcut/border_%s_%d.png"

def chat(msg): return [("chat", msg)]
def image(path): return [("image", path)]

class Module(ModuleBase):
    commands = ["밀리역대컷"]

    def __init__(self):
        print("Decompressing JP fonts...")
        f_src = gzip.open("module_pstcut/NotoSansCJKjp.otf.gz", "rb")
        f_dst = open("module_pstcut/NotoSansCJKjp.otf", "wb")
        f_dst.write(f_src.read())
        f_src.close()
        f_dst.close()
        print("Decompressed NotoSansCJKjp.otf")

    def run(self, params, usr_i):
        paramnum = len(params)

        if paramnum == 4:
            if params[2] in ["시어터", "투어"]:
                if params[3] in ["2500", "100"]:
                    PSType = "theater" if params[2] == "시어터" else "tour"
                    PSBorder = 2500 if params[3] == '2500' else 100
                    UpdateCache(PSType, PSBorder)
                    PlotBorder(PSType, PSBorder)
                    return image(IMG_PATH % (PSType, PSBorder))
            else:
                return chat("pstcut.py: 사용법\n!봇 밀리역대컷 [투어|시어터] [100|2500]")
        else:
            return chat("pstcut.py: 사용법\n!봇 밀리역대컷 [투어|시어터] [100|2500]")