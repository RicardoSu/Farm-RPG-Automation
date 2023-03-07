import time
import random
import mysecrets
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select



browser = webdriver.Chrome()
login = 'https://farmrpg.com/index.php#!/login.php'
explore = 'https://farmrpg.com/index.php#!/explore.php'


def logTime():
  return datetime.now().strftime("%H:%M:%S")

#Pause the program for a random amount of time between min_time and max_time seconds in miliseconds.
def random_sleep(min_time, max_time):
    time.sleep(random.uniform(min_time, max_time))


# Login to the game
browser.get(login)
random_sleep(1,2)
browser.find_element(By.NAME, "username").send_keys(mysecrets.username)
random_sleep(0.1,0.3)
browser.find_element(By.NAME, "password").send_keys(mysecrets.password)
random_sleep(0.1,0.3)
browser.find_element(By.CSS_SELECTOR, 'input#login_sub.button.btngreen').click()

home = "https://farmrpg.com/index.php#!/login.php"

def grindFarm2():
    print(logTime() + ' : Accessing farm.')
    farm = f"https://farmrpg.com/index.php#!/xfarm.php?id={mysecrets.farm_id}"
    random_sleep(2,3)
    browser.get(farm)
    random_sleep(3,4)
    try:
        # Harvest ready crops + sanity check for farm loaded.
        print(logTime() + ' : Harvesting all ready crops.')
        random_sleep(1,2)
        browser.find_element(By.CLASS_NAME, "harvestallbtn").click()
        print(logTime() + ' : Harvested all ready crops.')
        random_sleep(2,3)

        try:
            print(logTime() + ' : Selecting the first available seed')
            random_sleep(1,2)

            # Locate the select element
            select_element = browser.find_element(By.CLASS_NAME, 'seedid')
            select_element.click()
            random_sleep(1,2)

            # Select the second option
            # I could not select it manually so this is a fix
            for i in range(random.randint(7, 10)):
                select_element.send_keys(Keys.UP)
                time.sleep(random.uniform(0.1, 0.3))
                
            select_element.send_keys(Keys.DOWN)
            time.sleep(random.uniform(0.5, 0.75))
            select_element.send_keys(Keys.ENTER)


            # If we have seeds, plant new crops
            print(logTime() + ' : Do we have seeds?')
             
            seedsAmt = int(browser.find_element(By.CLASS_NAME,'seedid').find_elements(By.TAG_NAME, 'option')[1].get_attribute('data-amt'))
            seedsName = browser.find_element(By.CLASS_NAME,'seedid').find_elements(By.TAG_NAME, 'option')[1].get_attribute('data-name')
            print(logTime() + ' : Yes. We have ' + str(seedsAmt) + ' ' + seedsName + '.')

            if seedsAmt > 0:
                while True:
                    # Plant new crops
                    if seedsAmt > 0:
                        print(logTime() + ' : Planting new crops')
                        browser.find_element(By.CLASS_NAME, "plantallbtn").click()
                        random_sleep(2,3)
                        browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
                        random_sleep(1,2)
                        print(logTime() + ' : Waiting for crops to grow.')
                        random_sleep(120,150)
                        print(logTime() + ' : Restarting.')
                        grindFarm2()

        except Exception as e:
            print(f"Error: {e}")
            # If we don't have new seeds, go buy more.
            random_sleep(2,3)
            print(logTime() + ' : No more seeds remaining.')

            # Sell all unlocked crops
            sellUnlockedCrops()

            print(logTime() + ' : Lets go to buy seeds Farmer!')
            buySeeds()
    except:
        print(logTime() + ' : Accessing farm failed. Trying again in 2 seconds.')
        random_sleep(2,3)
        grindFarm2()

    try: 
        print(logTime() + ' : Accessing farm.')
        farm = f"https://farmrpg.com/index.php#!/xfarm.php?id={mysecrets.farm_id}"
        browser.get(farm)
        random_sleep(3,4)
        try: 
            seedsAmt = int(browser.find_element(By.CLASS_NAME,'seedid').find_elements(By.TAG_NAME, 'option')[1].get_attribute('data-amt'))
            if seedsAmt > 0:
                while True: 
                    # Harvest ready crops 
                    print(logTime() + ' : Harvesting all ready crops.')
                    browser.find_element(By.CLASS_NAME, "harvestallbtn").click()
                    random_sleep(1,2) 
                    # Plant new crops 
                    if seedsAmt > 0: 
                        print(logTime() + ' : Planting new crops')
                        browser.find_element(By.CLASS_NAME, "plantallbtn").click()
                        random_sleep(2,3)
                        browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
                        random_sleep(1,2)
                        try:
                            seedsAmt = int(browser.find_element(By.CLASS_NAME,'seedid').find_elements(By.TAG_NAME, 'option')[1].get_attribute('data-amt'))
                            print(logTime() + ' : Seeds remaining: ' + str(seedsAmt))
                            print(logTime() + ' : Waiting for crops to finish.')
                            time.sleep(65)
                        except: 
                            print(logTime() + ' No seeds remaining. Buy more seeds.')
                            break
        except: 
            print(logTime() + ' : No seeds remaining. Buy more seeds.')
            buySeeds()
    except: 
        print(logTime() + ' : Accessing failed. Trying again in 2 seconds.')
        random_sleep(2,3)
        grindFarm2()



