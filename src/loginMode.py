# Prithu Pareek - Created 11/19/19
# Login Mode

from mode import *

class LoginMode(Mode):
    def __init__(self, data):
        self.width = data.width
        self.height = data.height
        self.data = data
        self.usernameBox = InputBox(self.width/2-160, self.height/2-60,
        	   						self.width/2+160,
        	   						name='Username')
        self.passwordBox = InputBox(self.width/2-160, self.height/2+20, 
        							self.width/2+160, name='Password')
        self.loginButton = Button(self.width/2-160, self.height/2+80,
        						  self.width/2+160,
        						  name='Login')

    def mousePressed(self, event, data):
        self.usernameBox.mousePressed(event)
        self.passwordBox.mousePressed(event)
        self.loginButton.mousePressed(event)

        if self.loginButton.clicked:
        	print("clicked")

    def timerFired(self, data):
        # self.usernameBox.timerFired()
        # self.passwordBox.timerFired()
        pass

    def keyPressed(self, event, data):
        self.usernameBox.keyPressed(event)
        self.passwordBox.keyPressed(event)
        self.loginButton.keyPressed(event)

    def redrawAll(self, canvas, data):
        canvas.create_text(self.width/2, 50, text="LoginMode")

        # username box
        self.usernameBox.draw(canvas)
        self.passwordBox.draw(canvas)
        self.loginButton.draw(canvas)
        # canvas.create_text(self.x01+5, self.y01+50, text=self.userNameText, anchor='sw', font='Helvetica 36 bold')