import sys
import time
import random
import mysecrets
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

class pettingChickens:
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
        coop = f"https://farmrpg.com/index.php#!/coop.php?id={mysecrets.farm_id}"
        self.browser.get(coop)
        self.random_sleep(2,3)

        coop = f"https://farmrpg.com/index.php#!/coop.php?id={mysecrets.farm_id}"
        self.browser.get(coop)
        self.random_sleep(2,3)

        # Find all the img elements with the specified attributes
        all_chickens = self.browser.find_elements(By.CSS_SELECTOR,'[data-id]')
        # print(elements)
        chickens_count = len(all_chickens)

        print(self.logTime() + f' : You have {chickens_count-1} chicken(s) to pet.')

        # Loop through each img element and click on it
        counter = 0
        for i in range(1,chickens_count):
            self.random_sleep(1,2)
            img_elements = self.browser.find_element(By.XPATH,f"//img[contains(@src, 'chicken.png') and @data-id='{i}']")
            img_elements.click()
            self.random_sleep(2,3)
            counter += 1
            self.browser.find_element(By.CLASS_NAME, "fa-heart").click()
            print(self.logTime() + f' : You have pet {counter} chicken(s).')
            self.random_sleep(1,2)
            self.browser.find_elements(By.CLASS_NAME, "modal-button-bold")[0].click()
            print(self.logTime()+' : OK.')
            self.random_sleep(1, 2)
