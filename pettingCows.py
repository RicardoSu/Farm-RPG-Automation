import sys
import time
import random
import mysecrets
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

class pettingCows:  
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

      pasture = f"https://farmrpg.com/index.php#!/pasture.php?id={mysecrets.farm_id}"
      self.browser.get(pasture)
      self.random_sleep(2,3)

      # Find all the img elements with the specified attributes
      all_cows = self.browser.find_elements(By.CSS_SELECTOR,'[data-id]')
      # print(elements)
      cows_count = len(all_cows)

      print(self.logTime() + f' : You have {cows_count-1} cows(s) to pet.')

      # Loop through each img element and click on it
      counter = 0
      for i in range(1,cows_count):
          self.random_sleep(1,2)
          img_elements = self.browser.find_element(By.XPATH,f"//img[contains(@src, 'cow.png') and @data-id='{i}']")
          img_elements.click()
          self.random_sleep(2,3)
          counter += 1
          self.browser.find_element(By.CLASS_NAME, "fa-heart").click()
          print(self.logTime() + f' : You have pet {counter} cow(s).')
          self.random_sleep(1,2)
          self.browser.find_elements(By.CLASS_NAME, "modal-button-bold")[0].click()
          print(self.logTime()+' : OK.')
          self.random_sleep(1, 2)
        
