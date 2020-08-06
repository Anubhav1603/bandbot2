from module_pstcut.main import UpdateCache, PlotBorder

command = ["밀리역대컷"]
IMG_PATH = "REQUEST_IMAGE_module_pstcut/border_%s.png"

def Com(params, usr_i):
    paramnum = len(params)

    if paramnum == 3:
        if params[2] in ["시어터", "투어"]:
            PSType = "theater" if params[2] == "시어터" else "tour"
            UpdateCache(PSType)
            PlotBorder(PSType)
            return IMG_PATH % PSType
        else:
            return "pstcut.py: 사용법\n!봇 밀리역대컷 [투어|시어터]"
    else:
        return "pstcut.py: 사용법\n!봇 밀리역대컷 [투어|시어터]"