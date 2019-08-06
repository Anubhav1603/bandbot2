from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime, time

import datetime
import param

def loadingWait(driver):
	startsec = time()
	while(True):
		try:
			msgWrite = driver.find_element_by_class_name("commentWrite")
		except:
			if(time() > startsec+20):
				now = datetime.datetime.now()
				print("CHAT LOAD ERROR at " + now.isoformat())
				raise ChatError
				exit()
			continue
		break
	sleep(1)
	print("[" + param.NAME + "] " + param.version + " boot success")
	return msgWrite

def loginRefresh(doSilent):
	chromeOptions = {"debuggerAddress":"127.0.0.1:"+param.ChromeDevPort}
	capabilities = {"chromeOptions":chromeOptions}
	print("Driver initializing...")
	driver = webdriver.Remote("http://127.0.0.1:"+param.WebdriverPort, capabilities)
	print("Driver initialized.")
	driver.get(param.chatURL)
	print("Driver get completed.")
	msgWrite = loadingWait(driver)
	driver.implicitly_wait(30)
	if not doSilent:
		msgWrite.send_keys("[" + param.NAME + "] 새로고침 완료")
		msgWrite.send_keys(Keys.ENTER)
	return driver, msgWrite

if __name__ == "__main__":
	chromeOptions = {"debuggerAddress":"127.0.0.1:"+param.ChromeDevPort}
	capabilities = {"chromeOptions":chromeOptions}
	print("Driver initializing...")
	driver = webdriver.Remote("http://127.0.0.1:"+param.WebdriverPort, capabilities)
	print("Driver initialized.")

	driver.get(param.chatURL)
	print("Get login page completed.")
	driver.implicitly_wait(3)

	driver.find_element_by_css_selector(".uBtn.-icoType.-phone").click()
	print("Get PhonenumberPage completed.")
	driver.implicitly_wait(3)

	Phonenumber = input("전화번호 입력 :")
	driver.find_element_by_id("input_local_phone_number").send_keys(Phonenumber)
	driver.find_element_by_css_selector(".uBtn.-tcType.-confirm").click()
	print("Get PasswordPage completed.")
	driver.implicitly_wait(3)

	Password = input("비밀번호 입력 :")
	driver.find_element_by_id("pw").send_keys(Password)
	driver.find_element_by_css_selector(".uBtn.-tcType.-confirm").click()
	print("Get SMSPage completed.")
	driver.implicitly_wait(8)

	#driver.find_element_by_css_selector(".uBtn.-tcType.-confirm.gMat28").click()
	#print("Get SMSWaitPage completed.")
	#driver.implicitly_wait(8)

	#pw_band=input("인증번호: ")
	#driver.find_element_by_id("code").send_keys(str(pw_band))
	print(driver.find_element_by_id("hintNumberDiv").text)

	sleep(20)
	#driver.find_element_by_css_selector("button.uBtn.-tcType.-confirm").click();
	#print("Driver get completed.")

	msgWrite = loadingWait(driver)