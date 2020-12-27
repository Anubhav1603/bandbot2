import param
import time
from extensions import extnMods, extnModules

loadedModules = extnModules()
loadedMods = extnMods()

username = input("username? ")

def on_chat(usr_i, str_i):
    global loadedMods
    global loadedModules

    loadedMods.send_chat(usr_i, str_i)

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

if __name__ == '__main__':
    while True:
        print("--------------------------------------------------------")
        str_i = input(username + ": ")
        res = on_chat(username, str_i)
        for i, r in enumerate(res):
            print("response %d start {" % i)
            if r[0] == 'chat':
                print(r[1])
            elif r[0] == 'delay':
                time.sleep(float(r[1]))
            elif r[0] == 'image':
                print("IMAGE:", r[1])
            elif r[0] == 'change':
                print("채팅방 변경됨:", r[1])
            else:
                print("잘못된 response type")
            print("} response end")
        print("--------------------------------------------------------")
    