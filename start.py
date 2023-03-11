import sys
import time
import random
import threading
import cv2 as cv
import mysecrets
from tkinter import *
from SignIn import SignIn
from FarmBot import FarmBot
from datetime import datetime
from selenium import webdriver
from FishingBot import FishingBot
from PettingCows import PettingCows
from WindowCapture import WindowCapture
from PettingChickens import PettingChickens
from selenium.webdriver.common.by import By
from FishingStaminaBot import FishingStaminaBot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from FishingStaminaFarmBot import FishingStaminaFarmBot


browser = webdriver.Chrome()
# set initial window size to 1280x720
browser.set_window_size(1280, 720)

SignIn = SignIn(browser)
FishingBot = FishingBot(browser)
PettingCows = PettingCows(browser)
FarmBot = FarmBot(browser,mysecrets)
PettingChickens = PettingChickens(browser)
FishingStaminaBot = FishingStaminaBot(browser)
FishingStaminaFarmBot = FishingStaminaFarmBot(browser)

#Logs in using credentials
SignIn.main()

def runGrindFarm2():
    FarmBot.grindFarm2()

def runPettingChickensBot():
    PettingChickens.exitPlease = False
    PettingChickens.main()

def runPettingCowsBot():
    PettingCows.exitPlease = False
    PettingCows.main()

def runFishingBot():
    FishingBot.exitPlease = False
    FishingBot.main()

def runFishingBot_background():
    f = threading.Thread(target=runFishingBot)
    f.start()

def stopFishingBot():
    FishingBot.exitApp()
    print('exiting fishing bot')

def runFishingStaminaBot():
    FishingStaminaBot.exitPlease = False
    FishingStaminaBot.main()

def runFishingStaminaBot_background():
    f = threading.Thread(target=FishingStaminaBot)
    f.start()

def stopFishingStaminaBot():
    FishingStaminaBot.exitApp()
    print('exiting Fishing Stamina Bot bot')

def runFishingStaminaFarmBot():
    FishingStaminaFarmBot.exitPlease = False
    FishingStaminaFarmBot.main()

def runFishingStaminaFarmBot_background():
    f = threading.Thread(target=FishingStaminaFarmBot)
    f.start()

def stopFishingStaminaFarmBot():
    FishingStaminaFarmBot.exitApp()
    print('exiting Fishing Stamina Farm Bot bot')

def runSignIn():
    SignIn.exitPlease = False
    SignIn.main()

def runPond(id):
    SignIn.exitPlease = False
    SignIn.farm_pond(id)

def stopSignIn():
    print('exiting SignIn bot')
    SignIn.exitApp()
    


root = Tk()
# create geometry
root.title("FarmRPG_Bot")
root.geometry("500x400+805+400")
# Make the window stay above all other windows
root.attributes('-topmost',True)


# Creating a Label Widget
myLabel1 = Label(root, text="Farm Bot v2")
myLabel2 = Button(root, command=runGrindFarm2, text="Farm!")
myLabel3 = Label(root, text="Pet Animals")
myLabel4 = Button(root, command=runPettingChickensBot, text="Chicken(s)!")
myLabel6 = Button(root, command=runPettingCowsBot, text="Cows(s)!")
myLabel7 = Label(root, text="Start Fishing!")
myLabel8 = Button(root, command=runFishingBot_background, text="Click Me!")
myLabel9 = Button(root, command=stopFishingBot, text="Exit!")
myLabel10 = Label(root, text="Start Fishing & Exploring!")
myLabel11 = Button(root, command=runFishingStaminaBot, text="Click Me!")
myLabel12 = Button(root, command=stopFishingStaminaBot, text="Exit!")
myLabel13 = Label(root, text="Start Fishing, Exploring & Farm!")
myLabel14 = Button(root, command=runFishingStaminaFarmBot, text="Click Me!")
myLabel15 = Button(root, command=stopFishingStaminaFarmBot, text="Exit!")
myLabel16 = Label(root, text="Start Website!")
myLabel17 = Button(root, command=runSignIn, text="Click Me!")
myLabel18 = Button(root, command=stopSignIn, text="Exit!")
myLabel19 = Label(root, text="Go to Pond!")
myLabel20 = Button(root, text="Farm Pond", command=lambda: runPond(id=2))
myLabel21 = Button(root, text="Small Pond", command=lambda: runPond(id=1))
myLabel22 = Button(root, text="Forest Pond", command=lambda: runPond(id=3))
myLabel23 = Button(root, text="Lake Tempest", command=lambda: runPond(id=4))
myLabel24 = Button(root, text="Small Island", command=lambda: runPond(id=5))
myLabel25 = Button(root, text="Crystal River", command=lambda: runPond(id=6))
myLabel26 = Button(root, text="Emerald Beach", command=lambda: runPond(id=7))

# Grid Positions:
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=0, column=1)

myLabel3.grid(row=1, column=0)
myLabel4.grid(row=1, column=1)
myLabel6.grid(row=1, column=2)

myLabel7.grid(row=4, column=0)
myLabel8.grid(row=4, column=1)
myLabel9.grid(row=4, column=2)

myLabel10.grid(row=5, column=0)
myLabel11.grid(row=5, column=1)
myLabel12.grid(row=5, column=2)

myLabel13.grid(row=6, column=0)
myLabel14.grid(row=6, column=1)
myLabel15.grid(row=6, column=2)

myLabel16.grid(row=7, column=0)
myLabel17.grid(row=7, column=1)
myLabel18.grid(row=7, column=2)

myLabel19.grid(row=8, column=0)
myLabel20.grid(row=8, column=1)
myLabel21.grid(row=8, column=2)
myLabel22.grid(row=8, column=3)
myLabel23.grid(row=8, column=4)
myLabel24.grid(row=9, column=1)
myLabel25.grid(row=9, column=2)
myLabel26.grid(row=9, column=3)


root.mainloop()