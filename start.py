import param
from extensions import extnMods, extnModules

import bandchat

# bot = bandchat.Client("https://band.us/band/55800178/chat/CP2C7U", cli_login=False, user_data="%localappdata%\\Google\\Chrome\\User Data")

bot = bandchat.Client("https://band.us/band/55800178/chat/C6HumD")

loadedModules = extnModules()
loadedMods = extnMods()

@bot.on_event
def on_chat(usr_no, usr_i, str_i):
    global loadedMods
    global loadedModules

    loadedMods.send_chat(usr_i, str_i)

    if str_i.startswith('!봇'):
        params = str_i.split(" ")
        params = list(filter(lambda x: x != "", params))
        if params[0] == "!봇":
            paramnum = len(params)

            if paramnum == 1:
                return [("chat", "https://bot.ster.email")]
            else:
                if params[1][0] == "_":
                    if params[1] == "_reload":
                        try:
                            loadedModules = extnModules()
                            loadedMods = extnMods()
                            return [("chat", "모듈 갱신완료")]
                        except:
                            return [("chat", "모듈 갱신실패")]
                    elif params[1] == "_moveto":
                        rcode = params[2]
                        return [("chat", f"https://band.us/band/55800178/chat/{rcode}")]
                else:
                    res = loadedModules.commandSel(params, usr_i)

                    if res == loadedModules.wrong_command:
                        return [("chat", "잘못된 명령입니다.")]
                    else:
                        return res
    return []

bot.run()