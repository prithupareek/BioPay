# Prithu Pareek - Created 11/19/19
# Customer Portal Mode

from mode import *
import loginMode
from decimal import Decimal
import base64
from io import BytesIO

class CustomerPortalMode(Mode):
    def __init__(self, data):
        self.width = data.width
        self.height = data.height
        self.data = data

        # logo image
        self.logo = Image.open('images/logo.png')
        self.logo = scaleImage(self.logo, 0.1, antialias=True)
        self.tkLogo = ImageTk.PhotoImage(self.logo)

        # logout button
        self.logoutButton = DarkButton(self.width-185, 90,
                                  self.width-25,
                                  name='Logout')
        # settings button
        self.settingsButton = LightButton(self.width-350, 90,
                                  self.width-200,
                                  name='Settings')
        self.inSettingsMode = False # when true, settings pane is visible
        self.submitSettingButton = DarkButton(self.width/2-160, self.height/2+100,
                                  self.width/2+160,
                                  name='Submit')
        self.usernameBox = InputBox(self.width/2-160, self.height/2-80,
                                    self.width/2+160,
                                    name='Username')
        self.passwordBox = InputBox(self.width/2-160, self.height/2-20, 
                                    self.width/2+160, name='Password',
                                    hidden=True)
        self.nameBox = InputBox(self.width/2-160, self.height/2+40,
                                    self.width/2+160,
                                    name='First Name')

        self.updateBalanceCounter = 0

        # add money button
        self.addMoneyButton = DarkButton(self.width-350, 275,
                                  self.width-25,
                                  name='Add Money')
        # remove money button
        self.removeMoneyButton = DarkButton(self.width-350, 335,
                                  self.width-25,
                                  name='Remove Money')
        # modify money input
        self.moneyInput = InputBox(self.width/2-160, self.height/2-50,
                                    self.width/2+160,
                                    name='Amount')
        # submit money button
        self.submitMoneyButton = DarkButton(self.width/2-160, self.height/2+10,
                                  self.width/2+160,
                                  name='Submit')
        self.modifyingMoney = False
        self.modifyMode = 1 #1=add, -1=subtract

        # transparent image
        self.transparent = Image.open('images/opacity.png')
        self.transparent = scaleImage(self.transparent, 4, antialias=True)
        self.tkTransparent = ImageTk.PhotoImage(self.transparent)

        # user image to be displayed on portal
        # first needs to be converted from base64 to actual image
        image = BytesIO(base64.b64decode(user.face))
        self.userImage = Image.open(image)
        self.tkUserImage = ImageTk.PhotoImage(self.userImage)

        # change user face image button 
        self.changeFaceButton = DarkButton(self.width-350, 525,
                                  self.width-25,
                                  name='Change Face')
        self.changingFace = False
        # capture picture button
        self.captureImageButton = DarkButton(self.width/2-160, self.height/2+110,
                                  self.width/2+160,
                                  name='Capture')

    def timerFired(self, data):
        self.updateBalanceCounter += 1
        if self.updateBalanceCounter % 15 == 0:
            self.updateBalance()

    def updateBalance(self):
        currBalance = self.data.sql.updateAccountBalance(user.id)
        user.balance = currBalance['user_balance']

    def mousePressed(self, event, data):  
        if self.modifyingMoney:
            self.moneyInput.mousePressed(event)
            self.submitMoneyButton.mousePressed(event)

            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-80<event.y<self.height/2+80):
                self.modifyingMoney = False
        elif self.inSettingsMode:
            self.submitSettingButton.mousePressed(event)
            self.usernameBox.mousePressed(event)
            self.passwordBox.mousePressed(event)
            self.nameBox.mousePressed(event)

            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-200<event.y<self.height/2+200):
                self.inSettingsMode = False
        elif self.changingFace:
            self.captureImageButton.mousePressed(event)

            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-200<event.y<self.height/2+200):
                self.changingFace = False
                print("Releasing camera!")
                self.data.camera.release()
                self.data.cameraOn = False
        else:
            self.logoutButton.mousePressed(event)
            self.settingsButton.mousePressed(event)
            self.addMoneyButton.mousePressed(event)
            self.removeMoneyButton.mousePressed(event)
            self.changeFaceButton.mousePressed(event)

        if self.logoutButton.clicked:
            self.onLogoutButtonClickEvent()
        elif self.addMoneyButton.clicked:
            self.addMoneyButton.mouseReleased(event)
            self.onMoneyClickEvent(1)
        elif self.removeMoneyButton.clicked:
            self.removeMoneyButton.mouseReleased(event)
            self.onMoneyClickEvent(-1)
        elif self.submitMoneyButton.clicked:
            self.submitMoneyButton.mouseReleased(event)
            self.onSubmitMoneyClick()
        elif self.settingsButton.clicked:
            self.settingsButton.mouseReleased(event)
            self.onSettingsButtonClickEvent()
        elif self.submitSettingButton.clicked:
            self.submitSettingButton.mouseReleased(event)
            self.onSubmitSettingsButtonClickEvent()
        elif self.changeFaceButton.clicked:
            self.changeFaceButton.mouseReleased(event)
            self.onChangeFaceButtonClickEvent()
        elif self.captureImageButton.clicked:
            self.captureImageButton.mouseReleased(event)
            self.onCaptureImageButtonClickEvent()

    def onCaptureImageButtonClickEvent(self):
        # capture the image
        image = self.data.frame
        # convert to grayscale to reduce file size on databse
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # turn the image from array to actual image
        convertedImage = cv2.imencode('.jpg', image)[1]

        # convert to bytearray
        text = base64.b64encode(convertedImage)
        text = text.decode('utf-8')

        # save to database
        self.data.sql.updateFaceImage(user.id, text)
        
        # put new image on screen
        user.face = text
        self.tkUserImage = opencvToTk(image)


        # close window
        self.changingFace = False
        print("Releasing camera!")
        self.data.camera.release()
        self.data.cameraOn = False

    def onChangeFaceButtonClickEvent(self):
        # turn on the webcam 
        # From https://github.com/VasuAgrawal/112-opencv-tutorial/blob/master/opencvTkinterTemplate.py
        # with slight modifications
        camera = cv2.VideoCapture(self.data.camera_index)
        self.data.camera = camera
        self.data.cameraOn = True
        self.data.imageCaptured = False
        # _, self.data.frame = self.data.camera.read()
        self.changingFace = True

    def onSettingsButtonClickEvent(self):
        self.inSettingsMode = True

    def onSubmitSettingsButtonClickEvent(self):
        if self.usernameBox.inputText != ('' or self.usernameBox.name):
            username = self.usernameBox.inputText
        else:
            username = user.username
        if self.passwordBox.inputText != ('' or self.passwordBox.name):
            password = self.passwordBox.inputText
        else:
            password = user.password
        if self.nameBox.inputText != ('' or self.nameBox.name):
            name = self.nameBox.inputText
        else:
            name = user.firstName
        
        self.data.sql.modifyAccount(user.id, username, password, name)
        (user.username, user.password, user.firstName) = (username, password, name)
        self.inSettingsMode = False
        self.usernameBox.inputText = self.usernameBox.name
        self.passwordBox.inputText = self.passwordBox.name
        self.nameBox.inputText = self.nameBox.name

    def onSubmitMoneyClick(self):
        amountChange = Decimal(self.moneyInput.inputText)*self.modifyMode
        amount = user.balance + amountChange
        self.data.sql.modifyAccountBalance(user.id, amount)
        self.modifyingMoney = False
        self.moneyInput.inputText='Amount'

    def onMoneyClickEvent(self, mode):
        self.modifyingMoney = True
        self.modifyMode = mode

    def onLogoutButtonClickEvent(self):
        user = Struct()
        self.data.loginMode = loginMode.LoginMode(self.data)
        self.data.activeMode = self.data.loginMode

    def mouseReleased(self, event, data):
        if self.modifyingMoney:
            self.submitMoneyButton.mouseReleased(event)
        elif self.inSettingsMode:
            self.submitSettingButton.mouseReleased(event)
        elif self.changingFace:
            self.captureImageButton.mouseReleased(event)
        else:
            self.logoutButton.mouseReleased(event)
            self.settingsButton.mouseReleased(event)
            self.addMoneyButton.mouseReleased(event)
            self.removeMoneyButton.mouseReleased(event)
            self.changeFaceButton.mouseReleased(event)

    def keyPressed(self, event, data):
        if self.modifyingMoney:
            self.moneyInput.keyPressed(event)
        if self.inSettingsMode:
            self.usernameBox.keyPressed(event)
            self.passwordBox.keyPressed(event)
            self.nameBox.keyPressed(event)

    # From https://github.com/VasuAgrawal/112-opencv-tutorial/blob/master/opencvTkinterTemplate.py
    # with slight modifications
    def drawCamera(self, canvas, data):
        # resize image
        self.data.frame = cv2.resize(self.data.frame, (200, 113))
        data.tk_image = opencvToTk(self.data.frame)
        canvas.create_image(data.width / 2, data.height / 2, image=data.tk_image)

    # TODO: Fix exact UI Pixel stuff
    def drawFaceCapturePane(self, canvas):
        canvas.create_image(0,0,image=self.tkTransparent)
        canvas.create_rectangle(self.width/2-200, self.height/2-160, self.width/2+200, self.height/2+160, fill='#FFFFFF')
        canvas.create_text(self.width/2-160, self.height/2-140, text="Camera", anchor='nw', font='Helvetica 30')

        # draw the webcam
        self.drawCamera(canvas, self.data)

        # draw the capture button
        self.captureImageButton.draw(canvas)

    def drawMoneyPane(self, canvas):
        canvas.create_image(0,0,image=self.tkTransparent)
        canvas.create_rectangle(self.width/2-200, self.height/2-80, self.width/2+200, self.height/2+80, fill='#FFFFFF')
        self.moneyInput.draw(canvas)
        self.submitMoneyButton.draw(canvas)

    def drawSettingsPane(self, canvas):
        canvas.create_image(0,0,image=self.tkTransparent)
        canvas.create_rectangle(self.width/2-200, self.height/2-160, self.width/2+200, self.height/2+160, fill='#FFFFFF')
        canvas.create_text(self.width/2-160, self.height/2-140, text="Settings", anchor='nw', font='Helvetica 30')
        self.submitSettingButton.draw(canvas)
        self.usernameBox.draw(canvas)
        self.passwordBox.draw(canvas)
        self.nameBox.draw(canvas)

    def drawAccountBalance(self, canvas):
        # boundary rect
        canvas.create_rectangle(self.width-350, 150, self.width-25, 250, outline=GRAY_COLOR)
        canvas.create_text(self.width-340, 160, text='Account Balance', font='Helvetica 24 bold', anchor='nw')
        canvas.create_text(self.width-340, 190, text=f'${user.balance}', font='Helvetica 48', anchor='nw', fill=MAIN_COLOR)

    def redrawAll(self, canvas, data):
        # header
        canvas.create_rectangle(0, 0, self.width, 70, fill=MAIN_COLOR)
        canvas.create_image(self.width/2, 35, image=self.tkLogo)

        # Cutomer Portal text
        canvas.create_text(25, 90, text=f'Welcome, {user.firstName}!', font='Helvetica 36', anchor='nw')
        # welcome text
        canvas.create_text(25, 130, text='(Customer)', font='Helvetica 12 italic', anchor='nw')

        # logout button
        self.logoutButton.draw(canvas)
        # settings button
        self.settingsButton.draw(canvas)
        # add and remove money buttons
        self.addMoneyButton.draw(canvas)
        self.removeMoneyButton.draw(canvas)
        # change face button
        self.changeFaceButton.draw(canvas)

        self.drawAccountBalance(canvas)

        # userface image
        canvas.create_image(self.width-187, 455, image=self.tkUserImage)

        # footer
        canvas.create_rectangle(0,self.height,self.width, self.height/2+280, fill=MAIN_COLOR)
        canvas.create_text(self.width/2, self.height/2+290, text='Created By Prithu Pareek 2019', fill='#FFFFFF')

        if self.modifyingMoney:
            self.drawMoneyPane(canvas)
        elif self.inSettingsMode:
            self.drawSettingsPane(canvas)
        elif self.changingFace:
            self.drawFaceCapturePane(canvas)

