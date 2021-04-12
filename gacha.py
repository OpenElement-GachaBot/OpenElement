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
seeds_template = cv2.imread("templates/seeds.png", cv2.IMREAD_COLOR)
access_inv_template = cv2.imread("templates/access_inventory_template.png")
seed_fruit_template = cv2.imread("templates/seed_fruit.png", cv2.IMREAD_COLOR)
tinto_template = cv2.imread("templates/tintoberry.png", cv2.IMREAD_COLOR)

lower_yellow = np.array([0, 128, 195])
upper_yellow = np.array([31, 255, 255])
hsv = cv2.cvtColor(seed_fruit_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
seed_fruit_template = cv2.bitwise_and(seed_fruit_template, seed_fruit_template, mask= mask)
seed_fruit_template = cv2.cvtColor(seed_fruit_template, cv2.COLOR_BGR2GRAY)

cv2.imwrite("seed_dump.png", seed_fruit_template)

lower_red = np.array([0,0,0])
upper_red = np.array([40,255,255])
hsv = cv2.cvtColor(seeds_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_red, upper_red)
seeds_template = cv2.bitwise_and(seeds_template, seeds_template, mask= mask)
seeds_template = cv2.cvtColor(seeds_template, cv2.COLOR_BGR2GRAY)

hsv = cv2.cvtColor(tinto_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_red, upper_red)
tinto_template = cv2.bitwise_and(tinto_template, tinto_template, mask= mask)
tinto_template = cv2.cvtColor(tinto_template, cv2.COLOR_BGR2GRAY)


lower_cyan = np.array([90,250,250])
upper_cyan = np.array([110,255,255])


ride_template = cv2.imread('templates/ride.png', cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(ride_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
masked_template = cv2.bitwise_and(ride_template, ride_template, mask= mask)
ride_gray_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)


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

def checkForSeedText():
    roi = screen.getScreen()[275:400,1000:1345]
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, lower_yellow, upper_yellow)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    cv2.imwrite("dump.png", masked_screen)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_screen, seed_fruit_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 15000000):
        return True
    return False


def checkForTintos():
    roi = screen.getScreen()[240:320,210:300]
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, lower_red, upper_red)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_screen, tinto_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 10000000):
        return True
    return False


def checkForRideText():
    roi = screen.getScreen()[0:1080,600:1300]
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, lower_cyan, upper_cyan)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_screen, ride_gray_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 14000000):
        return True
    return False

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

def checkWeGotSeeds():
    roi = screen.getScreen()[230:886,120:677]

    lower_red = np.array([0,0,0])
    upper_red = np.array([40,255,255])
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_red, upper_red)
    roi = cv2.bitwise_and(roi, roi, mask= mask)
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, seeds_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 24000000):
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




def loadTheGacha():
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
        if(ark.inventoryIsOpen() == False): #still can't open gacha, so return the seeds and return
            ark.lookUp()
            ark.depositOverhead()
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
        if(ark.inventoryIsOpen()): # if its open, we put in seeds, take a row back out and break the loop
            ark.transferAll("seed")
            time.sleep(0.5)
            ark.searchStructureStacks("seed")
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

def seedOnce():
    # hold down the e key
    time.sleep(0.5)
    pyautogui.keyDown('e')
    time.sleep(1.0)

    # if the option to seed is visible
    if(checkForSeedText()):
        # move mouse to that option and click it
        pyautogui.moveTo(971, 540, 0.1)
        pyautogui.moveTo(1209, 357, 0.1, pyautogui.easeInQuad)
        time.sleep(0.1)
        pyautogui.click();
        time.sleep(0.5)

    # release e key
    pyautogui.keyUp('e')

    # take all the seeds from the iguanodon
    if(ark.openInventory()):
        ark.takeAll("s")
        ark.takeStacks("berry", 1)
        time.sleep(0.5)
        ark.closeInventory()

