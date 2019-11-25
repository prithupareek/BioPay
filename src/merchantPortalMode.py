# Prithu Pareek - Created 11/19/19
# Merchant Portal Mode

from portalMode import *

class MerchantPortalMode(PortalMode):
    def __init__(self, data):
        super().__init__(data)

        self.type = 'Merchant'

        # get inventory data
        self.inventory = data.sql.getInventoryData(user.inventoryTableName)

        # make the inventory table
        self.inventoryTable = Table(25, 150, 600, 3, name='Inventory')
        # add the items to the table
        for item in self.inventory:
            self.inventoryTable.addRow(item['item_name'], item["item_price"], mode='Add')

        self.cart = []
        self.cartTotal = 0
        # self.onScreenCart = []

        # make table for cart (empty at first)
        self.cartTable = Table(25, 375, 600, 3, name='Cart')

        # checkout button
        self.checkoutButton = DarkButton(self.width-350, 395,
                                  self.width-25,
                                  name='Checkout')
        self.checkingOut = False
        # capture picture button
        self.captureImageButton = DarkButton(self.width/2-160, self.height/2+110,
                                  self.width/2+160,
                                  name='Capture')

        # used during checkout, set to none by default
        self.transactionFailed = False


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
        elif self.checkingOut:
            self.captureImageButton.mousePressed(event)

            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-200<event.y<self.height/2+200):
                self.checkingOut = False
                print("Releasing camera!")
                self.data.camera.release()
                self.data.cameraOn = False
        else:
            self.logoutButton.mousePressed(event)
            self.settingsButton.mousePressed(event)
            self.addMoneyButton.mousePressed(event)
            self.removeMoneyButton.mousePressed(event)
            self.checkoutButton.mousePressed(event)

            # table mouse pressed for scrolling
            self.inventoryTable.mousePressed(event)
            self.cartTable.mousePressed(event)

            # loop through inventory to check if button clicked, and then add to cart
            for row in self.inventoryTable.rows:
                if row.button.clicked:
                    # self.cart = [(row.name, row.price)] + self.cart[:]
                    # self.cartTotal += self.cart[0][1]
                    self.cartTable.addRow(row.name, row.price, mode='Remove')

            # loop through the cart rows to check if button clicked, and then remove from cart
            for row in self.cartTable.rows:
                if row.button.clicked:
                    self.cartTable.removeRow(row)
                    break

            self.cart = [(row.name, row.price) for row in self.cartTable.rows]
            self.cartTotal = sum([price for (name, price) in self.cart])

        if self.logoutButton.clicked:
            self.onLogoutButtonClickEvent()
        if self.addMoneyButton.clicked:
            self.addMoneyButton.mouseReleased(event)
            self.onMoneyClickEvent(1)
        if self.removeMoneyButton.clicked:
            self.removeMoneyButton.mouseReleased(event)
            self.onMoneyClickEvent(-1)
        if self.submitMoneyButton.clicked:
            self.submitMoneyButton.mouseReleased(event)
            self.onSubmitMoneyClick()
        if self.settingsButton.clicked:
            self.settingsButton.mouseReleased(event)
            self.onSettingsButtonClickEvent()
        if self.submitSettingButton.clicked:
            self.submitSettingButton.mouseReleased(event)
            self.onSubmitSettingsButtonClickEvent()
        if self.checkoutButton.clicked:
            self.checkoutButton.mouseReleased(event)
            self.onCheckoutButtonClickEvent()
        if self.captureImageButton.clicked:
            self.captureImageButton.mouseReleased(event)
            self.onCaptureImageButtonClickEvent()

    def onCaptureImageButtonClickEvent(self):
        # capture the image
        image = self.data.frame

        # get face encoding for image
        # opencv stores images in BGR order, so first need to convert to rgb order
        # From https://github.com/ageitgey/face_recognition/issues/441
        rgbImage = image[:, :, ::-1]
        myFaceEncoding = face_recognition.face_encodings(rgbImage)[0]

        transactionCustId = None

        # compare to other encodings and find a match
        for customer in user.allFaceEncodings:
            uid = customer['user_id']
            b64Encoded = customer['user_face_encoding']
            
            if b64Encoded != None:
                decoded = base64.b64decode(b64Encoded)
                faceEncoding = np.fromstring(decoded, dtype=float)

                faceCompare = face_recognition.compare_faces([faceEncoding], myFaceEncoding)

                if faceCompare[0] == True:
                    transactionCustId = uid
                    break

        # complete transaction
        # if no cust found
        if transactionCustId == None:
            self.transactionFailed = True
        else:
            self.data.sql.transferMoney(transactionCustId, user.id, self.cartTotal)
            self.transactionFailed = False
            
            # once transaction is done, reset cart
            self.cart = []
            self.cartTotal = 0
            self.cartTable = Table(25, 375, 600, 3, name='Cart')


        # close window
        self.checkingOut = False
        print("Releasing camera!")
        self.data.camera.release()
        self.data.cameraOn = False

    def onCheckoutButtonClickEvent(self):
        # turn on the webcam 
        # From https://github.com/VasuAgrawal/112-opencv-tutorial/blob/master/opencvTkinterTemplate.py
        # with slight modifications
        camera = cv2.VideoCapture(self.data.camera_index)
        self.data.camera = camera
        self.data.cameraOn = True
        self.data.imageCaptured = False
        self.checkingOut = True

    def mouseReleased(self, event, data):
        if self.modifyingMoney:
            self.submitMoneyButton.mouseReleased(event)
        elif self.inSettingsMode:
            self.submitSettingButton.mouseReleased(event)
        elif self.checkingOut:
            self.captureImageButton.mouseReleased(event)
        else:
            self.logoutButton.mouseReleased(event)
            self.settingsButton.mouseReleased(event)
            self.addMoneyButton.mouseReleased(event)
            self.removeMoneyButton.mouseReleased(event)
            self.checkoutButton.mouseReleased(event)

            # row mouse released
            for row in self.inventoryTable.onScreen:
                row.mouseReleased(event)

            # table mouse released for scrolling
            self.inventoryTable.mouseReleased(event)
            self.cartTable.mouseReleased(event)

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

    def redrawAll(self, canvas, data):

        # draw the table
        self.inventoryTable.draw(canvas)
        self.cartTable.draw(canvas)

        # draw total
        canvas.create_text(25, 600, text=f'Total: ${self.cartTotal}', anchor='nw', font='Helvetic 36 bold')

        # checkout button
        self.checkoutButton.draw(canvas)

        super().redrawAll(canvas, data)

        if self.transactionFailed:
            canvas.create_text(300, 600, text="Transaction Failed. Try again.", anchor='nw', font='Helvetic 16', fill='red')

        if self.checkingOut:
            self.drawFaceCapturePane(canvas)
