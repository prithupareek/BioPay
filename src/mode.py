# Prithu Pareek - Created 11/19/19
# Holds the mode superclass

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from functions import *
from sql import *
from userData import *
import cv2
import face_recognition
import numpy as np
import sha1

class Mode(object):
    def __init__(self): pass
    def timerFired(self, data): pass
    def keyPressed(self, event, data): pass
    def mousePressed(self, event, data): pass
    def mouseReleased(self, event, data): pass