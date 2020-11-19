import param
from extensions import extnMods, extnModules

import bandchat

bot = bandchat.Client("https://band.us/band/77955502/chat/CQvbxV")

loadedModules = extnModules()
loadedMods = extnMods()
bot.run()

@bot.on_event
def on_chat(usr_i, str_i):
    global loadedMods
    global loadedModules
    if str_i[:3] == "!봇 ":
        params = str_i.split(" ")
        params = list(filter(params, lambda x: x != ""))
        if params[0] == "!봇":
            prefixChat = "[" + param.NAME + "] " + usr_i + "\n"

            paramnum = len(params)

            if paramnum == 1:
                resChat = prefixChat + param.GUIDE + loadedModules.strfModules()
            else:
                if params[1][0] == "_":
                    if params[1] == "_reload":
                        try:
                            loadedModules = extnModules()
                            loadedMods = extnMods()
                            resChat = "모듈 갱신완료"
                        except:
                            resChat = "모듈 갱신실패"
                else:
                    resChat = loadedModules.commandSel(params, usr_i)

                    if resChat == extnModules.wrongCommand:
                        resChat = prefixChat + "잘못된 명령입니다."
                    else:
                        resChat = prefixChat + resChat

            return [("chat", resChat)]