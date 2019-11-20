# Prithu Pareek - Created 11/19/19
# Customer Portal Mode

from mode import *
import loginMode
from decimal import Decimal

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
        # logout button
        self.settingsButton = LightButton(self.width-350, 90,
                                  self.width-200,
                                  name='Settings')
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
        else:
            self.logoutButton.mousePressed(event)
            self.settingsButton.mousePressed(event)
            self.addMoneyButton.mousePressed(event)
            self.removeMoneyButton.mousePressed(event)

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

    def onSubmitMoneyClick(self):
        amountChange = Decimal(self.moneyInput.inputText)*self.modifyMode
        amount = user.balance + amountChange
        print(amount)
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
        else:
            self.logoutButton.mouseReleased(event)
            self.settingsButton.mouseReleased(event)
            self.addMoneyButton.mouseReleased(event)
            self.removeMoneyButton.mouseReleased(event)

    def keyPressed(self, event, data):
        if self.modifyingMoney:
            self.moneyInput.keyPressed(event)

    def drawMoneyPane(self, canvas):
        canvas.create_image(0,0,image=self.tkTransparent)
        canvas.create_rectangle(self.width/2-200, self.height/2-80, self.width/2+200, self.height/2+80, fill='#FFFFFF')
        self.moneyInput.draw(canvas)
        self.submitMoneyButton.draw(canvas)

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

        self.drawAccountBalance(canvas)

        # footer
        canvas.create_rectangle(0,self.height,self.width, self.height/2+250, fill=MAIN_COLOR)
        canvas.create_text(self.width/2, self.height/2+275, text='Created By Prithu Pareek 2019', fill='#FFFFFF')

        if self.modifyingMoney:
            self.drawMoneyPane(canvas)

