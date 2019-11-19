# Prithu Pareek - Created 11/19/19
# Login Mode

from mode import *
from customerPortalMode import *
from merchantPortalMode import *

class LoginMode(Mode):
    def __init__(self, data):
        self.width = data.width
        self.height = data.height
        self.data = data
        self.usernameBox = InputBox(self.width/2-160, self.height/2-60,
        	   						self.width/2+160,
        	   						name='Username')
        self.passwordBox = InputBox(self.width/2-160, self.height/2+20, 
        							self.width/2+160, name='Password',
                                    hidden=True)
        self.loginButton = Button(self.width/2-160, self.height/2+80,
        						  self.width/2+160,
        						  name='Login')
        self.invalidCredentials = False

    def mousePressed(self, event, data):
        self.usernameBox.mousePressed(event)
        self.passwordBox.mousePressed(event)
        self.loginButton.mousePressed(event)

        if self.loginButton.clicked:
            self.onLoginClickEvent()

    def onLoginClickEvent(self):
        # connect to sql database
        host='35.237.8.126'
        sqlUser='root'
        password='password'
        db='biometric_payment_database'
        sql = SQLConnection(host, sqlUser, password, db)
        currUser = sql.login(self.usernameBox.inputText, self.passwordBox.inputText)
        if currUser == None:
            self.invalidCredentials = True
        else:
            self.invalidCredentials = False
            user.id = currUser['user_id']
            user.username = currUser['user_name']
            user.password = currUser['user_password']
            user.firstName = currUser['user_firstName']
            user.type = currUser['user_typ']

            if user.type == 'C':
                self.data.customerPortalMode = CustomerPortalMode(self.data)
                self.data.activeMode=self.data.customerPortalMode
            else:
                self.data.merchantPortalMode = MerchantPortalMode(self.data)
                self.data.activeMode=self.data.merchantPortalMode

    def mouseReleased(self, event, data):
        self.loginButton.mouseReleased(event)

    def timerFired(self, data):
        # self.usernameBox.timerFired()
        # self.passwordBox.timerFired()
        pass

    def keyPressed(self, event, data):
        self.usernameBox.keyPressed(event)
        self.passwordBox.keyPressed(event)

    def redrawAll(self, canvas, data):
        canvas.create_text(self.width/2, 50, text="LoginMode")

        # username box
        self.usernameBox.draw(canvas)
        self.passwordBox.draw(canvas)
        self.loginButton.draw(canvas)

        if self.invalidCredentials:
            canvas.create_text(self.width/2, self.height/2+150, text="Incorrect username of password.", font='Helvetica 16', fill='red')

        # canvas.create_text(self.x01+5, self.y01+50, text=self.userNameText, anchor='sw', font='Helvetica 36 bold')