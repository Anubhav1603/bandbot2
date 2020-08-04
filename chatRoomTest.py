
class bandChat():
    def __init__(self, URL):
        self.chatURL = URL

    def chatPrint(self, str_i):
        lines = str_i.split("\n")
        isImage = False

        if len(lines) >= 2:
            for line in lines:
                if "REQUEST_IMAGE_" in line:
                    path = line[14:]
                    self.sendImage(path)
                    isImage = True

        if isImage:
            return

        for chat in lines:
            self.msgWrite.send_keys(chat)
            self.msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
        self.msgWrite.send_keys(Keys.ENTER)

    def HTMLget(self):
        pass