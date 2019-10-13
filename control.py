import pyautogui
print(pyautogui.size())

class Control:
    HORIZONTAL_SENSITIVITY = .80
    VERTICAL_SENSITIVITY = .80

    def __init__(self):
        print("started")

    def moveMouse(self, x, y, curX=None, curY=None):
        multiplier = 1
        if (curX != None and abs(curX - x) > 20):

            multiplier /= self.HORIZONTAL_SENSITIVITY
        if (curY != None and abs(curY - y) > 20):
            multiplier /= self.VERTICAL_SENSITIVITY
        print("moveTo: x: " + str(x) + ", y: " + str(y) + "\n")
        pyautogui.moveTo(x, y, duration=0.125 * multiplier)

    def clickMouse(self, x, y):
        pyautogui.click(x, y)

# c = Control()
#
# c.moveMouse(100,100)
# c.clickMouse(100,100)
# c.moveMouse(900,900)