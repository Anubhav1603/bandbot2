import json

from extensions import extnMods, extnModules
import bandchat

URL = "https://band.us/band/55800178/chat/C6HumD"

# bot = bandchat.Client(URL, cli_login=False, user_data="%localappdata%\\Google\\Chrome\\User Data")

bot = bandchat.Client(URL)

f = open('redirection.json', 'r', encoding='utf-8')
primitive_db = json.load(f)
f.close()

redir_db = {}
for item in primitive_db:
    redir_db[item['user_no']] = item['addr']

loadedModules = extnModules()
loadedMods = extnMods()
enabled = True

def parser(params, usr_i):
    global loadedMods
    global loadedModules
    global enabled

    params = list(filter(lambda x: x != "", params))
    paramnum = len(params)

    if paramnum == 1:
        return [("chat", "http://bot.ster.email")]
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

@bot.on_event
def on_chat(usr_no, usr_i, str_i):
    loadedMods.send_chat(usr_i, str_i)

    if str_i.startswith('!봇'):
        params = str_i.split(" ")
        
        if params[0] == "!봇":
            if '>' in str_i:
                splitted = str_i.split('>')
                dst = splitted[1]
                if '갠챗' in dst:
                    params = splitted[0].split(" ")
                    res = parser(params, usr_i)
                    addr = redir_db[int(usr_no)]
                    addr = 'https://band.us/band/55800178/chat/' + addr

                    print(addr)
                    
                    chg = [("change", addr)]
                    chg.extend(res)
                    chg.append(("change", URL))

                    return chg

                else:
                    return []
            else:
                return parser(params, usr_i)
    return []
bot.run()