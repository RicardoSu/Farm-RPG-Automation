import sys
import time
import random
import mysecrets
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

class PettingCows:
    def __init__(self, browser):
        self.browser = browser
        self.exitPlease = False

    def exitApp(self):
        print('exiting app')
        sys.exit()

    def random_sleep(self, min_time, max_time):
        time.sleep(random.uniform(min_time, max_time))

    def logTime(self):
        return datetime.now().strftime("%H:%M:%S")
    
    def main(self):
        pasture = f"https://farmrpg.com/index.php#!/pasture.php?id={mysecrets.farm_id}"
        self.browser.get(pasture)
        self.random_sleep(2,3)
        self.browser.refresh()
        self.random_sleep(2,3)

        # Find all the img elements with the specified attributes
        all_cowss = self.browser.find_elements(By.CSS_SELECTOR,'[data-id]')
        cows_count = len(all_cowss)

        print(self.logTime() + f' : You have {cows_count-1} cows(s) to pet.')

        # Loop through each img element and click on it
        for i in range(1,cows_count):
            print(i)
            try:
                self.random_sleep(1,2)
                cows = f"https://farmrpg.com/#!/namecow.php?id={i}&farm=243308"
                self.browser.get(cows)
                self.random_sleep(2,3)
                self.browser.refresh()
                self.random_sleep(1.5,2)
                self.browser.find_element(By.CLASS_NAME, "fa-heart").click()
                print(self.logTime() + f' : You have pet {i} cows(s).')
                self.random_sleep(1,2)
                self.browser.find_elements(By.CLASS_NAME, "modal-button-bold")[0].click()
                print(self.logTime()+' : OK.')
                self.random_sleep(1, 2)
            except Exception as e:
                print(f"An exception occurred while processing cows {i}: {e}")
