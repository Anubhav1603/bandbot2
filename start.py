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

        loadedModules = extnModules(6)
        loadedMods = extnMods()
        chatRoom = bandChat(param.chatURL)

        timeFlag = int(strftime("%M")) < 30

        len_chat, i_chat, i_user = chatRoom.HTMLget()
        recent_chat = len(i_chat)

        while(True):
            minNow = int(strftime("%M"))
            if (minNow < 30 and timeFlag) or (minNow >= 30 and not timeFlag):
                timeFlag = not timeFlag
                chatRoom.loginRefresh()

            len_chat, i_chat, i_user = chatRoom.HTMLget()

            for i in range(recent_chat-len_chat, 0):
                str_i = i_chat[i].text
                usr_i = i_user[i].text
                print(usr_i + ":" + str_i)

                isCommand = loadedMods.sendChat(usr_i, str_i)

                if str_i[:2] == "!봇":
                    params = str_i.split(" ")
                    removeList(params, lambda x: len(x) == 0)
                    if params[0] == "!봇":
                        prefixChat = "[" + param.NAME + "] " + usr_i + "\n"
                        responseChat = loadedModules.commandSel(params, usr_i)

                        if True in isCommand:
                            chatRoom.chatPrint(prefixChat + "명령실행 완료")
                        elif responseChat == extnModules.wrongCommand:
                            chatRoom.chatPrint(prefixChat + "잘못된 명령입니다.")
                        elif responseChat == extnModules.emptyCall:
                            chatRoom.chatPrint(
                                prefixChat + param.GUIDE + loadedModules.strfModules())
                        else:
                            chatRoom.chatPrint(prefixChat + responseChat)
            
            recent_chat = len_chat
            sleep(0.5)

    
    elif sys.argv[1] == "--test":
        print("***BANDBOT STARTED IN SIMPLE TEST MODE***")
        print("this mode tests modules only")
        print("test username is \"QwErTyTeSt\".")
        print("type \"!exit\" to exit\n")

        loadedModules = extnModules(6)
        loadedMods = extnMods()

        while True:
            str_i = input("test chat: ")
            usr_i = "QwErTyTeSt"
            if str_i == "!exit":
                break
            
            isCommand = loadedMods.sendChat(usr_i, str_i)

            print("chatResponse start--------------------\n")
            if str_i[:2] == "!봇":
                params = str_i.split(" ")
                removeList(params, lambda x: len(x) == 0)
                if params[0] == "!봇":
                    prefixChat = "[" + param.NAME + "] " + usr_i + "\n"
                    responseChat = loadedModules.commandSel(params, usr_i)

                    if True in isCommand:
                        print(prefixChat + "명령실행 완료")
                    elif responseChat == extnModules.wrongCommand:
                        print(prefixChat + "잘못된 명령입니다.")
                    elif responseChat == extnModules.emptyCall:
                        print(prefixChat + param.GUIDE + loadedModules.strfModules())
                    else:
                        print(prefixChat + responseChat)

            print("\nchatResponse end:--------------------\n")