def sellUnlockedCrops():
    random_sleep(1, 2)
    print(logTime() + " : Selling all the fully grown crops to ensure that we don't exceed the inventory limit.")
    random_sleep(1, 2)
    browser.find_element(By.CLASS_NAME, "sellallcropsbtn").click()
    print(logTime() + ' : Selling all unlocked crops.')
    random_sleep(1, 2)
    print(logTime()+' : Confirm.')
    browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
    random_sleep(1, 2)
    browser.find_elements(By.CLASS_NAME, "modal-button-bold")[0].click()
    print(logTime()+' : OK.')
    random_sleep(3, 4)



def buySeeds():
  print(logTime() + ' : Going to the market to buy more needs.')
  market = "https://farmrpg.com/index.php#!/store.php" 
  try: 
    browser.get(market)
    random_sleep(2,3)

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

    print(logTime() + f" : Selection '{seeds_dict[seed_type][0]}' Seeds.")
    print(logTime() + ' : Selecting MAX for Seeds.')
    m = browser.find_elements(By.CLASS_NAME, 'maxqty')[seed_type]
    browser.execute_script("arguments[0].click();", m) 
    random_sleep(1,2)
    print(logTime() + f" : Buying '{seeds_dict[seed_type][0]}' Seeds.")
    b = browser.find_elements(By.CLASS_NAME, 'buybtn')[seed_type]
    browser.execute_script("arguments[0].click();", b) 
    random_sleep(1,2)
    print(logTime()+':  Confirm.')
    browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
    random_sleep(1,2)
    print(logTime()+' : OK.')
    browser.find_elements(By.CLASS_NAME, "modal-button")[2].click()
    random_sleep(1,2)

    return seeds_dict[seed_type][1]
  except: 
      print(logTime()+' : Market failed to load. Trying again in 2 seconds.')
      random_sleep(2,3)
      buySeeds()
      print(logTime()+' : Restart.') 
      grindFarm2()

#Visit farm page, harvwest all crops, plant new crops

def Farm_Check():
    farm = f"https://farmrpg.com/index.php#!/xfarm.php?id={mysecrets.farm_id}"
    browser.get(farm)
    time.sleep(1)
    try:
        browser.find_element(By.CLASS_NAME, "harvestallbtn").click()
        time.sleep(2)
        browser.find_element(By.CLASS_NAME, "plantallbtn").click()
        time.sleep(1)
        browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
    except:
        Farm_Check()

def Sell(): 
  market = "https://farmrpg.com/index.php#!/market.php"
  browser.get(market)
  time.sleep(2) 
  browser.find_element(By.CLASS_NAME, "sellallbtn").click()
  time.aleep(1)
  browser.find_element(By.CLASS_NAME, "actions-modal-button")[0].click()

def Explore():
    zoneSelect = str(random.randint(6, 8))
    explore4 = "https://farmrpg.com/index.php#!/area.php?id="+zoneSelect
    print(logTime()+' : Entering zone '+zoneSelect +'.')
    browser.get(explore4)
    time.sleep(2)
    browser.get(explore4)
    time.sleep(2)
    counter = 0
    while True:
        try:
            print(logTime() + ' : Explore in zone. ' + zoneSelect + ' (' + str(counter) + '/50)')
            browser.find_element(By.ID, "exploreconsole").click()
            counter += 1
            time.sleep(1)
            if counter > 50:
                print(logTime() + ' : Leaving zone ' + zoneSelect + '.')
                Explore()
        except:
            Explore()

def staminaChecker():
    stamina_script = 'var staminaData = document.evaluate(\'//*[@id="stamina"]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null); var staminaValue = staminaData.singleNodeValue.textContent.trim(); return staminaValue;'
    stamina_value = browser.execute_script(stamina_script)
    return stamina_value

def eatApple():
   stamina = staminaChecker()
   if stamina == 0:
      try: 
        browser.find_element(By.ID, "apples").click()
        time.sleep(1)
        browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
        time.sleep(1)
      except:
         time.sleep(1)
         eatOJ()

