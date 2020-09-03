import sys
from time import sleep, strftime

import param
from extensions import extnMods, extnModules
from chatRoom import bandChat

def removeList(asdf, function):
    toRemove = []
    for i, elem in enumerate(asdf):
        if function(elem):
            toRemove.append(i)
    toRemove.reverse()
    for i in toRemove:
        asdf.pop(i)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("***BANDBOT STARTED IN SERVICE MODE***")
        if input("Continue? (Y)") != "Y":
            exit()

        loadedModules = extnModules()
        loadedMods = extnMods()
        chatRoom = bandChat(param.chatURL)

        timeFlag = int(strftime("%M")) < 30

        len_chat, i_chat, i_user = chatRoom.HTMLget()
        recent_chat = len(i_chat)

        while True:
            minNow = int(strftime("%M"))
            if (minNow < 30 and timeFlag) or (minNow >= 30 and not timeFlag):
                timeFlag = not timeFlag
                chatRoom.loginRefresh()

            len_chat, i_chat, i_user = chatRoom.HTMLget()

            for i in range(recent_chat-len_chat, 0):
                str_i = i_chat[i].text
                usr_i = i_user[i].text
                print(usr_i + ":" + str_i)

                loadedMods.sendChat(usr_i, str_i)

                if str_i[:2] == "!봇":
                    params = str_i.split(" ")
                    removeList(params, lambda x: x == "")
                    
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

                        chatRoom.chatPrint(resChat)
            
            recent_chat = len_chat
            sleep(0.5)

    
    elif sys.argv[1] == "--test":
        print("***BANDBOT STARTED IN SIMPLE TEST MODE***")
        print("this mode tests modules only")
        print("test username is \"QwErTyTeSt\".")
        print("type \"!exit\" to exit\n")

        loadedModules = extnModules()
        loadedMods = extnMods()

        while True:
            str_i = input("test chat: ")
            usr_i = "QwErTyTeSt"
            if str_i == "!exit":
                break

            print("chatResponse start--------------------\n")
            loadedMods.sendChat(usr_i, str_i)
            if str_i[:2] == "!봇":
                params = str_i.split(" ")
                removeList(params, lambda x: x == "")
                
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

                    print(resChat)

            print("\nchatResponse end:--------------------\n")