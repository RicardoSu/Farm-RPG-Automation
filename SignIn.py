import sys
import time
import random
import mysecrets
from selenium import webdriver
from selenium.webdriver.common.by import By



class SignIn:
    def __init__(self, browser):
        self.browser = browser
        self.exitPlease = False

    def exitApp(self):
        print('exiting app')
        sys.exit()

    #Pause the program for a random amount of time between min_time and max_time seconds in miliseconds.
    def random_sleep(self,min_time, max_time):
        time.sleep(random.uniform(min_time, max_time))

    def main(self):
        login = f"https://farmrpg.com/index.php#!/login.php"
        self.browser.get(login)
        self.random_sleep(2,3)
        self.browser.find_element(By.NAME, "username").send_keys(mysecrets.username)
        self.random_sleep(0.1,0.3)
        self.browser.find_element(By.NAME, "password").send_keys(mysecrets.password)
        self.random_sleep(0.1,0.3)
        self.browser.find_element(By.CSS_SELECTOR, 'input#login_sub.button.btngreen').click()

    def farm_pond(self,id):
        fish_zone = f"https://farmrpg.com/#!/fishing.php?id={id}"
        self.browser.get(fish_zone)
        self.random_sleep(1,2)
        self.browser.refresh()
        self.random_sleep(2,3)
