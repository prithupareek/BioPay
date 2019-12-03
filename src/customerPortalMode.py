# Prithu Pareek - Created 11/19/19
# Customer Portal Mode
# Holds the class for the customer portal

from portalMode import *

# inherits from generic portal mode class
class CustomerPortalMode(PortalMode):
    def __init__(self, data):
        super().__init__(data)

        self.type = 'Customer'

        self.error = False

        # user image to be displayed on portal
        # first needs to be converted from base64 to actual image
        if user.face != None:
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

        # make the transaction history table
        self.transactionTable = Table(25, 150, 600, rows=8, name='Transaction History')
        
        # get the transaction made by the user
        try:
            self.transactions = data.sql.getTransactionHistory(user.id)
            for item in self.transactions:
                transId = item['trans_id']
                transPrice = item['trans_amount']
                merchName = data.sql.getUserNameById(item['recipient_id'])['user_firstName']
                self.transactionTable.addRow(transId, merchName, transPrice, -1, mode='Add') #using add mode, just to get plus sign button on ui
                self.error = False
        except:
            self.error = True

        self.viewingCart = False

        # category breakdown
        self.spendingCategoriesButton = LightButton(self.width-350, 585,
                                                    self.width-25,
                                                    name = 'Spending Categories')
        
        self.viewingCategories = False
        self.counter = 0

        # used to avoid errors
        self.faceError = False
        self.notEnoughData = False

    # mouse pressed event
    def mousePressed(self, event, data):  
        # if adding or removing money, then only listen for events on that pane
        if self.modifyingMoney:
            self.moneyInput.mousePressed(event)
            self.submitMoneyButton.mousePressed(event)

            # if you click off the pane, then close it, and return to the main portal mode
            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-80<event.y<self.height/2+80):
                self.modifyingMoney = False

        # same idea as above but for settings
        elif self.inSettingsMode:
            self.submitSettingButton.mousePressed(event)
            self.usernameBox.mousePressed(event)
            self.passwordBox.mousePressed(event)
            self.nameBox.mousePressed(event)

            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-200<event.y<self.height/2+200):
                self.inSettingsMode = False

        # same idea as above but for updating the face picture stored in the data base
        elif self.changingFace:
            self.captureImageButton.mousePressed(event)

            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-200<event.y<self.height/2+200):
                self.changingFace = False

                # turn off the camera when you close this pane
                self.data.camera.release()
                self.data.cameraOn = False
        # if viewing cart history
        elif self.viewingCart:
            # close pane if clicik off of it
            if not (self.width/2-400<event.x<self.width/2+400 and
                    self.height/2-250<event.y<self.height/2+250):
                self.viewingCart = False

            self.currentCartTable.mousePressed(event)

        # if viewing category history
        elif self.viewingCategories:
            # close pane if clicik off of it
            if not (self.width/2-400<event.x<self.width/2+400 and
                    self.height/2-250<event.y<self.height/2+250):
                self.viewingCategories = False
                self.notEnoughData = False

        # listen for other button clicks in the main portal mode
        else:
            self.logoutButton.mousePressed(event)
            self.settingsButton.mousePressed(event)
            self.addMoneyButton.mousePressed(event)
            self.removeMoneyButton.mousePressed(event)
            self.changeFaceButton.mousePressed(event)
            self.spendingCategoriesButton.mousePressed(event)

            self.transactionTable.mousePressed(event)

            # loop through the transaction table and check if a mouse if pressed
            for row in self.transactionTable.rows:
                if row.button.clicked:
                    self.transactionTable.mouseReleased(event)

                    # show the expanded list of items in the cart
                    self.viewingCart = True

                    # get the correct cart
                    try:
                        self.currentCart = self.data.sql.getCartData(f'cart_{row.prodId}')
                        self.currentCartTable = Table(self.width/2-360, self.height/2-175, self.width/2+330, rows=6, name="Cart History")
                        for item in self.currentCart:
                            self.currentCartTable.addRow(item["item_id"], item['item_name'], item["item_price"], item["item_qty"], mode='noButton')
                        self.error = False
                    except:
                        self.error = True


        # if a button is clicked, then call its respective function
        if self.logoutButton.clicked:
            self.onLogoutButtonClickEvent()
        if self.addMoneyButton.clicked:
            self.addMoneyButton.mouseReleased(event)
            self.onMoneyClickEvent(1) #addin money
        if self.removeMoneyButton.clicked:
            self.removeMoneyButton.mouseReleased(event)
            self.onMoneyClickEvent(-1) #subtracting money
        if self.submitMoneyButton.clicked:
            self.submitMoneyButton.mouseReleased(event)
            self.onSubmitMoneyClick()
        if self.settingsButton.clicked:
            self.settingsButton.mouseReleased(event)
            self.onSettingsButtonClickEvent()
        if self.submitSettingButton.clicked:
            self.submitSettingButton.mouseReleased(event)
            self.onSubmitSettingsButtonClickEvent()
        if self.changeFaceButton.clicked:
            self.changeFaceButton.mouseReleased(event)
            self.onChangeFaceButtonClickEvent()
        if self.captureImageButton.clicked:
            self.captureImageButton.mouseReleased(event)
            self.onCaptureImageButtonClickEvent()
        if self.spendingCategoriesButton.clicked:
            self.spendingCategoriesButton.mouseReleased(event)
            self.onSpendingCategoriesButtonClickEvent()

    def timerFired(self, data):
        super().timerFired(data)

        self.counter += 1

        # periodically refresh the transaction history
        if self.counter % 150 == 0:

            # get the transaction made by the user
            self.transactionTable.clear()
            try:
                self.transactions = data.sql.getTransactionHistory(user.id)
                for item in self.transactions:
                    transId = item['trans_id']
                    transPrice = item['trans_amount']
                    merchName = data.sql.getUserNameById(item['recipient_id'])['user_firstName']
                    self.transactionTable.addRow(transId, merchName, transPrice, -1, mode='Add') #using add mode, just to get plus sign button on ui
                    self.error = False
            except:
                self.error = True


    def onSpendingCategoriesButtonClickEvent(self):

        categoriesDict = dict()

        try:
            # loop through transactions
            for transaction in self.transactions:

                # get the cart for the transaction
                transactionCart = self.data.sql.getCartData(f'cart_{transaction["trans_id"]}')

                # get the merchant inventory for the transaction
                merchantInventory = self.data.sql.getInventoryData(f'M_{transaction["recipient_id"]}_Inventory')

                # loop through the cart items
                for item in transactionCart:

                    # loop through the merchant inventory
                    for inventoryItem in merchantInventory:

                        if item["item_id"] == inventoryItem["item_id"]:

                            itemCategory = inventoryItem["item_category"]

                            if itemCategory in categoriesDict:
                                categoriesDict[itemCategory] += item["item_price"]*item["item_qty"]
                            else:
                                categoriesDict[itemCategory] = item["item_price"]*item["item_qty"]
            
            # calculate percentages
            self.percentages = {}

            total = sum(categoriesDict.values())

            for item in categoriesDict:
                self.percentages[item] = categoriesDict[item]/total

            self.chart = PieChart(self.width/2, self.height/2+15, 150, self.percentages)

            self.viewingCategories = True
            self.error = False
        except:
            self.error = True


    # takes picture and saves it to the database
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

        try:
            # save to database
            self.data.sql.updateFaceImage(user.id, text)
            self.error = False
        except:
            self.error = True

        # update face encoding...
        # opencv stores images in BGR order, so first need to convert to rgb order
        # From https://github.com/ageitgey/face_recognition/issues/441
        rgbImage = self.data.frame[:, :, ::-1]

        # makes sure that a face is found in the image
        try:
            myFaceEncoding = face_recognition.face_encodings(rgbImage)[0]
            self.faceError = False

            # convert to string to store in databse
            encoded = base64.b64encode(myFaceEncoding)
            encodedString = encoded.decode('utf-8')

            # save to database
            self.data.sql.updateFaceEncoding(user.id, encodedString)

            # put new image on screen
            user.face = text
            self.tkUserImage = opencvToTk(image)

            # close window
            self.changingFace = False
            self.data.camera.release()
            self.data.cameraOn = False
        except:
            self.faceError = True


    # turns on teh camea, and opens displays the live feed on the screen
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

    # mouse released events, different based on what state of the UI you are in
    def mouseReleased(self, event, data):
        if self.modifyingMoney:
            self.submitMoneyButton.mouseReleased(event)
        elif self.inSettingsMode:
            self.submitSettingButton.mouseReleased(event)
        elif self.changingFace:
            self.captureImageButton.mouseReleased(event)
        elif self.viewingCart:
            self.currentCartTable.mouseReleased(event)
        else:
            self.logoutButton.mouseReleased(event)
            self.settingsButton.mouseReleased(event)
            self.addMoneyButton.mouseReleased(event)
            self.removeMoneyButton.mouseReleased(event)
            self.changeFaceButton.mouseReleased(event)
            self.spendingCategoriesButton.mouseReleased(event)

            self.transactionTable.mouseReleased(event)

    # From https://github.com/VasuAgrawal/112-opencv-tutorial/blob/master/opencvTkinterTemplate.py
    # with slight modifications
    def drawCamera(self, canvas, data):
        # resize image
        self.data.frame = cv2.resize(self.data.frame, (200, 113))
        data.tk_image = opencvToTk(self.data.frame)
        canvas.create_image(data.width / 2, data.height / 2, image=data.tk_image)

    # TODO: Fix exact UI Pixel stuff
    def drawFaceCapturePane(self, canvas):
        # the transparent image is used because there is no opacity for tkinter
        canvas.create_image(0,0,image=self.tkTransparent)
        canvas.create_rectangle(self.width/2-200, self.height/2-160, self.width/2+200, self.height/2+160, fill='#FFFFFF')
        canvas.create_text(self.width/2-160, self.height/2-140, text="Camera", anchor='nw', font='Helvetica 30')

        # draw the webcam
        self.drawCamera(canvas, self.data)

        # draw the capture button
        self.captureImageButton.draw(canvas)

    def drawCartPane(self, canvas):
        canvas.create_image(0,0,image=self.tkTransparent)
        canvas.create_rectangle(self.width/2-400, self.height/2-250, self.width/2+400, self.height/2+250, fill='#FFFFFF')
        canvas.create_text(self.width/2-360, self.height/2-230, text="Transaction History", anchor='nw', font='Helvetica 30')

        self.currentCartTable.draw(canvas)

    def drawCategoriesPane(self, canvas):
        canvas.create_image(0,0,image=self.tkTransparent)
        canvas.create_rectangle(self.width/2-400, self.height/2-250, self.width/2+400, self.height/2+250, fill='#FFFFFF')
        canvas.create_text(self.width/2-360, self.height/2-230, text="Spending Categories", anchor='nw', font='Helvetica 30')

        try:
            self.chart.draw(canvas)
            self.notEnoughData = False
        except:
            self.notEnoughData = True

    def redrawAll(self, canvas, data):

        # change face button
        self.changeFaceButton.draw(canvas)

        # categoreis button
        self.spendingCategoriesButton.draw(canvas)

        if user.face != None:
            # userface image
            canvas.create_image(self.width-187, 455, image=self.tkUserImage)

        # draw trans history table
        self.transactionTable.draw(canvas)

        super().redrawAll(canvas, data)

        if self.changingFace:
            self.drawFaceCapturePane(canvas)
        elif self.viewingCart:
            self.drawCartPane(canvas)
        elif self.viewingCategories:
            self.drawCategoriesPane(canvas)

        if self.faceError:
            canvas.create_text(300, 600, text="Face scanning error. Try again.", anchor='nw', font='Helvetic 16', fill='red')
        if self.error:
            canvas.create_text(300, 600, text="Oops. Something went wrong.", anchor='nw', font='Helvetic 16', fill='red')
        if self.notEnoughData:
            canvas.create_text(self.width/2, self.height/2, text="Not enough data.", anchor='c', font='Helvetic 16', fill='red')
