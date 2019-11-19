# Prithu Pareek - Created 11/18/19
# BioPay Main Project File

# module imports
import time
import sys
from tkinter import *
import tkinter as tk
# import numpy as np
import cv2
from PIL import Image, ImageTk
import string

# importing the other python files
from functions import *
from splashScreenMode import *
from loginMode import *
from customerPortalMode import *
from merchantPortalMode import *

class App(object):
    # __init__ and appsStarted get called once when app is called
    def __init__(self, width, height):
        self.run(width, height)
        self.data = None

    def appStarted(self, data):
        self.data = data
        # Initialize the webcams
        # camera = cv2.VideoCapture(data.camera_index)
        # self.data.camera = camera
        # self.data.cameraOn = True
        self.data.splashScreenMode = SplashScreenMode(data)
        self.data.loginMode = LoginMode(data)

        self.data.activeMode = self.data.splashScreenMode

    def keyPressed(self, event, data):
        self.data.activeMode.keyPressed(event, data)

    def timerFired(self, data):
        self.data.activeMode.timerFired(data)

    def mousePressed(self, event, data):
        self.data.activeMode.mousePressed(event, data)

    def mouseReleased(self, event, data):
        self.data.activeMode.mouseReleased(event, data)

    def drawTextBox(self, canvas, data):
        self.data.activeMode.drawTextBox(canvas, data)

    # From https://github.com/VasuAgrawal/112-opencv-tutorial/blob/master/opencvTkinterTemplate.py
    # with slight modifications
    def opencvToTk(self, frame):
        """Convert an opencv image to a tkinter image, to display in canvas."""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_image)
        tk_image = ImageTk.PhotoImage(image=pil_img)
        return tk_image

    # From https://github.com/VasuAgrawal/112-opencv-tutorial/blob/master/opencvTkinterTemplate.py
    # with slight modifications
    def drawCamera(self, canvas, data):
        data.tk_image = self.opencvToTk(data.frame)
        canvas.create_image(data.width / 2, data.height / 2, image=data.tk_image)

    def redrawAll(self, canvas, data):
        # self.drawCamera(canvas, data)
        self.data.activeMode.redrawAll(canvas, data)



    ####################################
    # GRAPHICS CODE RUN FUNCTION
    # From https://github.com/VasuAgrawal/112-opencv-tutorial/blob/master/opencvTkinterTemplate.py
    # with modifications
    ####################################
    def run(self, width=300, height=300):

        class Struct(object): pass
        data = Struct()
        data.width = width
        data.height = height
        data.camera_index = 0
        data.cameraOn = False

        data.timer_delay = 100 # ms
        data.redraw_delay = 50 # ms

        # Make tkinter window and canvas
        data.root = Tk()
        canvas = Canvas(data.root, width=data.width, height=data.height)
        canvas.pack()

        # prevent the window from being resizeable
        data.root.resizable(False, False)

        self.appStarted(data)

        # Basic bindings. Note that only timer events will redraw.
        data.root.bind("<Button-1>", lambda event: self.mousePressed(event, data))
        data.root.bind("<Key>", lambda event: self.keyPressed(event, data))
        data.root.bind("<B1-ButtonRelease>", lambda event: self.mouseReleased(event, data))

        # Timer fired needs a wrapper. This is for periodic events.
        def timerFiredWrapper(data):
            # Ensuring that the code runs at roughly the right periodicity
            start = time.time()
            self.timerFired(data)
            end = time.time()
            diff_ms = (end - start) * 1000
            delay = int(max(data.timer_delay - diff_ms, 0))
            data.root.after(delay, lambda: timerFiredWrapper(data))

        # Wait a timer delay before beginning, to allow everything else to
        # initialize first.
        data.root.after(data.timer_delay, 
            lambda: timerFiredWrapper(data))

        def redrawAllWrapper(canvas, data):
            start = time.time()

            if data.cameraOn:
                # Get the camera frame and get it processed.
                _, data.frame = data.camera.read()
                # self.cameraFired(data)

            # Redrawing code
            canvas.delete(ALL)
            self.redrawAll(canvas, data)

            # Calculate delay accordingly
            end = time.time()
            diff_ms = (end - start) * 1000

            # Have at least a 5ms delay between redraw. Ideally higher is better.
            delay = int(max(data.redraw_delay - diff_ms, 5))

            data.root.after(delay, lambda: redrawAllWrapper(canvas, data))

        # Start drawing immediately
        data.root.after(0, lambda: redrawAllWrapper(canvas, data))

        # Loop tkinter
        data.root.mainloop()

        # Once the loop is done, release the camera.
        # print("Releasing camera!")
        # data.camera.release()

App(1000, 600)