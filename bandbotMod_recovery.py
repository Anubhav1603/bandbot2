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

CHATSAVE = SimpleQueue(10)

def recvChat(usr_i, str_i):
    if (usr_i == "ㅎㅅㅋ" or usr_i == "QwErTyTeSt") and str_i == "!봇 복구":
        bot = teletoken.getBot()
        teletoken.sendChat(bot, "최근 채팅기록 10개를 복원합니다.")
        for chat in CHATSAVE.data:
            teletoken.sendChat(bot, chat[0] + ": " + chat[1])
        return True

    elif usr_i != "ㅎㅅㅋ":
        CHATSAVE.add((usr_i, str_i))
        return False