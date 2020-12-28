from time import sleep, strftime, time
import os

import requests

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options

class BandchatException(Exception):
    def __init__(self, msg = "Bandchat module error"):
        super().__init__(msg)

class ChatLoadException(BandchatException):
    def __init__(self):
        super().__init__("Chat load error")

class LoginFailure(BandchatException):
    def __init__(self):
        super().__init__("Login failed")

class InvalidEventException(BandchatException):
    def __init__(self):
        super().__init__("Invalid on_event name")

TYPEDICT = {
            'DChattingRoomTextMessageItemView': 0,
            'DChattingRoomStickerMessageItemView': 1,
            'DChattingRoomPhotoMessageItemView': 2,
            'DChattingRoomVideoMessageItemView': 3,
            'DChattingRoomAniGifMessageItemView': 4,
            'DChattingRoomFileMessageItemView': 5,
            'UnknownOrDeletedMessage': 6
           }

class ChatObject():
    # Types
    # 0: Text
    # 1: Sticker
    # 2: Image
    # 3: Video
    # 4: GIF
    # 5: File
    # 6: Unknown or deleted message object
    def __init__(self, webelement):
        self._elem = webelement

        try:
            viewname = self._elem.get_attribute('data-viewname')
            viewclass = self._elem.get_attribute('class')
            if viewname in TYPEDICT:
                self.type = TYPEDICT[viewname]
            else: raise ValueError

            self.ismychat = 'logMy' in viewclass
            
            if self.ismychat:
                self.user = "^_+_MYCHAT"
            else:
                self.user = self._elem.find_element_by_css_selector('.author').text

            if self.type == 0:
                self.text = self._elem.find_element_by_css_selector('._messageContent').text
            else:
                self.text = "^_+_Parsing nontext chat is not implemented yet"
        except:
            self.type = 6
            self.ismychat = False
            self.user = "Unknown"
            self.text = "^_+_Unknown"
    
    def get_reply(self):
        if self.type == 6: 
            print("Cannot reply to unknown or deleted chat")
            return False

        try:
            self._elem.find_element_by_css_selector('button.btnMore').click()
            self._elem.find_element_by_css_selector('button[data-menutype="MENU_TYPE_REPLY"]').click()
            return True
        except Exception as e:
            print(e)
            return False

    def send_emotion(self, emotiontype):
        typelist = ['great', 'funny', 'like', 'shocked', 'sad', 'angry']

        if self.type == 6:
            print("Cannot send emotion to unknown or deleted chat")
            return False

        elif self.ismychat:
            print("Cannot send emotion to my chat")
            return False

        elif emotiontype not in typelist:
            print("Wrong emotiontype")
            return False

        try:
            self._elem.find_element_by_css_selector('button.btnMore').click()
            self._elem.find_element_by_css_selector('button[data-menutype="MENU_TYPE_EMOTION"]').click()
            self._elem.find_element_by_css_selector(f'button[data-emotion-type="{emotiontype}"]').click()
        except Exception as e:
            print(e)
            return False

