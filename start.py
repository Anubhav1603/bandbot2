import param
from extensions import extnMods, extnModules

import bandchat

bot = bandchat.Client("https://band.us/band/77955502/chat/C6HumD")

loadedModules = extnModules()
loadedMods = extnMods()

@bot.on_event
def on_chat(usr_i, str_i):
    global loadedMods
    global loadedModules
    if str_i.startswith('!봇'):
        params = str_i.split(" ")
        params = list(filter(lambda x: x != "", params))
        if params[0] == "!봇":
            prefixChat = "[" + param.NAME + "] " + usr_i + "\n"

            paramnum = len(params)

            if paramnum == 1:
                return [("chat", prefixChat + param.GUIDE + loadedModules.strfModules())]
            else:
                if params[1][0] == "_":
                    if params[1] == "_reload":
                        try:
                            loadedModules = extnModules()
                            loadedMods = extnMods()
                            return [("chat", "모듈 갱신완료")]
                        except:
                            return [("chat", "모듈 갱신실패")]
                else:
                    res = loadedModules.commandSel(params, usr_i)

                    if res == loadedModules.wrong_command:
                        return [("chat", "잘못된 명령어입니다.")]
                    else:
                        return res
    
    return []
bot.run()