import time
import pyautogui
import screen
import cv2
import numpy as np
import json
from pynput.keyboard import Key, Listener
import ark

crystal_template = cv2.imread("templates/gacha_crystal.png", cv2.IMREAD_GRAYSCALE)
broken_whip_template = cv2.imread("templates/broken_whip.png", cv2.IMREAD_GRAYSCALE)
added_template = cv2.imread("templates/added_template.png", cv2.IMREAD_GRAYSCALE)
owlshit_template = cv2.imread("templates/owlshit.png", cv2.IMREAD_GRAYSCALE)
tooltips_template = cv2.imread("templates/tool_tips_enabled.png", cv2.IMREAD_GRAYSCALE)
access_inv_template = cv2.imread("templates/access_inventory_template.png")
lower_cyan = np.array([90,250,250])
upper_cyan = np.array([110,255,255])


hsv = cv2.cvtColor(access_inv_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
masked_template = cv2.bitwise_and(access_inv_template, access_inv_template, mask= mask)
access_inv_gray_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)


location = ""


def disableToolTips():
    roi = screen.getScreen()[164:210,623:668]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crystal_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 4000000):
        pyautogui.press('g')


def checkInvAccessibleText():
    roi = screen.getScreen()[0:1080,600:1300]
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, lower_cyan, upper_cyan)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_screen, access_inv_gray_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 25000000):
        return True
    return False


def checkWeGotRowOfCrystals():
    roi = screen.getScreen()[230:330,585:670]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crystal_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 9000000):
        return True
    return False

def checkWeGotCrystals():
    roi = screen.getScreen()[230:330,120:210]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crystal_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 10000000):
        return True
    return False


def waitForAddedGraphic():
    counter = 0
    while(counter < 10):
        roi = screen.getScreen()[1030:1070, 37:142]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(gray_roi, added_template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if(max_val > 3000000):
            return True

        time.sleep(0.1)
        counter += 1
    return False

def gotOwlShit():
    roi = screen.getScreen()[790:880,1710:1800]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_roi, owlshit_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 4000000):
        return True
    return False

def gotNoOwlShit():
    roi = screen.getScreen()[330:410,1240:1330]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_roi, owlshit_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 4000000):
        return False
    return True

def clickPattern():
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(1.0)

def whipCrackPattern():
    pyautogui.press('1')

    pyautogui.keyDown("right")
    time.sleep(1.0)
    pyautogui.keyUp("right")
    clickPattern()

    pyautogui.keyDown("right")
    time.sleep(0.5)
    pyautogui.keyUp("right")
    clickPattern()

    pyautogui.keyDown("right")
    time.sleep(0.5)
    pyautogui.keyUp("right")
    clickPattern()

    pyautogui.keyDown("right")
    time.sleep(0.5)
    pyautogui.keyUp("right")
    clickPattern()

    pyautogui.keyDown("right")
    time.sleep(1.5)
    pyautogui.keyUp("right")
    pyautogui.press('1')


def whipTheCrystals():
    ark.openInventory()

    time.sleep(1)
    ark.takeAll("broken")
    time.sleep(1)

    #drag a whip from the vault to the first slot on the hot bar
    ark.searchStructureStacks("whip")
    pyautogui.moveTo(1295, 283);
    pyautogui.dragTo(690, 1050, 0.5, button='left')
    waitForAddedGraphic()

    time.sleep(0.5)
    ark.closeInventory()

    whipCrackPattern()

    while(ark.inventoryIsOpen() == False):
        pyautogui.keyDown("left")
        time.sleep(0.2)
        pyautogui.keyUp("left")
        pyautogui.press('f')
        time.sleep(2.0)


    disableToolTips()
    time.sleep(0.5)
    pyautogui.moveTo(690, 1050)
    pyautogui.click()
    pyautogui.press('t')
    time.sleep(0.5)

    pyautogui.moveTo(167, 185)
    pyautogui.click()
    pyautogui.typewrite("gacha", interval=0.02)

    count = 0
    time.sleep(0.2)

    pyautogui.moveTo(167, 280, 0.1)
    pyautogui.click()
    time.sleep(1.0)

    while(checkWeGotRowOfCrystals()):
        for i in range(6):
            pyautogui.moveTo(167+(i*95), 280, 0.1)
            pyautogui.click()
            pyautogui.press('e')

        time.sleep(0.8)
        count += 6

    pyautogui.moveTo(165, 280)
    pyautogui.click()
    while(checkWeGotCrystals()):
        pyautogui.press('e')
        time.sleep(0.8)
        count += 1
        if(count > 300):
            break

    ark.transferAll("whip")
    time.sleep(0.5)
    ark.dropItems("chitin")
    ark.dropItems("prim")

    ark.closeInventory()
    ark.lookUp()

    # double press e because sometimes the first press picks up crystals instead of depositing element
    pyautogui.press('e')
    time.sleep(0.5)
    pyautogui.press('e')
    time.sleep(0.5)

    ark.lookDown()

    for i in range(5):
        pyautogui.press('f')
        time.sleep(2.0)
        if(ark.inventoryIsOpen() == True):
            time.sleep(0.5)
            pyautogui.moveTo(690, 1050)
            pyautogui.click()
            pyautogui.press('t')
            time.sleep(0.5)

            ark.transferAll("")
            time.sleep(2.0)
            ark.closeInventory()
            break

        pyautogui.keyDown('down')
        time.sleep(0.1)
        pyautogui.keyUp('down')




