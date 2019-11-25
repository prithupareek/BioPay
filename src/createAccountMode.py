# Prithu Pareek - Created 11/19/19
# Create Account Mode

from mode import *
from customerPortalMode import *
from merchantPortalMode import *

class CreateAccountMode(Mode):
    def __init__(self, data):
        self.width = data.width
        self.height = data.height
        self.data = data
        self.usernameBox = InputBox(self.width/2-160, self.height/2-60,
        	   						self.width/2+160,
        	   						name='Username')
        self.passwordBox = InputBox(self.width/2-160, self.height/2, 
        							self.width/2+160, name='Password',
                                    hidden=True)
        self.nameBox = InputBox(self.width/2-160, self.height/2+60,
                                    self.width/2+160,
                                    name='First Name')
        self.accountTypeButton = ToggleButton(self.width/2-160, self.height/2+120,
                                  self.width/2+160,
                                  name='Customer', alternativeName='Merchant')
        self.createAccountButton = LightButton(self.width/2-160, self.height/2+180,
                                  self.width/2+160,
                                  name='Create Account')
        self.invalidCredentials = False

        self.logo = Image.open('images/logo.png')
        self.logo = scaleImage(self.logo, 0.25, antialias=True)
        self.tkLogo = ImageTk.PhotoImage(self.logo)

        self.userAlreadyExists = False

    def mousePressed(self, event, data):
        self.usernameBox.mousePressed(event)
        self.passwordBox.mousePressed(event)
        self.nameBox.mousePressed(event)
        self.accountTypeButton.mousePressed(event)
        self.createAccountButton.mousePressed(event)

        if self.createAccountButton.clicked:
            self.onCreateAccountClickEvent()

    def onCreateAccountClickEvent(self):
        # connect to sql database
        host='35.237.8.126'
        sqlUser='root'
        password='[3#1/r>(e}UI6;Q'
        db='biometric_payment_database'
        self.data.sql = SQLConnection(host, sqlUser, password, db)

        # first check if user already exists
        if self.data.sql.findUserByUsername(self.usernameBox.inputText) != None:
            self.userAlreadyExists = True
            return

        self.userAlreadyExists = False

        currUser = self.data.sql.createAccount(self.usernameBox.inputText, self.passwordBox.inputText, 
                                               self.nameBox.inputText, self.accountTypeButton.name[0])

        # go to the respective portal
        user.id = currUser['user_id']
        user.username = currUser['user_name']
        user.password = currUser['user_password']
        user.firstName = currUser['user_firstName']
        user.type = currUser['user_typ']
        user.balance = currUser['user_balance']
        user.face = currUser['user_face']
        user.faceEncoding = currUser['user_face_encoding']


        if user.type == 'C':
            self.data.customerPortalMode = CustomerPortalMode(self.data)
            self.data.activeMode=self.data.customerPortalMode
        else:
            # if merchant, then create merchant inventory table, and add reference to user_id table
            self.data.sql.setInventoryReference(user.id)
            user.inventoryTableName = f"M_{user.id}_Inventory"
            self.data.sql.createMerchantInventoryTable(user.id)


            self.data.merchantPortalMode = MerchantPortalMode(self.data)
            self.data.activeMode=self.data.merchantPortalMode


    def mouseReleased(self, event, data):
        self.createAccountButton.mouseReleased(event)

    def timerFired(self, data):
        # self.usernameBox.timerFired()
        # self.passwordBox.timerFired()
        pass

    def keyPressed(self, event, data):
        self.usernameBox.keyPressed(event)
        self.passwordBox.keyPressed(event)
        self.nameBox.keyPressed(event)

    def redrawAll(self, canvas, data):
        canvas.create_text(self.width/2, 50, text="LoginMode")

        # username box
        self.usernameBox.draw(canvas)
        self.passwordBox.draw(canvas)
        self.nameBox.draw(canvas)
        self.createAccountButton.draw(canvas)
        self.accountTypeButton.draw(canvas)

        if self.userAlreadyExists:
            canvas.create_text(self.width/2, self.height/2+230, text="User already exists.", font='Helvetica 16', fill='red')

        # header
        canvas.create_rectangle(0,0,self.width, self.height/2-100, fill=MAIN_COLOR)
        canvas.create_image(self.width/2, 100, image=self.tkLogo)

        # footer
        canvas.create_rectangle(0,self.height,self.width, self.height/2+250, fill=MAIN_COLOR)
        canvas.create_text(self.width/2, self.height/2+275, text='Created By Prithu Pareek 2019', fill='#FFFFFF')
        # canvas.create_text(self.x01+5, self.y01+50, text=self.userNameText, anchor='sw', font='Helvetica 36 bold')










