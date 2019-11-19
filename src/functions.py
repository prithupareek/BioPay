# Prithu Pareek - Created 11/18/19
# Stores extra functions, to prevent cluttering of other files

from PIL import Image, ImageTk
import string
import math

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
                    'slash':'/', 'question':'?'
                }

    def __init__(self, x0, y0, x1, name, hidden=False):
        self.clicked = False
        self.outlineWidth = 1
        (self.x0, self.y0, self.x1, self.y1) = (x0, y0, x1, y0+40)
        self.name = self.inputText = name
        # self.maxInputLen = math.floor((self.x1-self.x0)/12.5)
        self.maxInputLen = 16
        self.hidden=hidden

    def mousePressed(self, event):
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            self.clicked = True
            self.outlineWidth = 3
            if self.inputText == self.name:
                self.inputText = ''
            
        else:
            self.clicked = False
            self.outlineWidth = 1
            if self.inputText == '':
                self.inputText = self.name
            
            
    def keyPressed(self, event):
        if self.clicked:

            key = event.keysym
            if key in InputBox.symbolDict:
                key = InputBox.symbolDict[key]

            if key == 'BackSpace':
                self.inputText = self.inputText[:-1]
            elif (key in string.ascii_letters or string.digits) and len(key)==1 and len(self.inputText)<self.maxInputLen:
                self.inputText += key

    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, 
                                width=self.outlineWidth)
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
        self.outlineWidth = 1

    def mousePressed(self, event):
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            self.clicked = True
            self.outlineWidth = 3

    def mouseReleased(self, event):
        if (self.x0 < event.x < self.x1 and
            self.y0 < event.y < self.y1):
            self.clicked = False
            self.outlineWidth = 1

    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill='#2178cf', width=self.outlineWidth)
        canvas.create_text((self.x1-self.x0)/2+self.x0, (self.y1-self.y0)/2+self.y0, text=self.name, font='Helvetica 32', fill='#FFFFFF')


