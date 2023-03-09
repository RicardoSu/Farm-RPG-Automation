import sys
import time
import random
import threading
import cv2 as cv
import mysecrets
from tkinter import *
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class farmBot:

  def __init__(self, browser, mysecrets):
      self.browser = browser
      self.mysecrets = mysecrets
      self.exitPlease = False

  def exitApp(self):
        print('exiting app')
        sys.exit()

  def logTime(self):
    return datetime.now().strftime("%H:%M:%S")

  #Pause the program for a random amount of time between min_time and max_time seconds in miliseconds.
  def random_sleep(self,min_time, max_time):
      time.sleep(random.uniform(min_time, max_time))

  def grindFarm2(self):
      print(self.logTime() + ' : Accessing farm.')
      farm = f"https://farmrpg.com/index.php#!/xfarm.php?id={mysecrets.farm_id}"
      self.random_sleep(2,3)
      self.browser.get(farm)
      self.random_sleep(3,4)
      try:
          # Harvest ready crops + sanity check for farm loaded.
          print(self.logTime() + ' : Harvesting all ready crops.')
          self.random_sleep(1,2)
          self.browser.find_element(By.CLASS_NAME, "harvestallbtn").click()
          print(self.logTime() + ' : Harvested all ready crops.')
          self.random_sleep(2,3)

          try:
              print(self.logTime() + ' : Selecting the first available seed')
              self.random_sleep(1,2)

              # Locate the select element
              select_element = self.browser.find_element(By.CLASS_NAME, 'seedid')
              select_element.click()
              self.random_sleep(1,2)

              # Select the second option
              # I could not select it manually so this is a fix
              for i in range(random.randint(7, 10)):
                  select_element.send_keys(Keys.UP)
                  time.sleep(random.uniform(0.1, 0.3))
                  
              select_element.send_keys(Keys.DOWN)
              time.sleep(random.uniform(0.5, 0.75))
              select_element.send_keys(Keys.ENTER)


              # If we have seeds, plant new crops
              print(self.logTime() + ' : Do we have seeds?')
              
              seedsAmt = int(self.browser.find_element(By.CLASS_NAME,'seedid').find_elements(By.TAG_NAME, 'option')[1].get_attribute('data-amt'))
              seedsName = self.browser.find_element(By.CLASS_NAME,'seedid').find_elements(By.TAG_NAME, 'option')[1].get_attribute('data-name')
              print(self.logTime() + ' : Yes. We have ' + str(seedsAmt) + ' ' + seedsName + '.')

              if seedsAmt > 0:
                  while True:
                      # Plant new crops
                      if seedsAmt > 0:
                          print(self.logTime() + ' : Planting new crops')
                          self.browser.find_element(By.CLASS_NAME, "plantallbtn").click()
                          self.random_sleep(2,3)
                          self.browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
                          self.random_sleep(1,2)
                          print(self.logTime() + ' : Waiting for crops to grow.')
                          self.random_sleep(120,150)
                          print(self.logTime() + ' : Restarting.')
                          self.grindFarm2()

          except Exception as e:
              print(f"Error: {e}")
              # If we don't have new seeds, go buy more.
              self.random_sleep(2,3)
              print(self.logTime() + ' : No more seeds remaining.')

              # Sell all unlocked crops
              self.sellUnlockedCrops()

              print(self.logTime() + ' : Lets go to buy seeds Farmer!')
              self.buySeeds()
      except:
          print(self.logTime() + ' : Accessing farm failed. Trying again in 2 seconds.')
          self.random_sleep(2,3)
          self.grindFarm2()

      try: 
          print(self.logTime() + ' : Accessing farm.')
          farm = f"https://farmrpg.com/index.php#!/xfarm.php?id={mysecrets.farm_id}"
          self.browser.get(farm)
          self.random_sleep(3,4)
          try: 
              seedsAmt = int(self.browser.find_element(By.CLASS_NAME,'seedid').find_elements(By.TAG_NAME, 'option')[1].get_attribute('data-amt'))
              if seedsAmt > 0:
                  while True: 
                      # Harvest ready crops 
                      print(self.logTime() + ' : Harvesting all ready crops.')
                      self.browser.find_element(By.CLASS_NAME, "harvestallbtn").click()
                      self.random_sleep(1,2) 
                      # Plant new crops 
                      if seedsAmt > 0: 
                          print(self.logTime() + ' : Planting new crops')
                          self.browser.find_element(By.CLASS_NAME, "plantallbtn").click()
                          self.random_sleep(2,3)
                          self.browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
                          self.random_sleep(1,2)
                          try:
                              seedsAmt = int(self.browser.find_element(By.CLASS_NAME,'seedid').find_elements(By.TAG_NAME, 'option')[1].get_attribute('data-amt'))
                              print(self.logTime() + ' : Seeds remaining: ' + str(seedsAmt))
                              print(self.logTime() + ' : Waiting for crops to finish.')
                              time.sleep(65)
                          except: 
                              print(self.logTime() + ' No seeds remaining. Buy more seeds.')
                              break
          except: 
              print(self.logTime() + ' : No seeds remaining. Buy more seeds.')
              self.buySeeds()
      except: 
          print(self.logTime() + ' : Accessing failed. Trying again in 2 seconds.')
          self.random_sleep(2,3)
          self.grindFarm2()



  def sellUnlockedCrops(self):
      self.random_sleep(1, 2)
      print(self.logTime() + " : Selling all the fully grown crops to ensure that we don't exceed the inventory limit.")
      self.random_sleep(1, 2)
      self.browser.find_element(By.CLASS_NAME, "sellallcropsbtn").click()
      print(self.logTime() + ' : Selling all unlocked crops.')
      self.random_sleep(1, 2)
      print(self.logTime()+' : Confirm.')
      self.browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
      self.random_sleep(1, 2)
      self.browser.find_elements(By.CLASS_NAME, "modal-button-bold")[0].click()
      print(self.logTime()+' : OK.')
      self.random_sleep(3, 4)



  def buySeeds(self):
    print(self.logTime() + ' : Going to the market to buy more needs.')
    market = "https://farmrpg.com/index.php#!/store.php" 
    try: 
      self.browser.get(market)
      self.random_sleep(2,3)

      seeds_dict = {
          0 : "Pepper",
          1 : "Carrot",
          2 : "Pea",
          3 : "Cucumber",
          4 : "Eggplant",
          5 : "Radish",
          6 : "Onion",
          7 : "Hops",
          8 : "Potato",
          9 : "Tomato",
          10 :"Leek",
          11 :"Watermelon",
          12 :"Corn",
          13 :"Cabbage",
          14 :"Pine",
          15 :"Pumpkin",
          16 :"Wheat",
          17 :"Mushroom",
          18 :"Broccoli",
          19 :"Cotton",
          20 :"Sunflower",
          21 :"Beet",
          22 :"Rice",
      }

      # Refer to chart above
      seed_type = 9

      print(self.logTime() + f" : Selection '{seeds_dict[seed_type][0]}' Seeds.")
      print(self.logTime() + ' : Selecting MAX for Seeds.')
      m = self.browser.find_elements(By.CLASS_NAME, 'maxqty')[seed_type]
      self.browser.execute_script("arguments[0].click();", m) 
      self.random_sleep(1,2)
      print(self.logTime() + f" : Buying '{seeds_dict[seed_type][0]}' Seeds.")
      b = self.browser.find_elements(By.CLASS_NAME, 'buybtn')[seed_type]
      self.browser.execute_script("arguments[0].click();", b) 
      self.random_sleep(1,2)
      print(self.logTime()+':  Confirm.')
      self.browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
      self.random_sleep(1,2)
      print(self.logTime()+' : OK.')
      self.browser.find_elements(By.CLASS_NAME, "modal-button")[2].click()
      self.random_sleep(1,2)

      return seeds_dict[seed_type][1]
    except: 
        print(self.logTime()+' : Market failed to load. Trying again in 2 seconds.')
        self.random_sleep(2,3)
        self.buySeeds()
        print(self.logTime()+' : Restart.') 
        self.grindFarm2()

  #Visit farm page, harvwest all crops, plant new crops

  def Farm_Check(self):
      farm = f"https://farmrpg.com/index.php#!/xfarm.php?id={mysecrets.farm_id}"
      self.browser.get(farm)
      time.sleep(1)
      try:
          self.browser.find_element(By.CLASS_NAME, "harvestallbtn").click()
          time.sleep(2)
          self.browser.find_element(By.CLASS_NAME, "plantallbtn").click()
          time.sleep(1)
          self.browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
      except:
          self.Farm_Check()

  def Sell(self): 
    market = "https://farmrpg.com/index.php#!/market.php"
    self.browser.get(market)
    time.sleep(2) 
    self.browser.find_element(By.CLASS_NAME, "sellallbtn").click()
    time.aleep(1)
    self.browser.find_element(By.CLASS_NAME, "actions-modal-button")[0].click()

  def Explore(self):
      zoneSelect = str(random.randint(6, 8))
      explore4 = "https://farmrpg.com/index.php#!/area.php?id="+zoneSelect
      print(self.logTime()+' : Entering zone '+zoneSelect +'.')
      self.browser.get(explore4)
      time.sleep(2)
      self.browser.get(explore4)
      time.sleep(2)
      counter = 0
      while True:
          try:
              print(self.logTime() + ' : Explore in zone. ' + zoneSelect + ' (' + str(counter) + '/50)')
              self.browser.find_element(By.ID, "exploreconsole").click()
              counter += 1
              time.sleep(1)
              if counter > 50:
                  print(self.logTime() + ' : Leaving zone ' + zoneSelect + '.')
                  self.Explore()
          except:
              self.Explore()

  def staminaChecker(self):
      stamina_script = """var staminaData = document.evaluate(\'//*[@id="stamina"]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null); 
                          var staminaValue = staminaData.singleNodeValue.textContent.trim(); 
                          return staminaValue;"""
      stamina_value = self.browser.execute_script(stamina_script)
      return stamina_value

  def eatApple(self):
    stamina = self.staminaChecker()
    if stamina == 0:
        try: 
          self.browser.find_element(By.ID, "apples").click()
          time.sleep(1)
          self.browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
          time.sleep(1)
        except:
          time.sleep(1)
          self.eatOJ()

  def eatOJ(self):
    stamina = self.staminaChecker()
    if stamina == 0:
        try: 
          self.browser.find_element(By.ID, "oj").click()
          time.sleep(1)
          self.browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
          time.sleep(1)
        except:
          time.sleep(1)
          self.eatLM() 

  def eatLM(self):
      stamina = self.staminaChecker()
      if stamina == 0:
        try: 
          self.browser.find_element(By.ID, "lm").click()
          time.sleep(1)
          self.browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
          time.sleep(1)
        except:
          finished = True

  def Fishing(self):
      pondSelect = str(random.randint(1, 8))
      pond = "https://farmrpg.com/index.php#!/fishing.php?id=" + pondSelect
      print(self.logTime() + ' : Entering pond ' + pondSelect + '.')
      self.browser.get(pond)
      time.sleep(2)
      self.browser.get(pond)
      time.sleep(2)
      try:
          worms = int(self.browser.find_element(By.CLASS_NAME, "col-45").find_element(By.TAG_NAME, 'strong').text)
          counter = 0
      except:
          self.Fishing()
      while worms > 0:
          print(self.logTime() + ' : Fishing in pond ' + pondSelect + ' (' + str(counter) + '/75)')
          self.Catch()
          counter += 1
          worms = int(self.browser.find_element(By.CLASS_NAME, "col-45").find_element(By.TAG_NAME, 'strong').text)
          if counter > 75:
              print(self.logTime() + ' : Leaving pond ' + pondSelect + '.')
              self.Fishing()
          if worms == 0:
              self.BuyWorms()

  def FishingHome(self):
      pond = "https://farmrpg.com/index.php#!/fishing.php?id=2"
      print(self.logTime() + ' : Entering pond ')
      self.browser.get(pond)
      time.sleep(2)
      self.browser.get(pond)
      time.sleep(2)
      try:
          worms = int(self.browser.find_element(By.CLASS_NAME, "col-45").
          find_element(By.TAG_NAME, 'strong').text)
          counter = 0
      except:
          self.FishingHome()
      while worms > 0:
          print(self.logTime() + ' : Fishing')
          self.Catch()
          counter += 1
          worms = int(self.browser.find_element(By.CLASS_NAME, "col-45").
          find_element(By.TAG_NAME, 'strong').text)
          if counter > 75:
              print(self.logTime() + ' : Refreshing pond.')
              self.FishingHome()
          if worms == 0:
              self.BuyWorms()

  def BuyWorms(self):
    print(self.logTime() + ' : Buying more worms.')
    market = "https://farmrpg.com/index.php#!/store.php"
    self.browser.get(market)
    time.sleep(1)
    try: 
        self.browser.find_elements(By.CLASS_NAME, "maxqty")[-1].click()
    except:
        self.browser.get(market)
    time.sleep(.5)
    s = self.browser.find_elements(By.CLASS_NAME, 'buybtn')[-1]
    self.browser.execute_script("arguments[0].click();", s)
    time.sleep(.5)
    self.browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
    time.sleep(.5)
    self.browser.find_elements(By.CLASS_NAME, "modal-button")[2].click()
    time.sleep(.5) 
    self.FishingHome()

  def Catch(self):
      fish = self.browser.find_elements(By.CLASS_NAME, "fishcell")
      catcher = self.browser.find_elements(By.CLASS_NAME, "fishcaught")
      for i in fish:
          try:
              i.click()
          except:
              pass
      try:
          time.sleep(0.5)
          catcher.click()
          time.sleep(1)
      except:
          pass

  def Crafting(self):
    workshop = "https://farmrpg.com/index.php#!/workshop.php"
    self.browser.get(workshop)
    time.sleep(2)
    craftable = self.browser.find_elements(By.CLASS_NAME, "btngreen")
    while len(craftable) > 0:
      craftable[0].click()
      time.sleep(1)
      self.browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
      craftable = self.browser.find_elements(By.CLASS_NAME, "btngreen")
      if len(craftable) == 0:
        break 