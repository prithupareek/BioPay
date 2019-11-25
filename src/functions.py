# Prithu Pareek - Created 11/18/19
# Stores extra functions, to prevent cluttering of other files

from PIL import Image, ImageTk
import string
import math
import cv2

# colors
MAIN_COLOR = '#2178cf'
ACCENT_COLOR = '#21cfcf'
ACCENT_COLOR_DARK = '#116969'
GRAY_COLOR = '#d8d8d8'

# From https://github.com/VasuAgrawal/112-opencv-tutorial/blob/master/opencvTkinterTemplate.py
# with slight modifications
def opencvToTk(frame):
    """Convert an opencv image to a tkinter image, to display in canvas."""
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_image)
    tk_image = ImageTk.PhotoImage(image=pil_img)
    return tk_image

# From cmu_112_graphics.py version 0.8.5
def scaleImage(image, scale, antialias=False):
        # antialiasing is higher-quality but slower
        resample = Image.ANTIALIAS if antialias else Image.NEAREST
        return image.resize((round(image.width*scale), round(image.height*scale)), 
                            resample=resample)

# class to draw input textboxes in tkinter
# need to add ability to have alphanumeric charecters as well
class InputBox(object):

    symbolDict = {
                    'exclam': '!', 'at': '@', 'numbersign':'#', 'dollar':'$', 'percent':'%', 'asciicircum':'^', 'ampersand':'&',
                    'asterisk':'*', 'parenleft':'(', 'parenright':')', 'minus':'-', 'underscore':'_', 'plus':'+', 'equal':'=',
                    'quoteleft':'`', 'asciitilde':'~', 'bracketleft':'[', 'bracketright':']', 'braceleft':'{', 'braceright':'}',
                    'backslash':'\\', 'bar':'|', 'semicolon':';', 'colon':':', 'less':'<', 'greater':'>', 'comma':',', 'period':'.',
                    'slash':'/', 'question':'?', 'space':' '
                }

    def __init__(self, x0, y0, x1, name, hidden=False):
        self.clicked = False
        self.outlineWidth = 1
        self.outlineColor = '#000000'
        (self.x0, self.y0, self.x1, self.y1) = (x0, y0, x1, y0+40)
        self.name = self.inputText = name
        # self.maxInputLen = math.floor((self.x1-self.x0)/12.5)
        self.maxInputLen = 16
        self.hidden=hidden

    # if you click on the textBox, then make the outline thick and if you haven't typed, clear the text
    def mousePressed(self, event):
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            self.clicked = True
            self.outlineWidth = 3
            self.outlineColor = MAIN_COLOR
            if self.inputText == self.name:
                self.inputText = ''
        # reset if click off the box
        else:
            self.clicked = False
            self.outlineWidth = 1
            self.outlineColor = '#000000'
            if self.inputText == '':
                self.inputText = self.name
            
    # typing inside the box
    def keyPressed(self, event):
        if self.clicked:

            key = event.keysym
            if key in InputBox.symbolDict:
                key = InputBox.symbolDict[key]

            if key == 'BackSpace':
                self.inputText = self.inputText[:-1]
            elif (key in string.ascii_letters or string.digits) and len(key)==1 and len(self.inputText)<self.maxInputLen:
                self.inputText += key

    # drawing the box and text inside it, if password, then draw * not actual text
    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, 
                                width=self.outlineWidth, outline=self.outlineColor)
        if self.hidden:
            displayText = '*'*len(self.inputText)
        else:
            displayText = self.inputText
        canvas.create_text(self.x0+5, self.y1, text=displayText,
                           anchor='sw', font='Helvetica 32')

# button class
class Button(object):
    def __init__(self, x0, y0, x1, name):
        (self.x0, self.y0, self.x1, self.y1) = (x0, y0, x1, y0+40)
        self.name = name
        self.clicked = False
        self.startColor = ACCENT_COLOR
        self.clickedColor = ACCENT_COLOR_DARK
        self.fillColor = self.startColor
        self.textColor = '#FFFFFF'
        self.outline = 0

    def mousePressed(self, event):
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            self.clicked = True
            self.fillColor = self.clickedColor

    def mouseReleased(self, event):
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            self.clicked = False
            self.fillColor = self.startColor

    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.fillColor, width=self.outline, outline=GRAY_COLOR)
        canvas.create_text((self.x1-self.x0)/2+self.x0, (self.y1-self.y0)/2+self.y0, text=self.name, font='Helvetica 32', fill=self.textColor)

class DarkButton(Button):
    pass

class LightButton(Button):
    def __init__(self, x0, y0, x1, name):
        super().__init__(x0, y0, x1, name)
        self.startColor = '#FFFFFF'
        self.clickedColor = GRAY_COLOR
        self.fillColor = self.startColor
        self.textColor = ACCENT_COLOR
        self.outline = 1

