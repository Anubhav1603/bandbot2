import telegram
import teletoken
from time import strftime

def recvChat(usr_i, str_i):
    alarm_keywords = ["촉수","ㅎㅅㅋ","히사코"]
    for keyword in alarm_keywords:
        if keyword in str_i:
            bot = teletoken.getBot()
            msg = strftime("%H:%M ") + usr_i + " is calling you.\n" + str_i
            teletoken.sendChat(bot, msg)
            
    alarm_users = ["레몬스타"]
    for keyuser in alarm_users:
        if keyuser == usr_i:
            bot = teletoken.getBot()
            msg = "senpai alert" + strftime("%H:%M ") + str_i
            teletoken.sendChat(bot, msg)