from extensions import ModBase

import API.telegram
import teletoken

class SimpleQueue():
    def __init__(self, maxsize):
        self.data = []
        self.maxsize = maxsize
    
    def add(self, element):
        if(len(self.data) < self.maxsize):
            self.data.append(element)
        else:
            self.data.pop(0)
            self.data.append(element)

class Mod(ModBase):
    def __init__(self):
        self.chatsave = SimpleQueue(15)

    def recv_chat(self, usr_i, str_i):
        if (usr_i == "ㅎㅅㅋ" or usr_i == "QwErTyTeSt") and str_i == "!봇 복구":
            bot = API.telegram.Bot(teletoken.TOKEN, teletoken.CHAT_ID)
            bot.sendMessage("최근 채팅기록 15개를 복원합니다.")

            for chat in self.chatsave.data:
                bot.sendMessage(chat[0] + ": " + chat[1])

        elif usr_i != "ㅎㅅㅋ":
            self.chatsave.add((usr_i, str_i))