import API.telegram
import teletoken
from time import strftime

def recvChat(usr_i, str_i):
    alarm_keywords = ["촉수","ㅎㅅㅋ","히사코"]
    for keyword in alarm_keywords:
        if keyword in str_i:
            bot = API.telegram.Bot(teletoken.TOKEN, teletoken.CHAT_ID)
            msg = strftime("%H:%M ") + usr_i + " is calling you.\n" + str_i
            bot.sendMessage(msg)
            
    alarm_users = ["레몬스타"]
    for keyuser in alarm_users:
        if keyuser == usr_i:
            bot = API.telegram.Bot(teletoken.TOKEN, teletoken.CHAT_ID)
            msg = "senpai alert" + strftime("%H:%M ") + str_i
            bot.sendMessage(msg)
    
    return False