import random
import pyautogui
import cv2 as cv
from time import time 
from time import sleep 
from time import ctime
from datetime import datetime
from WindowCapture import WindowCapture
from Vision import Vision
from tkinter import *
from selenium.webdriver.common.by import By


class FishingStaminaBot:
    
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
        zoneSelect = str(random.randint(1, 5))
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
                    farm_pond = "https://farmrpg.com/#!/fishing.php?id=2"
                    print(self.logTime()+' : Entering zone Farm Pond.')
                    self.PageNavigation(farm_pond)
                    self.main()

            except Exception as e:
                print(self.logTime() + f" : An error occurred:", e)
                farm_pond = "https://farmrpg.com/#!/fishing.php?id=2"
                print(self.logTime()+' : Entering zone Farm Pond.')
                self.PageNavigation(farm_pond)
                self.main()

    def exitApp(self):
        # If button pressed, destroy the window
        self.exitPlease = True
        
    def main(self):

        counter = 0
        farm_counter = 0
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
                farm_counter += 1
            
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

                self.browser.get(fish_lake)
                self.random_sleep(2, 2.5)

                
            # get an updated image of the game
            screenshot = self.wincap.get_screenshot()
            if(self.STATE == 'FISHING'):
                findFishingShadow = self.fishShadow.find(screenshot, 0.9, 'points')
                if(findFishingShadow.any()):
                    findShadowClickpoint = self.fishShadow.get_click_points(findFishingShadow)
                    # Prints (x,y) of the found shadow
                    print(self.logTime() + f" : Fish Shadow Location : {findShadowClickpoint}")
                    self.logFishFound()
                    sleep(.2)
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
