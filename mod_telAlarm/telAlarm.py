import API.telegram
import teletoken
from time import strftime

def recvChat(usr_i, str_i):
    alarm_keywords = ["촉수","ㅎㅅㅋ","히사코","형석","KAIST","카이","히샄"]
    for keyword in alarm_keywords:
        if keyword in str_i:
            bot = API.telegram.Bot(teletoken.TOKEN, teletoken.CHAT_ID)
            msg = strftime("%H:%M ") + usr_i + " is calling you.\n" + str_i
            bot.sendMessage(msg)
            
    alarm_user_keywords = ["레몬"]
    for keyuser in alarm_user_keywords:
        if keyuser in usr_i:
            bot = API.telegram.Bot(teletoken.TOKEN, teletoken.CHAT_ID)
            msg = "VIP alert" + strftime("%H:%M ") + str_i
            bot.sendMessage(msg)
    
    return False