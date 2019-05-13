import telegram

def getBot():
	return telegram.Bot(token = "")

def sendChat(bot, message):
	bot.sendMessage(chat_id = "", text = message)