import time
import pyautogui
import screen
import cv2
import numpy as np

inventory_template = cv2.imread("templates/inventory_template.png", cv2.IMREAD_GRAYSCALE)
inventory_template = cv2.Canny(inventory_template, 100, 200)

img = cv2.imread("templates/bed_button_corner.png", cv2.IMREAD_GRAYSCALE)
bed_button_edge = cv2.Canny(img,100,200)

lookUpDelay = 3
lookDownDelay = 1.75

setFps = 25
firstRun = True

def limitFps():
    global setFps
    pyautogui.press("tab")
    time.sleep(0.2)
    pyautogui.typewrite("t.maxfps " + str(setFps), interval=0.02)
    pyautogui.press("enter")

def setGamma():
    pyautogui.press("tab")
    time.sleep(0.2)
    pyautogui.typewrite("gamma 5", interval=0.02)
    pyautogui.press("enter")


def setParams(up, down, fps):
    global lookUpDelay
    global lookDownDelay
    global setFps
    lookUpDelay = up
    lookDownDelay = down
    setFps = fps


def lookUp():
    global lookUpDelay
    pyautogui.keyDown('up')
    time.sleep(lookUpDelay)
    pyautogui.keyUp('up')

def lookDown():
    global lookDownDelay
    pyautogui.keyDown('down')
    time.sleep(lookDownDelay)
    pyautogui.keyUp('down')

def enterBedName(name):
    pyautogui.moveTo(336, 986, duration=0.1)
    pyautogui.click()
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.press('backspace')
    pyautogui.typewrite(name, interval=0.05)
    time.sleep(0.5)

def checkBedButtonEdge():
    img = screen.getGrayScreen()[950:1100,580:620]
    img = cv2.Canny(img, 100, 200)
    res = cv2.matchTemplate(img, bed_button_edge, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(max_val)
    if(max_val > 2500000):
        return True
    return False


def bedSpawn(bedName, x, y):
    global firstRun
    time.sleep(1.5)
    enterBedName(bedName)
    time.sleep(0.25)
    pyautogui.moveTo(x, y)
    time.sleep(0.25)
    pyautogui.click()
    time.sleep(0.25)
    if(checkBedButtonEdge):
        pyautogui.moveTo(755, 983)
        time.sleep(0.25)
        pyautogui.click()
        time.sleep(12)
        pyautogui.press('c')
        if(firstRun == True):
            firstRun = False
            limitFps()
            setGamma()
        return True
    else:
        return False


def inventoryIsOpen():# {{{
    img = screen.getGrayScreen()
    img = cv2.Canny(img, 100, 200)
    res = cv2.matchTemplate(img, inventory_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 40000000):
        return True
    return False

def closeInventory():# {{{
    while(inventoryIsOpen() == True):
        pyautogui.moveTo(1816, 37)
        pyautogui.click()
        time.sleep(2.0)
        if(inventoryIsOpen() == False):
            return

def craft(item, timesToPressA):
    searchStructureStacks(item)
    pyautogui.moveTo(1290, 280)
    pyautogui.click()
    for i in range(0, timesToPressA):
        pyautogui.press('a')
        time.sleep(0.25)

def searchMyStacks(thing):# {{{
    pyautogui.moveTo(144, 191)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    time.sleep(0.2)
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.typewrite(thing, interval=0.02)
    time.sleep(0.5)


def searchStructureStacks(thing):# {{{
    pyautogui.moveTo(1322, 191)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    time.sleep(0.2)
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.typewrite(thing, interval=0.02)
    time.sleep(0.5)
# }}}
def takeStacks(thing, count):# {{{
    searchStructureStacks(thing)
    pyautogui.moveTo(1287, 290)
    pyautogui.click()
    for i in range(count):
        pyautogui.press('t')
        time.sleep(1)
# }}}
def takeAll(thing = ""):
    if(thing != ""):
        time.sleep(0.5)
        pyautogui.moveTo(1285, 180)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        pyautogui.typewrite(thing, interval=0.01)
    time.sleep(0.5)
    pyautogui.moveTo(1424, 190)
    pyautogui.click()
    time.sleep(0.5)

def transferAll(thing = ""):# {{{
    if(thing != ""):
        pyautogui.moveTo(198, 191)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        pyautogui.typewrite(thing, interval=0.005)
        time.sleep(0.5)
    pyautogui.moveTo(351, 186)
    pyautogui.click()
    time.sleep(0.5)

def transferStacks(thing, count):# {{{
    pyautogui.moveTo(198, 191)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.typewrite(thing, interval=0.005)
    time.sleep(0.5)
    counter = 0
    pyautogui.moveTo(170, 280)
    pyautogui.click()
    time.sleep(1.0)
    while(counter < count):
        pyautogui.press('t')
        time.sleep(0.5)
        counter += 1

def openInventory():
    pyautogui.press('f')
    time.sleep(2.0)
    count = 0
    while((inventoryIsOpen() == False) and (count < 6)):
        count += 1
        pyautogui.press('f')
        time.sleep(2.0)
        if(getBedScreenCoords() != None):
            pyautogui.press('esc')
            time.sleep(2.0)
    if(count >= 6):
        return False
    return True

def tTransferTo(nRows):
    time.sleep(0.5)
    pyautogui.moveTo(167, 280, 0.1)
    pyautogui.click()
    for j in range(nRows): #transfer a few rows back to the gacha
        for i in range(6):
            pyautogui.moveTo(167+(i*95), 280, 0.1)
            pyautogui.press('t')

def tTransferFrom(nRows):
    pyautogui.moveTo(1288, 280, 0.1)
    pyautogui.click()
    for j in range(nRows):
        for i in range(6):
            pyautogui.moveTo(1288+(i*95), 280, 0.1)
            pyautogui.press('t')

def getBedScreenCoords():
    roi = screen.getScreen()

    lower_blue = np.array([90,200,200])
    upper_blue = np.array([100,255,255])


    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(roi, roi, mask= mask)
    gray_roi = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)

    bed_template = cv2.imread('templates/bed_icon_template.png', cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(bed_template, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    masked_template = cv2.bitwise_and(bed_template, bed_template, mask= mask)
    bed_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)


    res = cv2.matchTemplate(gray_roi, bed_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 8000000):
        return (max_loc[0]+14, max_loc[1]+14)
    return None

def dropItems(thing):
    pyautogui.moveTo(198, 191)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.typewrite(thing, interval=0.02)
    time.sleep(0.5)
    pyautogui.moveTo(412, 190)
    pyautogui.click()


def accessBed():
    while(getBedScreenCoords() == None):
        lookDown()
        pyautogui.press('e')
        time.sleep(1.5)
        if(inventoryIsOpen()):
            closeInventory()

def takeAllOverhead():
    lookUp()
    openInventory()
    takeAll()
    closeInventory()
    lookDown()

def depositOverhead():
    lookUp()
    pyautogui.press('e')
    lookDown()


