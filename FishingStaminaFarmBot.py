import random
import cv2 as cv
import pyautogui
import mysecrets
from tkinter import *
from Vision import Vision
from datetime import datetime
from time import sleep, time, ctime
from WindowCapture import WindowCapture
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class FishingStaminaFarmBot:
    
    def __init__(self,browser):
        self.browser = browser
        self.exitPlease = False
        # initialize the WindowCapture class
        self.wincap = WindowCapture()
        # initialize the Vision class
        self.fishShadow = Vision('assets/fishShadow.jpg')
        self.fishingClickTarget = Vision('assets/fishingClickTarget.jpg')
        self.noRoomForBait = Vision('assets/noRoomForBait.jpg')
        self.refreshWindowTimer = time()
        self.loop_time = time()
        self.STATE = 'FISHING'

    #Pause the program for a random amount of time between min_time and max_time seconds in miliseconds.
    def random_sleep(self,min_time, max_time):
        sleep(random.uniform(min_time, max_time))

    def logTime(self):
        return datetime.now().strftime("%H:%M:%S")

    def logFishing(self):
        # log current time+ "going fishing"
        print(self.logTime() + ' : Going fishing at LAKE TEMPEST.')

    def logFishFound(self):
        # prints current time + "fish found"
        print(self.logTime() + ' : Fish found at LAKE TEMPEST')

    def logClickOnFish(self):
        print(self.logTime() + ' : Clicking on fish at LAKE TEMPEST')
    
    def wormsCounter(self):
        worms_value = self.browser.execute_script("""
            const divElement = document.querySelector('.col-45 strong');
            const numberValue = parseInt(divElement.textContent);
            return numberValue;
        """)
        return int(worms_value)


    def BuyWorms(self):
        print(self.logTime() + ' : Buying more worms.')
        market = "https://farmrpg.com/index.php#!/store.php"
        self.browser.get(market)
        self.random_sleep(2,3)
        try: 
            self.browser.find_elements(By.CLASS_NAME, "maxqty")[-1].click()
        except:
            self.browser.get(market)
        self.random_sleep(0.5,1)
        s = self.browser.find_elements(By.CLASS_NAME, 'buybtn')[-1]
        self.browser.execute_script("arguments[0].click();", s)
        self.random_sleep(0.5,1)
        self.browser.find_element(By.CLASS_NAME, "actions-modal-button").click()
        self.random_sleep(0.5,1)
        self.browser.find_elements(By.CLASS_NAME, "modal-button")[2].click()
        self.random_sleep(0.5,1)

    def sellUnlockedFish(self):
        self.random_sleep(1, 2)
        print(self.logTime() + " : Selling all the unlocked fish to ensure that we don't exceed the inventory limit.")
        self.random_sleep(1, 2)
        self.browser.find_element(By.CLASS_NAME, "sellallfishbtn").click()
        print(self.logTime() + ' : Selling all unlocked fish.')
        self.random_sleep(1, 2)
        print(self.logTime()+' : Confirm.')
        self.browser.find_elements(By.CLASS_NAME, "actions-modal-button")[0].click()
        self.random_sleep(1, 2)
        self.browser.find_elements(By.CLASS_NAME, "modal-button-bold")[0].click()
        print(self.logTime()+' : COMPLETED!.')
        self.random_sleep(3, 4)

    def staminaChecker(self):
        stamina_script = """var staminaData = document.evaluate(\'//*[@id="stamina"]\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null); 
                            var staminaValue = staminaData.singleNodeValue.textContent.trim(); 
                            return staminaValue;"""
        stamina_value = self.browser.execute_script(stamina_script)
        return int(stamina_value)


    def PageNavigation(self,page_link):
        self.browser.get(page_link)
        self.random_sleep(2, 2.5)

        self.browser.get(page_link)
        self.random_sleep(2, 2.5)

            

    def Explore(self):
        zoneSelect = str(random.randint(1, 7))
        explore_link = "https://farmrpg.com/index.php#!/area.php?id="+zoneSelect
        print(self.logTime()+' : Entering zone '+zoneSelect +'.')

        self.PageNavigation(explore_link)

        counter = self.staminaChecker()

        while counter > 1:
            try:
                print(self.logTime() + f' : You have {self.staminaChecker()} points of Stamina')
                self.browser.find_element(By.ID, "exploreconsole").click()
                self.random_sleep(0.1, 0.2)
                if self.staminaChecker() < 2:
                    print(self.logTime() + ' : Leaving zone ' + zoneSelect + '.')
                    self.grindFarm3()
                    # farm_pond = "https://farmrpg.com/#!/fishing.php?id=2"
                    # print(self.logTime()+' : Entering zone Farm Pond.')
                    # self.PageNavigation(farm_pond)
                    # self.main()

            except Exception as e:
                print(self.logTime() + f" : An error occurred:", e)
                print(self.logTime() + ' : Leaving zone ' + zoneSelect + '.')
                self.grindFarm3()
                # farm_pond = "https://farmrpg.com/#!/fishing.php?id=2"
                # print(self.logTime()+' : Entering zone Farm Pond.')
                # self.PageNavigation(farm_pond)
                # self.main()


    def grindFarm3(self):

        print(self.logTime() + ' : Accessing farm.')
        farm = f"https://farmrpg.com/index.php#!/xfarm.php?id={mysecrets.farm_id}"
        self.browser.get(farm)
        self.random_sleep(2,3)
        self.browser.refresh()
        self.random_sleep(2,3)
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
                    self.random_sleep(0.1,0.3)
                    
                select_element.send_keys(Keys.DOWN)
                self.random_sleep(0.5,0.75)
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
                            print(self.logTime() + ' : Lets go Fish while we wait for crops to grow.')
                            farm_pond = "https://farmrpg.com/#!/fishing.php?id=2"
                            print(self.logTime()+' : Entering zone Farm Pond.')
                            self.PageNavigation(farm_pond)
                            self.main()

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
            self.grindFarm3()

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
            self.random_sleep(1,2)
            self.buySeeds()
            print(self.logTime()+' : Restart.') 
            self.grindFarm3()

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
        self.random_sleep(1, 2)

    def exitApp(self):
        # If button pressed, destroy the window
        self.exitPlease = True
        
    def main(self):
        print(self.logTime() + f" : Welcome to FishingStaminaFarmBot")

        counter = 0
        resetTimer = time()
        while(self.exitPlease == False):
            
            fish_to_fill_stamina = 20
            
            if counter >= 20:
                self.Explore()

                fish_lake = f"https://farmrpg.com/#!/fishing.php?id=2"
                self.browser.get(fish_lake)
                self.random_sleep(2,3)

                fish_lake = f"https://farmrpg.com/#!/fishing.php?id=2"
                self.browser.get(fish_lake)
                self.random_sleep(2,3)

                counter = 0
 
            
            if self.wormsCounter() <= 1:

                print(self.logTime() + f" : You have {self.wormsCounter()} worm(s)")

                self.random_sleep(1,2)

                self.sellUnlockedFish()
                self.random_sleep(3,4)

                self.BuyWorms()
                self.random_sleep(2,3)

                fish_lake = f"https://farmrpg.com/#!/fishing.php?id=2"
                self.browser.get(fish_lake)
                self.random_sleep(2,3)
                self.browser.refresh()
                self.random_sleep(2,3)

                
            # get an updated image of the game
            screenshot = self.wincap.get_screenshot()
            if(self.STATE == 'FISHING'):
                findFishingShadow = self.fishShadow.find(screenshot, 0.9, 'points')
                if(findFishingShadow.any()):
                    findShadowClickpoint = self.fishShadow.get_click_points(findFishingShadow)
                    # Prints (x,y) of the found shadow
                    print(self.logTime() + f" : Fish Shadow Location : {findShadowClickpoint}")
                    self.logFishFound()
                    sleep(0.2)
                    for clickpoint in findShadowClickpoint:
                        pyautogui.click(clickpoint[0], clickpoint[1])
                        self.logClickOnFish()
                        self.STATE = 'FISHING_CLICK'
                        
            else:
                screenshot = self.wincap.get_screenshot()
                findFishingClickTarget = self.fishingClickTarget.find(screenshot, 0.9, 'points')
                if(findFishingClickTarget.any()):
                    sleep(0.6)
                    findClickpoint = self.fishingClickTarget.get_click_points(findFishingClickTarget)
                    #Prints (x,y) of the found fishing target
                    print(self.logTime() + f" : Blue Circle Location : {findClickpoint}")
                    tryingTimer = time()
                    
                    while(time() - tryingTimer < 2):
                        for clickTarget in findClickpoint:
                            # pyautogui.click(clickTarget[0], (clickTarget[1]))
                            # Manual calibration clickTarget[1] - 55 
                            pyautogui.click(clickTarget[0], clickTarget[1] - 55 )
                            self.STATE = 'FISHING'
                    counter += 1
                    print(self.logTime() + f" : You caught {counter}/{fish_to_fill_stamina} fishes ")

                if (time() - resetTimer > 15):
                    self.STATE = 'FISHING'
                    print(self.logTime() + " : RESET")
                        


            # debug the loop rate
            print(self.logTime() + ' : FPS {}'.format(1 / (time() - self.loop_time)))
            self.loop_time = time()

            # press 'q' with the output window focused to exit.
            # waits 1 ms every loop to process key presses
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
            if self.exitPlease == True:
                cv.destroyAllWindows()
                break

        print('Done.')