class Client():
    def __init__(self, url,
                 get_rate=0.5,
                 refresh_rate=1800,
                 cli_login=True,
                 user_data=None,
                 ):
        self.chatURL = url
        self.refresh_rate = refresh_rate
        self.get_rate = get_rate
        
        self.on_chat = lambda x,y: []
        self.on_ready = lambda :[]

        options = ChromeOptions()

        options.add_argument('--disable-extensions')
        options.add_argument("--no-sandbox")
        if cli_login:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
        
        if user_data is not None:
            options.add_argument(f"--user-data-dir={user_data}")
        
        print("Driver initializing...")
        self.driver = Chrome(options=options)
        print("Driver initialized.")
        self.driver.implicitly_wait(3)

        if cli_login:
            try:
                self.driver.get(self.chatURL)
                print("Get login page completed.")
            except requests.exceptions.ConnectionError:
                raise LoginFailure

            try:
                self.driver.find_element_by_css_selector(
                    ".uBtn.-icoType.-phone").click()
                print("Get PhonenumberPage completed.")

                Phonenumber = input("Phone number: +82")
                self.driver.find_element_by_id(
                    "input_local_phone_number").send_keys(Phonenumber)
                self.driver.find_element_by_css_selector(
                    ".uBtn.-tcType.-confirm").click()
                print("Get PasswordPage completed.")

                Password = input("Password: ")
                self.driver.find_element_by_id("pw").send_keys(Password)
                self.driver.find_element_by_css_selector(
                    ".uBtn.-tcType.-confirm").click()
                print("Get SMSPage completed.")
                self.driver.implicitly_wait(8)
            except NoSuchElementException:
                raise LoginFailure
            
            try:
                print(self.driver.find_element_by_id("hintNumberDiv").text)
                sleep(20)
            except NoSuchElementException:
                pw_band = input("SMS authcode: ")
                self.driver.find_element_by_id("code").send_keys(str(pw_band))
                self.driver.find_element_by_css_selector(
                    "button.uBtn.-tcType.-confirm").click()
                print("Driver get completed.")
        else:
            input("Please login from GUI.\nPress Enter to Continue...")

        self._get_msgbox()

    def _get_msgbox(self):
        startsec = time()
        while(True):
            try:
                self.msgWrite = self.driver.find_element_by_class_name(
                    "commentWrite")
            except NoSuchElementException:
                if(time() > startsec + 10):
                    raise ChatLoadException
                sleep(1)
                continue
            break
        sleep(1)
        print("Messagebox grabbed")

    def _refresh(self):
        self.last_refresh = time()
        self.next_refresh = self.last_refresh + self.refresh_rate

        self.driver.get(self.chatURL)
        self._get_msgbox()
        self.driver.implicitly_wait(10)

    def _send_image(self, rPath):
        try:
            absPath = os.path.abspath(rPath)
            img_up = self.driver.find_element_by_css_selector(
                "input[data-uiselector='imageUploadButton']")
            img_up.send_keys(absPath)
        except Exception as e:
            print(e)
        return

    def _send_chat(self, str_i):
        lines = str_i.split("\n")

        for chat in lines:
            self.msgWrite.send_keys(chat)
            self.msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
        self.msgWrite.send_keys(Keys.ENTER)

    def _get_chats(self):
        chats = self.driver.find_elements_by_css_selector('._childViewContainer>.logWrap')

        chatlist = []
        for chat in chats:
            try:
                chatlist.append(ChatObject(chat))
            except Exception as e:
                print(e)
        
        return chatlist

    def _get_chats_len(self):
        chats = self.driver.find_elements_by_class_name('logWrap')
        return len(chats)

    def _parse_response(self, res_lst):
        for res in res_lst:
            if res[0] == "chat":
                self._send_chat(res[1])
            elif res[0] == "image":
                self._send_image(res[1])
            elif res[0] == "change":
                self.chatURL = res[1]
                self._refresh()
            elif res[0] == "delay":
                sleep(float(res[1]))
    
    def on_event(self, ifunction):
        if ifunction.__name__ == "on_chat":
            self.on_chat = ifunction
        elif ifunction.__name__ == "on_ready":
            self.on_ready = ifunction
        else:
            raise InvalidEventException

    def run(self):
        self._refresh()
        recent_chat = self._get_chats_len()
        self._parse_response(self.on_ready())

        while True:
            if time() >= self.next_refresh:
                self._refresh()
                recent_chat = self._get_chats_len()
                len_chat = recent_chat
            
            len_chat = self._get_chats_len()

            if len_chat > recent_chat:
                chat_list = self._get_chats()
                for i in range(recent_chat - len_chat, 0):
                    chat = chat_list[i]
                    print(chat.user + ":" + chat.text)
                    self._parse_response(self.on_chat(chat))
            
            recent_chat = len_chat
            sleep(self.get_rate)