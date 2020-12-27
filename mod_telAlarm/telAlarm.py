from extensions import ModBase

import API.telegram
import teletoken

class Mod(ModBase):
    def __init__(self):
        self.bot = API.telegram.Bot(teletoken.TOKEN, teletoken.CHAT_ID)

    def recv_chat(self, usr_i, str_i):
        alarm_user_keywords = ["레몬"]
        for keyuser in alarm_user_keywords:
            if keyuser in usr_i:
                msg = "VIP alert" + str_i
                self.bot.sendMessage(msg)
                return

        alarm_keywords = ["촉수","ㅎㅅㅋ","히사코","형석","KAIST","카이","히샄"]
        for keyword in alarm_keywords:
            if keyword in str_i:
                msg = usr_i + " is calling you.\n" + str_i
                self.bot.sendMessage(msg)
                return
