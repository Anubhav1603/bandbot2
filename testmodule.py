import param
from extensions import extnMods, extnModules

loadedModules = extnModules()
loadedMods = extnMods()

username = input("username? ")

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
                    elif "REQUEST_IMAGE_" in resChat:
                        resList = []
                        for line in resChat.split('\n'):
                            if line[:14] == "REQUEST_IMAGE_":
                                resList.append(("image", line[14:]))
                        return resList

                    else:
                        resChat = prefixChat + resChat

            return [("chat", resChat)]

if __name__ == '__main__':
    while True:
        print("--------------------------------------------------------")
        str_i = input(username + ": ")
        print("response start {")
        print(on_chat(username, str_i))
        print("} response end")
        print("--------------------------------------------------------")
    