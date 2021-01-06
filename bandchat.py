from time import sleep
import os
import json
import gzip

import requests

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from seleniumwire.webdriver import Chrome
from seleniumwire.webdriver import ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

class Client():
    def __init__(self, url,
                 get_rate=0.5,
                 chat_per_refresh=100,
                 cli_login=True,
                 user_data=None,
                 timeout=10,
                 ):
        self.chatURL = url
        self.chat_per_refresh = chat_per_refresh
        self.get_rate = get_rate
        self.timeout = timeout
        
        self.on_chat = lambda x,y: []
        self.on_ready = lambda : []
        self.dict_user = {}

        def response_interceptor(req, res):
            if 'sync_chat_channel' in req.url and req.method == 'GET':
                try:
                    dict_raw = gzip.decompress(res.body)
                    dict_usr = json.loads(dict_raw)
                    dict_usr = dict_usr['result_data']['users']
                    for usr in dict_usr:
                        self.dict_user[usr["user_no"]] = usr["name"]
                    print("Found usercode-username dictionary")
                except:
                    print("Invalid dictionary")

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {
            'performance':'ALL'
        }

        options = ChromeOptions()
        options.add_experimental_option('perfLoggingPrefs', {
            'enableNetwork': True,
            'enablePage': False
        })
        options.add_argument('--disable-extensions')
        options.add_argument("--no-sandbox")
        if cli_login:
            options.headless = True
        if user_data is not None:
            options.add_argument(f"--user-data-dir={user_data}")
        
        print("Driver initializing...")
        self.driver = Chrome(options=options)
        self.driver.response_interceptor = response_interceptor
        self.driver.implicitly_wait(timeout)
        print("Driver initialized.")

        if cli_login:
            try:
                self.driver.get(self.chatURL)
                print("Get login page completed.")
            except requests.exceptions.ConnectionError:
                raise LoginFailure

            try:
                self._locate_by_css_selector(".uBtn.-icoType.-phone").click()

                phone_box = self._locate_by_id("input_local_phone_number")
                print("Get PhonenumberPage completed.")

                phone = input("Phone number: +82")
                phone_box.send_keys(phone)
                self._locate_by_css_selector(".uBtn.-tcType.-confirm").click()

                pw_box = self._locate_by_id("pw")
                print("Get PasswordPage completed.")

                pw = input("Password: ")
                self._locate_by_id("pw").send_keys(pw)
                self._locate_by_css_selector(".uBtn.-tcType.-confirm").click()
                
                print("Get SMSPage completed.")
            except NoSuchElementException:
                raise LoginFailure
            
            try:
                print("Trying to get hintNumberDiv...")
                hint = self._locate_by_id("hintNumberDiv")
                print("Hintnumber:", hint.text)
                input("Press Enter to continue...")
            except Exception as e:
                print("Retrieving SMS authcode...")
                code_box = self._locate_by_id("code")
                print("codebox grabbed")
                pw_band = input("SMS authcode: ")
                code_box.send_keys(str(pw_band))
                self._locate_by_css_selector(
                    "button.uBtn.-tcType.-confirm").click()
                print("Login completed.")
        else:
            self.driver.get(self.chatURL)
            input("Please login from GUI.\nPress Enter to Continue...")

        self._refresh()
        self._clear_log()

    def _clear_log(self):
        self.driver.get_log('performance')
        
    def _refresh(self):
        self.driver.get(self.chatURL)
        self.msgWrite = self._locate_by_class("commentWrite")
        print("Messagebox grabbed")
    
    def _locate_by_id(self, id_name):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.ID, id_name)))
    
    def _locate_by_class(self, class_name):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    
    def _locate_by_css_selector(self, css):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css)))

    def _send_image(self, rPath):
        try:
            absPath = os.path.abspath(rPath)
            img_up = self._locate_by_css_selector(
                "input[data-uiselector='imageUploadButton']")
            img_up.send_keys(absPath)
            sleep(2)
        except Exception as e:
            print(e)
        return

    def _send_chat(self, str_i):
        lines = str_i.split("\n")
        last_index = len(lines) - 1

        for i, chat in enumerate(lines):
            self.msgWrite.send_keys(chat)
            if i != last_index:
                self.msgWrite.send_keys(Keys.SHIFT, Keys.ENTER)
        WebDriverWait(self.driver, 5).until(lambda x: self.msgWrite.get_attribute('value') == str_i)
        self.msgWrite.send_keys(Keys.ENTER)

    def _parse_response(self, res_lst):
        try:
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
        except Exception as e:
            print(e)
            print("Error while parsing response")
    
    def on_event(self, ifunction):
        if ifunction.__name__ == "on_chat":
            self.on_chat = ifunction
        elif ifunction.__name__ == "on_ready":
            self.on_ready = ifunction
        else:
            raise InvalidEventException

    def run(self):
        self._refresh()
        num_chats = 0
        while True:
            if num_chats > self.chat_per_refresh:
                self._refresh()
                num_chats = 0

            for log in self.driver.get_log('performance'):
                try:
                    message = log['message']
                    if "Network.webSocketFrameReceived" not in message:
                        continue
                    elif "userNo" not in message:
                        continue
                    elif "contents" not in message:
                        continue

                    num_chats += 1
                    msg = json.loads(message)
                    payload = msg['message']['params']['response']['payloadData']
                    from_index = payload.find(',') + 1
                    message_parsed = json.loads(payload[from_index:])

                    chat_parsed = message_parsed[1]['message']
                    user_no = chat_parsed['userNo']
                    chat_body = chat_parsed['contents']
                    try:
                        user_str = self.dict_user[int(user_no)]
                    except Exception as e:
                        print(e)
                        user_str = "unknown_user"

                    print(f"{user_str}: {chat_body}")
                    res = self.on_chat(user_no, user_str, chat_body)
                    self._parse_response(res)

                except Exception as e:
                    print(e)
                    continue

            sleep(self.get_rate)