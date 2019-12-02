# Prithu Pareek - Created 11/19/19
# Create Account Mode
# This file contains the class that hold the create account mode for the app.

from mode import *
from customerPortalMode import *
from merchantPortalMode import *

class CreateAccountMode(Mode):
    def __init__(self, data):

        # screen with and height
        self.width = data.width
        self.height = data.height
        self.data = data

        # input boxes
        self.usernameBox = InputBox(self.width/2-160, self.height/2-60,
        	   						self.width/2+160,
        	   						name='Username')
        self.passwordBox = InputBox(self.width/2-160, self.height/2, 
        							self.width/2+160, name='Password',
                                    hidden=True)
        self.nameBox = InputBox(self.width/2-160, self.height/2+60,
                                    self.width/2+160,
                                    name='First Name')

        # button for user to chose betweeen customer or merchant account
        self.accountTypeButton = ToggleButton(self.width/2-160, self.height/2+120,
                                  self.width/2+160,
                                  name='Customer', alternativeName='Merchant')

        # button to allow user to create an account
        self.createAccountButton = LightButton(self.width/2-160, self.height/2+180,
                                  self.width/2+160,
                                  name='Create Account')

        # get the logo from files, scales it, and converts it to a Tk Image
        self.logo = Image.open('images/logo.png')
        self.logo = scaleImage(self.logo, 0.25, antialias=True)
        self.tkLogo = ImageTk.PhotoImage(self.logo)

        # set to true if the user already exits, no account can be made with the same username twice
        self.userAlreadyExists = False

    # triggered on a mouse pressed event
    def mousePressed(self, event, data):
        # mouse pressed events for the buttons/input boxes
        self.usernameBox.mousePressed(event)
        self.passwordBox.mousePressed(event)
        self.nameBox.mousePressed(event)
        self.accountTypeButton.mousePressed(event)
        self.createAccountButton.mousePressed(event)

        # triggers a function call if create account button is clicked
        if self.createAccountButton.clicked:
            self.onCreateAccountClickEvent()

    # called if create account button is clicked
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

        # make the sql call
        currUser = self.data.sql.createAccount(self.usernameBox.inputText, sha1.hash(self.passwordBox.inputText), 
                                               self.nameBox.inputText, self.accountTypeButton.name[0])

        # grab user data from return of sql call
        user.id = currUser['user_id']
        user.username = currUser['user_name']
        user.password = currUser['user_password']
        user.firstName = currUser['user_firstName']
        user.type = currUser['user_typ']
        user.balance = currUser['user_balance']
        user.face = currUser['user_face']
        user.faceEncoding = currUser['user_face_encoding']

        # go to respective portal if user is customer or merchant
        if user.type == 'C':
            self.data.customerPortalMode = CustomerPortalMode(self.data)
            self.data.activeMode=self.data.customerPortalMode
        else:
            # if merchant, then create merchant inventory table, and add reference to user_id table
            self.data.sql.setInventoryReference(user.id)
            user.inventoryTableName = f"M_{user.id}_Inventory"
            self.data.sql.createMerchantInventoryTable(user.id)

            # go to merchant portal
            self.data.merchantPortalMode = MerchantPortalMode(self.data)
            self.data.activeMode=self.data.merchantPortalMode

    # mouse released events
    def mouseReleased(self, event, data):
        self.createAccountButton.mouseReleased(event)

    # key pressed events
    def keyPressed(self, event, data):
        self.usernameBox.keyPressed(event)
        self.passwordBox.keyPressed(event)
        self.nameBox.keyPressed(event)

    # draws to the canvas
    def redrawAll(self, canvas, data):
        canvas.create_text(self.width/2, 50, text="LoginMode")

        # username box
        self.usernameBox.draw(canvas)
        self.passwordBox.draw(canvas)
        self.nameBox.draw(canvas)
        self.createAccountButton.draw(canvas)
        self.accountTypeButton.draw(canvas)

        # display error if user alread exists
        if self.userAlreadyExists:
            canvas.create_text(self.width/2, self.height/2+230, text="User already exists.", font='Helvetica 16', fill='red')

        # header
        canvas.create_rectangle(0,0,self.width, self.height/2-100, fill=MAIN_COLOR)
        canvas.create_image(self.width/2, 100, image=self.tkLogo)

        # footer
        canvas.create_rectangle(0,self.height,self.width, self.height/2+250, fill=MAIN_COLOR)
        canvas.create_text(self.width/2, self.height/2+275, text='Created By Prithu Pareek 2019', fill='#FFFFFF')