def eatOJ():
   stamina = staminaChecker()
   if stamina == 0:
      try: 
        browser.find_element(By.ID, "oj").click()
        time.sleep(1)
        browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
        time.sleep(1)
      except:
         time.sleep(1)
         eatLM() 

def eatLM():
    stamina = staminaChecker()
    if stamina == 0:
      try: 
        browser.find_element(By.ID, "lm").click()
        time.sleep(1)
        browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
        time.sleep(1)
      except:
         finished = True

def Fishing():
    pondSelect = str(random.randint(1, 8))
    pond = "https://farmrpg.com/index.php#!/fishing.php?id=" + pondSelect
    print(logTime() + ' : Entering pond ' + pondSelect + '.')
    browser.get(pond)
    time.sleep(2)
    browser.get(pond)
    time.sleep(2)
    try:
        worms = int(browser.find_element(By.CLASS_NAME, "col-45").find_element(By.TAG_NAME, 'strong').text)
        counter = 0
    except:
        Fishing()
    while worms > 0:
        print(logTime() + ' : Fishing in pond ' + pondSelect + ' (' + str(counter) + '/75)')
        Catch()
        counter += 1
        worms = int(browser.find_element(By.CLASS_NAME, "col-45").find_element(By.TAG_NAME, 'strong').text)
        if counter > 75:
            print(logTime() + ' : Leaving pond ' + pondSelect + '.')
            Fishing()
        if worms == 0:
            BuyWorms()

def FishingHome():
    pond = "https://farmrpg.com/index.php#!/fishing.php?id=2"
    print(logTime() + ' : Entering pond ')
    browser.get(pond)
    time.sleep(2)
    browser.get(pond)
    time.sleep(2)
    try:
        worms = int(browser.find_element(By.CLASS_NAME, "col-45").
        find_element(By.TAG_NAME, 'strong').text)
        counter = 0
    except:
        FishingHome()
    while worms > 0:
        print(logTime() + ' : Fishing')
        Catch()
        counter += 1
        worms = int(browser.find_element(By.CLASS_NAME, "col-45").
        find_element(By.TAG_NAME, 'strong').text)
        if counter > 75:
            print(logTime() + ' : Refreshing pond.')
            FishingHome()
        if worms == 0:
            BuyWorms()

def BuyWorms():
  print(logTime() + ' : Buying more worms.')
  market = "https://farmrpg.com/index.php#!/store.php"
  browser.get(market)
  time.sleep(1)
  try: 
      browser.find_elements(By.CLASS_NAME, "maxqty")[-1].click()
  except:
      browser.get(market)
  time.sleep(.5)
  s = browser.find_elements(By.CLASS_NAME, 'buybtn')[-1]
  browser.execute_script("arguments[0].click();", s)
  time.sleep(.5)
  browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
  time.sleep(.5)
  browser.find_elements(By.CLASS_NAME, "modal-button")[2].click()
  time.sleep(.5) 
  FishingHome()

def Catch():
    fish = browser.find_elements(By.CLASS_NAME, "fishcell")
    catcher = browser.find_elements(By.CLASS_NAME, "fishcaught")
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

def Crafting():
  workshop = "https://farmrpg.com/index.php#!/workshop.php"
  browser.get(workshop)
  time.sleep(2)
  craftable = browser.find_elements(By.CLASS_NAME, "btngreen")
  while len(craftable) > 0:
    craftable[0].click()
    time.sleep(1)
    browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
    craftable = browser.find_elements(By.CLASS_NAME, "btngreen")
    if len(craftable) == 0:
       break 


def PetChicken():
    random_sleep(1,2)
    coop = f"https://farmrpg.com/index.php#!/coop.php?id={mysecrets.farm_id}"
    browser.get(coop)
    random_sleep(2,3)

    coop = f"https://farmrpg.com/index.php#!/coop.php?id={mysecrets.farm_id}"
    browser.get(coop)
    random_sleep(2,3)

    # Find all the img elements with the specified attributes
    all_chickens = browser.find_elements(By.CSS_SELECTOR,'[data-id]')
    # print(elements)
    chickens_count = len(all_chickens)

    print(logTime() + f' : You have {chickens_count-1} chicken(s) to pet.')

    # Loop through each img element and click on it
    counter = 0
    for i in range(1,chickens_count):
        random_sleep(1,2)
        img_elements = browser.find_element(By.XPATH,f"//img[contains(@src, 'chicken.png') and @data-id='{i}']")
        img_elements.click()
        random_sleep(2,3)
        counter += 1
        browser.find_element(By.CLASS_NAME, "fa-heart").click()
        print(logTime() + f' : You have pet {counter} chicken(s).')
        random_sleep(1,2)
        browser.find_elements(By.CLASS_NAME, "modal-button-bold")[0].click()
        print(logTime()+' : OK.')
        random_sleep(1, 2)