def seed():
    if(ark.openInventory() == False):
        return

    ark.searchMyStacks("seed")

    count = 0
    while((checkWeGotSeeds() == False) and (count < 7)):
        count += 1
        ark.searchMyStacks("berry")
        time.sleep(0.5)
        ark.transferAll()
        time.sleep(1.0)
        ark.closeInventory()
        time.sleep(1.0)
        seedOnce()
        seedOnce()

        ark.lookUp()

        time.sleep(0.5)
        pyautogui.press('e')

        ark.closeInventory()
        time.sleep(0.5)

        for i in range(12):
            pyautogui.keyDown('down')
            time.sleep(0.1)
            pyautogui.keyUp('down')
            if(checkForRideText()):
                break

        if(ark.openInventory() == False):
            ark.lookUp()
            ark.lookUp()
            pyautogui.keyDown('down')
            time.sleep(0.4)
            pyautogui.keyUp('down')
            return

        ark.searchMyStacks("seed")

    ark.dropItems("seed")
    ark.takeAll()
    ark.closeInventory()

def turn(rh, delay=0.9):
    turnKey = 'left'
    if(rh):
        turnKey = 'right'

    pyautogui.keyDown(turnKey)
    time.sleep(delay)
    pyautogui.keyUp(turnKey)

# gets the berries from the feeding troughs
def getTheBerries(direction):
    # turn towards the troughs
    turn(direction)
    turn(direction, 0.5)

    # look down a bit
    pyautogui.keyDown('down')
    time.sleep(0.05)
    pyautogui.keyUp('down')

    hasBerries = False
    count = 0
    # tweak the direction of player until the 'press e to access inventory' text is fairly well centered on the screen
    while(checkInvAccessibleText() == False):
        if(count > 10):
            return False
        count += 1
        turn(direction, 0.05)

    # open the inventory
    if(ark.openInventory()):
        # take all the berries and check we have got berries
        ark.takeAll("berry")
        if(checkForTintos()):
            hasBerries = True
        ark.closeInventory()
    else:
        return False

    pyautogui.keyDown('up')
    time.sleep(0.35)
    pyautogui.keyUp('up')

    if(ark.openInventory()):
        ark.takeAll("berry")
        if(checkForTintos()):
            hasBerries = True
        ark.closeInventory()
    return hasBerries

