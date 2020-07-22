import requests

URL = "https://api.telegram.org/bot%s/%s"

class Bot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
    
    def sendMessage(self, message):
        req = {'chat_id': self.chat_id, 'text': message}
        res = requests.get(URL % (self.token, "sendMessage"), data = req)

    def getUpdates(self):
        res = requests.get(URL % (self.token, "getUpdates"))
        res = res.json()
        if len(res["result"]) == 0:
            raise Exception
        else:
            return res["result"][-1]