# Toggle Button, toggle between two options (name 1 and name 2)
class ToggleButton(Button):
    def __init__(self, x0, y0, x1, name, alternativeName):
        super().__init__(x0, y0, x1, name)
        self.name1 = name
        self.name2 = alternativeName

    def mousePressed(self, event):
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            if not self.clicked:
                self.clicked = True
                self.fillColor = self.clickedColor
                self.name = self.name2
            else:
                self.clicked = False
                self.fillColor = self.startColor
                self.name = self.name1

    def mouseReleased(self, event):
        pass

# scroll button
class ScrollButton(Button):
    def __init__(self, x0, y0, name):
        super().__init__(x0, y0, x0+10, name)
        (self.x0, self.y0, self.x1, self.y1) = (x0, y0, x0+30, y0+30)

    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.fillColor, width=self.outline, outline=GRAY_COLOR)
        canvas.create_text((self.x1-self.x0)/2+self.x0, (self.y1-self.y0)/2+self.y0, text=self.name, font='16', fill=self.textColor)


# Table class
class Table(object):
    def __init__(self, x0, y0, x1, rows, name):
        (self.x0, self.y0, self.x1, self.y1) = (x0, y0, x1, y0+60*rows)
        self.numRows = rows
        self.rows = []
        self.name = name
        self.scroll = 0
        self.scrollUpButton = ScrollButton(x1+5, (self.y1-self.y0)//3+self.y0+30, name=u"\u25B2")
        self.scrollDownButton = ScrollButton(x1+5, 2*(self.y1-self.y0)//3 + self.y0+30, name=u"\u25BC")
        self.onScreen = []

    def mousePressed(self, event):
        self.scrollUpButton.mousePressed(event)
        self.scrollDownButton.mousePressed(event)

        if self.scrollUpButton.clicked and self.scroll+self.numRows < len(self.rows):
            self.scroll += 1
        elif self.scrollDownButton.clicked and self.scroll > 0:
            self.scroll -= 1

        # keep loop on screen
        start = self.scroll
        end = min((self.scroll+self.numRows),len(self.rows))

        # loop through the buttons on screen
        for i in range(start, end):
            self.rows[i].mousePressed(event)

    def mouseReleased(self, event):
        self.scrollUpButton.mouseReleased(event)
        self.scrollDownButton.mouseReleased(event)

        # keep loop on screen
        start = self.scroll
        end = min((self.scroll+self.numRows),len(self.rows))

        # loop through the buttons on screen
        for i in range(start, end):
            self.rows[i].mouseReleased(event)

    def addRow(self, prodID, name, price, mode):
          self.rows.insert(0, TableRow(self.x0, self.y0+30+60*len(self.rows), self.x1, name, price, mode, prodID))

    def removeRow(self, row):
        self.rows.remove(row)

    def draw(self, canvas):
        canvas.create_text(self.x0, self.y0, text=self.name, font='Helvetica 24', anchor='nw')
        canvas.create_rectangle(self.x0, self.y0+30, self.x1, self.y1+30, outline=GRAY_COLOR, width=1, fill='#FFFFFF')

        # draw the rows, but allow for scrolling, if not empty
        if len(self.rows) > 0:

            start = self.scroll
            end = min((self.scroll+self.numRows),len(self.rows))

            self.onScreen = [self.rows[i] for i in range(start, end)]

            for i in range(start, end):
                self.rows[i].updateYPos((i-self.scroll)*60 + self.y0 + 30)

                self.rows[i].draw(canvas)

        # draw the scroll buttons
        self.scrollUpButton.draw(canvas)
        self.scrollDownButton.draw(canvas)

# TableRow class
class TableRow(object):
    def __init__(self, x0, y0, x1, name, price, mode, prodID):
        (self.x0, self.y0, self.x1, self.y1) = (x0, y0, x1, y0+60)
        self.name = name
        self.price = price
        self.mode = mode
        self.prodId = prodID
        self.button = DarkButton(2*(x1-x0)//3 + self.x0, y0+10, 2*(x1-x0)//3 + self.x0+175, mode)

    def updateYPos(self, newY0):
        self.y0 = newY0
        self.y1 = newY0 + 60
        self.button.y0 = newY0 + 10
        self.button.y1 = self.button.y0 + 40

    def mousePressed(self, event):
        self.button.mousePressed(event)

    def mouseReleased(self, event):
        self.button.mouseReleased(event)

    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline=GRAY_COLOR, width=1, fill='#FFFFFF')
        canvas.create_text(self.x0+25, (self.y1-self.y0)/2+self.y0, text=self.name, font='Helvetica 24', fill='#000000', anchor='w')
        canvas.create_text((self.x1-self.x0)//3 + self.x0 +25, (self.y1-self.y0)/2+self.y0, text="$"+str(self.price), font='Helvetica 24', fill='#000000', anchor='w')
        self.button.draw(canvas)