def putTheBerriesBack(direction):
    turn(not direction, 0.5)

    pyautogui.keyDown('down')
    time.sleep(0.1)
    pyautogui.keyUp('down')

    count = 0
    while(checkInvAccessibleText() == False):
        if(count > 10):
            return False
        count += 1
        turn(not direction, 0.05)

    if(ark.openInventory()):
        ark.transferAll("berry")
        ark.closeInventory()

    pyautogui.keyDown('up')
    time.sleep(0.4)
    pyautogui.keyUp('up')

    if(ark.openInventory()):
        ark.transferAll("berry")
        ark.closeInventory()
    return True

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
print("Version 2.67")
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
    print("Do you wanna\n1: run the gacha bot\n2: run the seeder bot\n3: helper macros\n")
    val = input("")
    if(val == "1"):
        val = input("Do the seed dedis need to be refilled? y/n")

        print("Starting . . . ")
        print("8 seconds to alt tab back in")
        time.sleep(8)
        print("OK taking over controls")

        start = time.time()
        count = 0
        if(val.lower().startswith('y') == True):
            for i in beds["seedBeds"]:
                turnDirection = ((count %2) == 1)
                count += 1

                duration = time.time() - start
                if(duration > 1200):
                    start = time.time()
                    suicideBed = beds["suicideBed"]
                    ark.bedSpawn(suicideBed["name"], suicideBed["x"], suicideBed["y"])
                    time.sleep(15)

                ark.bedSpawn(i["name"], i["x"], i["y"])
                time.sleep(3.0)


                """
                1. find the troughs
                2. get the berries
                3. find iguanodon
                4. seed
                5. find the troughs again
                6. put berries back
                """
                if(getTheBerries(turnDirection) == False):
                    ark.accessBed()

                turn(turnDirection, 0.5)
                turnCount = 0
                attempts = 10
                while(turnCount < attempts):
                    if(checkForRideText()):
                        break
                    turn(turnDirection, 0.05)
                    turnCount += 1

                if(turnCount >= attempts):
                    turn(not turnDirection, 1.0)
                    pyautogui.keyDown('down')
                    time.sleep(0.35)
                    pyautogui.keyUp('down')
                    putTheBerriesBack(turnDirection)
                    ark.lookDown()
                    ark.accessBed()

                else:
                    ark.lookUp()
                    pyautogui.press('e')
                    for i in range(16):
                        pyautogui.keyDown('down')
                        time.sleep(0.05)
                        pyautogui.keyUp('down')
                        time.sleep(0.1)
                        if(checkForRideText()):
                            break

                    seed()
                    ark.lookDown()
                    ark.lookDown()
                    ark.lookUp()

                    putTheBerriesBack(turnDirection)
                    ark.accessBed()

            suicideBed = beds["suicideBed"]
            ark.bedSpawn(suicideBed["name"], suicideBed["x"], suicideBed["y"])
            time.sleep(15)
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
                loadTheGacha()
                ark.accessBed()
    elif(val == "2"):
        print("Enter bed name to start at or press enter to start at the beginning: ")
        startBedName = input("")
        print("Starting . . . ")
        print("8 seconds to alt tab back in")
        time.sleep(8)
        print("OK taking over controls")

        count = 0
        skipping = False
        if(startBedName != ""):
            skipping = True

        start = time.time()
        for i in beds["seedBeds"]:
            turnDirection = ((count %2) == 1)
            count += 1

            if(skipping):
                if(i["name"] == startBedName):
                    skipping = False
                else:
                    continue

            duration = time.time() - start
            if(duration > 1200):
                start = time.time()
                suicideBed = beds["suicideBed"]
                ark.bedSpawn(suicideBed["name"], suicideBed["x"], suicideBed["y"])
                time.sleep(15)

            ark.bedSpawn(i["name"], i["x"], i["y"])
            time.sleep(3.0)


            """
            1. find the troughs
            2. get the berries
            3. find iguanodon
            4. seed
            5. find the troughs again
            6. put berries back
            """
            if(getTheBerries(turnDirection) == False):
                ark.accessBed()

            turn(turnDirection, 0.5)
            turnCount = 0
            attempts = 10
            while(turnCount < attempts):
                if(checkForRideText()):
                    break
                turn(turnDirection, 0.05)
                turnCount += 1

            if(turnCount >= attempts):
                turn(not turnDirection, 1.0)
                pyautogui.keyDown('down')
                time.sleep(0.35)
                pyautogui.keyUp('down')
                putTheBerriesBack(turnDirection)
                ark.lookDown()
                ark.accessBed()

            else:
                ark.lookUp()
                pyautogui.press('e')
                for i in range(16):
                    pyautogui.keyDown('down')
                    time.sleep(0.05)
                    pyautogui.keyUp('down')
                    time.sleep(0.1)
                    if(checkForRideText()):
                        break

                seed()
                ark.lookDown()
                ark.lookDown()
                ark.lookUp()

                putTheBerriesBack(turnDirection)
                ark.accessBed()

    elif(val == "3"):
        print("Quick Handy Macros")
        print("F1 - seed once. Look at the iguanodon, make sure it has berries, make sure you have at least 2 stacks of berries")
        print("F2 - seed until the dedi is full. stand under seed dedi with iguanodon infront of you, load iguanodon with berries")
        print("F3 - start crafting an element dedi.")
        print("F4 - stop crafting element")

        listener = Listener(on_press=onPress, on_release=onRelease)
        listener.start()

        while(True):
            while(len(keyPresses) > 0):
                key = keyPresses.pop(0)
                if(key == Key.f1):
                    seedOnce()
                if(key == Key.f2):
                    seed()
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
        print("Make a proper selection you idiot. 1 2 or 3. PICK ONE FFS ITS NOT FUCKING HARD.")
