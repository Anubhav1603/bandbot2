import param
from extensions import extnMods, extnModules

import bandchat

bot = bandchat.Client("https://band.us/band/55800178/chat/CP2C7U", cli_login=False, user_data="%localappdata%\\Google\\Chrome\\User Data")

# bot = bandchat.Client("https://band.us/band/55800178/chat/C6HumD")

loadedModules = extnModules()
loadedMods = extnMods()

@bot.on_event
def on_chat(chatobj):
    global loadedMods
    global loadedModules

    usr_i = chatobj.user
    str_i = chatobj.text

    loadedMods.send_chat(usr_i, str_i)

    if str_i.startswith('!봇'):
        params = str_i.split(" ")
        params = list(filter(lambda x: x != "", params))
        if params[0] == "!봇":
            paramnum = len(params)

            if paramnum == 1:
                chatobj.get_reply()
                return [("chat", "https://bot.ster.email")]
            else:
                if params[1][0] == "_":
                    if params[1] == "_reload":
                        chatobj.get_reply()
                        try:
                            loadedModules = extnModules()
                            loadedMods = extnMods()
                            return [("chat", "모듈 갱신완료")]
                        except:
                            return [("chat", "모듈 갱신실패")]
                else:
                    res = loadedModules.commandSel(params, usr_i)

                    if res == loadedModules.wrong_command:
                        chatobj.send_emotion('angry')
                        return []
                    else:
                        # TODO: 예외처리 좀더 상세히.
                        can_reply = True
                        for r in res:
                            if r[0] == 'image':
                                can_reply = False
                        if can_reply: chatobj.get_reply()
                        return res
    return []

bot.run()