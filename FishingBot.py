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


class FishingBot:
    
    def __init__(self):

        
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
        time.sleep(random.uniform(min_time, max_time))

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


    def exitApp(self):
        # If button pressed, destroy the window
        self.exitPlease = True
        
    def main(self):  

        resetTimer = time()
        while(self.exitPlease == False):
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
                            pyautogui.click(clickTarget[0], clickTarget[1] - 50)
                            self.STATE = 'FISHING'

                if (time() - resetTimer > 15):
                    self.STATE = 'FISHING'
                    print("reset")
                        


            # # refreshWindowTimer 
            # if (time() - self.refreshWindowTimer > 1200): # EVERY 300 SECONDS REFRESH THE WINDOW, SELL ALL FISH, BUY BAIT
            #     self.refreshWindowTimer = time()
            #     sleep(3.5)
            #     pyautogui.click(1010, 80)
            #     print("Clicked at 1010, 80 on bookmark button")
            #     sleep(3.5)
            #     pyautogui.click(116, 180) # CLICK HOME
            #     sleep(2)
            #     pyautogui.click(400, 525) # CLICK GO TO TOWN [NORMAL 535, 430] [BANNER 400, 525]
            #     sleep(2)
            #     pyautogui.click(508, 318) # CLICK GO TO COUNTRY STORE
            #     sleep(2)
            #     scrollTimer = time()
            #     while(time() - scrollTimer < 7):
            #         pyautogui.scroll(-100) # SCROLL DOWN THE PAGE FOR 7 SECONDS
            #         sleep(.1)
            #     sleep(2)
            #     pyautogui.click(1478, 820) # CLICK BUY WORMS
            #     sleep(2)
            #     pyautogui.click(960, 965) # CLICK YES
            #     sleep(2)
            #     checkForPopup = self.noRoomForBait.find(screenshot, 0.9, 'points')
            #     if(checkForPopup.any()):
            #         print("No room for bait")
            #         pyautogui.click(966, 622) # CLICK OK
            #         sleep(2)
            #         pyautogui.click(116, 180) # CLICK HOME
            #         sleep(2)
            #         pyautogui.click(356, 592) # CLICK GO FISHING [NORMAL 502, 502] [BANNER 356, 592]
            #         sleep(2)
            #         pyautogui.click(573,533) # CLICK LAKE TEMPEST
            #         print("Clicked at 502, 502 to go fishing at LAKE TEMPEST")
            #         sleep(2)
            #         # write to a new text file and log current time+"going fishing"
            #         self.logFishing()
            #         sleep(2)
            #     else:
            #         pyautogui.click(966, 564) # CLICK GO TO FARM
            #         sleep(2)
            #         pyautogui.click(116, 180) # CLICK HOME
            #         sleep(2)
            #         pyautogui.click(356, 592) # CLICK GO FISHING [NORMAL 502, 502] [BANNER 356, 592]
            #         sleep(2)
            #         pyautogui.click(573,533) # CLICK LAKE TEMPEST
            #         print("Clicked at 502, 502 to go fishing at LAKE TEMPEST")
            #         sleep(2)
            #         # write to a new text file and log current time+"going fishing"
            #         self.logFishing()
            #         sleep(2)


            # debug the loop rate
            print('FPS {}'.format(1 / (time() - self.loop_time)))
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