def loadTheGacha(food):
    # crouch and open gacha inventory
    time.sleep(0.5)
    pyautogui.press('f')
    time.sleep(1.5)
    if(ark.inventoryIsOpen() == False): #if gacha inventory isn't open, look down a little and try again
        pyautogui.keyDown("down")
        time.sleep(0.1)
        pyautogui.keyUp("down")

        time.sleep(0.5)
        pyautogui.press('f')
        time.sleep(1.5)
        if(ark.inventoryIsOpen() == False): #still can't open gacha, so post error and give up
            return

    # remove excess owl shit
    ark.searchStructureStacks("owl")
    if(gotOwlShit()):
        ark.takeAll("owl") #take all the owl shit from the gacha
        time.sleep(0.5)
        ark.tTransferTo(3)

        ark.dropItems("owl") #drop the rest of the shit

    ark.closeInventory()

    #look up to the seed dedi
    ark.lookUp()

    #take all from seed dedi
    ark.openInventory()
    ark.takeAll()
    time.sleep(0.5)
    ark.closeInventory()

    #look back at the gacha
    ark.lookDown()

    #open gacha inventory
    pyautogui.press('f')
    time.sleep(2.0)
    for i in range(5): # loop 5 times, so we try a few times to open gacha inventory
        if(ark.inventoryIsOpen()): # if its open, we put in food, take a row back out and break the loop
            ark.transferAll(food)
            time.sleep(0.5)
            ark.searchStructureStacks(food)
            ark.tTransferFrom(1)

            ark.closeInventory()
            break
        pyautogui.keyDown("down") # else we look down a little and try again
        time.sleep(0.2)
        pyautogui.keyUp("down")
        pyautogui.press('f')
        time.sleep(2.0)

    # look back up at the dedi
    ark.lookUp()
    time.sleep(1.0)
    pyautogui.press('e') # put the seeds into the dedi
    time.sleep(1.0)

    ark.lookDown()
    ark.lookDown()

    
def craftElement():
    ark.takeAll("")
    time.sleep(0.2)
    pyautogui.moveTo(235, 298)
    time.sleep(0.2)
    pyautogui.press('a')
    time.sleep(0.2)

keyPresses = []

def onPress(key):
    global keyPresses
    keyPresses.append(key)


def onRelease(key):
    pass


print("Shazza's Amazing Totally Awesome Gacha Bot")
print("its so op omg")
print("Version 2.83")
print("\n\n")

beds = []

with open('beds.json') as json_file:
    data = json.load(json_file)
    count = 0
    print("Locations:")
    for i in data["locations"]:
        print("    " + str(count) + " - " + i["name"])
        count += 1

    val = input("Enter your location (0 - " + str(len(data["locations"])-1) + "): ")

    beds = data["locations"][int(val)]
    

for i in beds["crystalBeds"]:
    if(i.get("x") is None):
        i["x"] = beds["default_x"]
    if(i.get("y") is None):
        i["y"] = beds["default_y"]

for i in beds["seedBeds"]:
    if(i.get("x") is None):
        i["x"] = beds["default_x"]
    if(i.get("y") is None):
        i["y"] = beds["default_y"]



lapCounter = 0

ark.setParams(1.45, 1.45, 10)

def whipCrystals():
    global beds
    for i in beds["crystalBeds"]:
        ark.bedSpawn(i["name"], i["x"], i["y"])
        whipTheCrystals()
        ark.accessBed()

while(True):
    print("Do you wanna\n1: run the gacha bot\n2: helper macros\n")
    val = input("")
    if(val == "1"):

        print("Starting . . . ")
        print("8 seconds to alt tab back in")
        time.sleep(8)
        print("OK taking over controls")

        start = time.time()
        count = 0

        #start = time.time()
        start = 0
        count = 0

        while(True):
            #start = time.time()
            for i in beds["seedBeds"]:
                duration = time.time() - start
                if(duration > 720):
                    start = time.time()
                    whipCrystals()
                    count += 1
                    if((count%3) == 0):
                        suicideBed = beds["suicideBed"]
                        ark.bedSpawn(suicideBed["name"], suicideBed["x"], suicideBed["y"])
                    time.sleep(15)

                ark.bedSpawn(i["name"], i["x"], i["y"])
                loadTheGacha(beds["food"])
                ark.accessBed()
    
    elif(val == "2"):
        print("Quick Handy Macros")
        print("F3 - start crafting an element dedi.")
        print("F4 - stop crafting element")

        listener = Listener(on_press=onPress, on_release=onRelease)
        listener.start()

        while(True):
            while(len(keyPresses) > 0):
                key = keyPresses.pop(0)
                if(key == Key.f3):
                    ark.searchMyStacks("element")
                    run = True
                    while(run):
                        craftElement()
                        while(len(keyPresses) > 0):
                            if(keyPresses.pop(0) == Key.f4):
                                run = False
                                break


                time.sleep(0.01)

    else:
        print("Make a proper selection you idiot. 1 or 2. PICK ONE FFS ITS NOT FUCKING HARD.")
