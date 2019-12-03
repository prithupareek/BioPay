# Prithu Pareek - Created 11/18/19
# Stores extra functions, to prevent cluttering of other files

from PIL import Image, ImageTk
import string
import math
import cv2
import random

# colors
MAIN_COLOR = '#2178cf'
ACCENT_COLOR = '#21cfcf'
ACCENT_COLOR_DARK = '#116969'
GRAY_COLOR = '#d8d8d8'
# From https://stackoverflow.com/questions/4969543/colour-chart-for-tkinter-and-tix, with modifications
COLORS = ['midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4']

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

    # event.keysm returns the name of the symbol, so this dictionary holds the conversions
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
        self.maxInputLen = 16
        self.hidden=hidden

    # if you click on the textBox, then make the outline thick and if you haven't typed, clear the text
    def mousePressed(self, event):
        # if you click on the box, it goes into active mode so the user knows what box they are typing in
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            self.clicked = True
            self.outlineWidth = 3
            self.outlineColor = MAIN_COLOR

            # makes the box empty when you click on it for the first time so you don't have to delete the filler text
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

            # translate symbol name into actual symbol
            if key in InputBox.symbolDict:
                key = InputBox.symbolDict[key]

            # lets you delete charecters
            if key == 'BackSpace':
                self.inputText = self.inputText[:-1]

            # regular letters
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

    # set self.clicked to true if the button is clicked, and turn the button darker to indicate to the user that it was clicked
    def mousePressed(self, event):
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            self.clicked = True
            self.fillColor = self.clickedColor

    # on mouserelase click is false again, and the color is normal
    def mouseReleased(self, event):
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            self.clicked = False
            self.fillColor = self.startColor

    # draw the button
    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.fillColor, width=self.outline, outline=GRAY_COLOR)
        canvas.create_text((self.x1-self.x0)/2+self.x0, (self.y1-self.y0)/2+self.y0, text=self.name, font='Helvetica 32', fill=self.textColor)

# Dark button inherits from button
class DarkButton(Button):
    pass

# inherits from button, same thing, but with different color scheme
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

    # changes the name and color based on the click
    # the name of the button is used to determine what state the button is in when the button is used in the app
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

# scroll button, used in the table class, different size/shape
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
        self.numRows = rows #num of visible rows
        self.rows = [] #holds each row
        self.name = name
        self.scroll = 0
        self.scrollUpButton = ScrollButton(x1+5, (self.y1-self.y0)//3+self.y0+30, name=u"\u25B2")
        self.scrollDownButton = ScrollButton(x1+5, 2*(self.y1-self.y0)//3 + self.y0+30, name=u"\u25BC")
        self.onScreen = [] #rows that are currently visible on screen

    def mousePressed(self, event):
        self.scrollUpButton.mousePressed(event)
        self.scrollDownButton.mousePressed(event)

        # self.scroll is used to control what is visible on screen
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

    def addRow(self, prodID, name, price, qty, mode):
          self.rows.insert(0, TableRow(self.x0, self.y0+30+60*len(self.rows), self.x1, name, price, mode, prodID, qty))

    def removeRow(self, row):
        self.rows.remove(row)

    # remove all rows from the table
    def clear(self):
        self.rows = []

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
    def __init__(self, x0, y0, x1, name, price, mode, prodID, qty):
        (self.x0, self.y0, self.x1, self.y1) = (x0, y0, x1, y0+60)
        self.name = name
        self.price = price
        self.mode = mode # add, remove, noButton
        self.prodId = prodID
        self.qty = qty
        if mode != 'noButton':
            if mode == 'Add':
                buttonText = '+'
            elif mode == 'Remove':
                buttonText = '-'
            self.button = DarkButton(2.6*(x1-x0)//3 + self.x0, y0+10, 2.8*(x1-x0)//3 + self.x0, buttonText)

    def updateYPos(self, newY0):
        self.y0 = newY0
        self.y1 = newY0 + 60
        if self.mode != 'noButton':
            self.button.y0 = newY0 + 10
            self.button.y1 = self.button.y0 + 40

    def mousePressed(self, event):
        if self.mode != 'noButton':
            self.button.mousePressed(event)

    def mouseReleased(self, event):
        if self.mode != 'noButton':
            self.button.mouseReleased(event)

    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline=GRAY_COLOR, width=1, fill='#FFFFFF')
        canvas.create_text(self.x0+25, (self.y1-self.y0)/2+self.y0, text=self.name, font='Helvetica 24', fill='#000000', anchor='w')
        canvas.create_text((self.x1-self.x0)//3 + self.x0 +25, (self.y1-self.y0)/2+self.y0, text="$"+str(self.price), font='Helvetica 24', fill='#000000', anchor='w')

        if not self.qty == -1:
            canvas.create_text(2*(self.x1-self.x0)//3 + self.x0, (self.y1-self.y0)/2+self.y0, text="Qty:"+str(self.qty), font='Helvetica 24', fill='#000000', anchor='w')
        if self.mode != 'noButton':
            self.button.draw(canvas)

# piechart class
class PieChart(object):
    def __init__(self, cx, cy, r, data):
        self.cx, self.cy = cx, cy
        self. r = r
        self.data = data
        self.xy = (cx - r, cy -r, cx + r, cy+r)
        self.colors = [COLORS[random.randint(0, len(COLORS))] for i in range(len(self.data))]
        print(self.data)


    def draw(self, canvas):        
        start = 0
        colorCounter = 0

        # create the arcs
        for item in self.data:
            extent = self.data[item]*360

            canvas.create_arc(self.xy, start=start, extent=extent, fill=self.colors[colorCounter])

            # create the text labels
            canvas.create_text(self.cx+(self.r+75)*math.cos(float(start+extent/2)*math.pi/180), 
                               self.cy+(self.r+75)*(-1)*math.sin(float(start+extent/2)*math.pi/180), text=item+" "+f"{self.data[item]*100}"[:5]+"%", anchor='c', font='Helvetica 16')

            colorCounter += 1
            start = start + extent

            

