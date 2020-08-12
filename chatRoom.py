from bs4 import BeautifulSoup

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from time import sleep, strftime, time
import os


class bandChat():
    def __init__(self, URL):
        self.chatURL = URL
        

        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--disable-extensions')
        options.add_argument("--no-sandbox")

        print("Driver initializing...")
        self.driver = Chrome(options=options)
        print("Driver initialized.")

        self.driver.get(self.chatURL)
        print("Get login page completed.")
        self.driver.implicitly_wait(3)

        self.driver.find_element_by_css_selector(
            ".uBtn.-icoType.-phone").click()
        print("Get PhonenumberPage completed.")
        self.driver.implicitly_wait(3)

        Phonenumber = input("전화번호 입력 :")
        self.driver.find_element_by_id(
            "input_local_phone_number").send_keys(Phonenumber)
        self.driver.find_element_by_css_selector(
            ".uBtn.-tcType.-confirm").click()
        print("Get PasswordPage completed.")
        self.driver.implicitly_wait(3)

        Password = input("비밀번호 입력 :")
        self.driver.find_element_by_id("pw").send_keys(Password)
        self.driver.find_element_by_css_selector(
            ".uBtn.-tcType.-confirm").click()
        print("Get SMSPage completed.")
        self.driver.implicitly_wait(8)
        try:
            print(self.driver.find_element_by_id("hintNumberDiv").text)
            sleep(20)
        except NoSuchElementException:
            pw_band = input("인증번호: ")
            self.driver.find_element_by_id("code").send_keys(str(pw_band))
            self.driver.find_element_by_css_selector(
                "button.uBtn.-tcType.-confirm").click()
            print("Driver get completed.")

        self.get_msgWrite()

    def get_msgWrite(self):
        startsec = time()
        while(True):
            try:
                self.msgWrite = self.driver.find_element_by_class_name(
                    "commentWrite")
            except:
                if(time() > startsec + 10):
                    print("CHAT LOAD ERROR at " + strftime("%Y.%M.%D, %H:%M"))
                    exit()
                continue
            break
        sleep(1)
        print("boot success")

    def loginRefresh(self):
        self.driver.refresh()

        self.get_msgWrite()
        self.driver.implicitly_wait(30)

    def sendImage(self, rPath):
        try:
            absPath = os.path.abspath(rPath)
            img_up = self.driver.find_element_by_css_selector(
                "input[data-uiselector='imageUploadButton']")
            img_up.send_keys(absPath)
        except Exception as e:
            print(e)
        return

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
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        chatlist = soup.find_all("span", class_="txt")
        userlist = soup.find_all("button", class_="author")
        return len(chatlist), chatlist, userlist
