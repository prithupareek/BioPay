# Prithu Pareek - Created 11/19/19
# Holds the mode superclass

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from functions import *

class Mode(object):
    def __init__(self): pass
    def timerFired(self, data): pass
    def keyPressed(self, event, data): pass
    def mousePressed(self, event, data): pass
    def drawTextBox(self, canvas, data): pass