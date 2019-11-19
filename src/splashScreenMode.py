# Prithu Pareek - Created 11/19/19
# Splash Screen Mode

from mode import *

# Create the splash screen, transitions to the login mode automatically after 3 seconds
class SplashScreenMode(Mode):
    def __init__(self, data):
        self.width = data.width
        self.height = data.height
        self.data = data
        self.logo = Image.open('images/logo.png')
        self.logo = scaleImage(self.logo, 0.4, antialias=True)
        self.tkLogo = ImageTk.PhotoImage(self.logo)
        self.counter = 0
        
    def timerFired(self, data):
        self.counter += 1
        if self.counter == 15:
            self.data.activeMode = self.data.loginMode

    def redrawAll(self, canvas, data):
        canvas.create_rectangle(0, 0, self.width, self.height, fill=MAIN_COLOR)
        
        canvas.create_image(self.width/2, self.height/2-self.logo.height/2, image=self.tkLogo)
        canvas.create_text(self.width/2, self.height/2+50, text="BioPay", font='Helvetica 64  bold', fill='#FFFFFF')