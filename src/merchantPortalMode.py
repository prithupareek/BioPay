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
        self.inventoryTable = Table(25, 150, 600, rows=3, name='Inventory')
        # add the items to the table
        for item in self.inventory:
            self.inventoryTable.addRow(item["item_id"], item['item_name'], item["item_price"], item["item_qty"], mode='Add')

        self.cart = []
        self.cartTotal = 0
        # self.onScreenCart = []

        # make table for cart (empty at first)
        self.cartTable = Table(25, 375, 600, rows=3, name='Cart')

        # checkout button
        self.checkoutButton = DarkButton(self.width-350, 515,
                                  self.width-25,
                                  name='Checkout')
        self.checkingOut = False
        # capture picture button
        self.captureImageButton = DarkButton(self.width/2-160, self.height/2+110,
                                  self.width/2+160,
                                  name='Capture')

        # used during checkout, set to none by default
        self.transactionFailed = None

        # current transaction successsful customer
        self.transCust = None

        # edit inventory buttons
        self.addItemButton = DarkButton(self.width-350, 395,
                                        self.width-25,
                                        name='Add Item')
        self.removeItemButton = LightButton(self.width-350, 455,
                                            self.width-25,
                                            name='Remove Item')
        self.editingInventory = False

        # add/remove inventory input boxes and submit button
        self.itemNameInput = InputBox(self.width/2-160, self.height/2-80,
                                    self.width/2+160,
                                    name='Name')
        self.itemPriceInput = InputBox(self.width/2-160, self.height/2-20,
                                    self.width/2+160,
                                    name='Price')
        self.itemQtyInput = InputBox(self.width/2-160, self.height/2+40,
                                    self.width/2+160,
                                    name='Qty')
        self.itemCategoryInput = InputBox(self.width/2-160, self.height/2+100,
                                    self.width/2+160,
                                    name='Category')
        self.itemSubmitButton = DarkButton(self.width/2-160, self.height/2+160,
                                  self.width/2+160,
                                  name='Submit')

        # show suggested items button
        self.suggestedProductsButton = LightButton(self.width-350, 575,
                                                   self.width-25,
                                                   name='Suggested Products')
        self.inSuggestedProductsMode = False
        # suggested products table
        self.suggestedProductsTable = Table(self.width/2-360, self.height/2-175, self.width/2+330, rows=6, name="Customer also bought")
        # suggested products list
        self.suggestedProducts = []

    # mouse pressed eventss
    def mousePressed(self, event, data):  
        if self.modifyingMoney:
            self.moneyInput.mousePressed(event)
            self.submitMoneyButton.mousePressed(event)

            # close pane if click off of it
            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-80<event.y<self.height/2+80):
                self.modifyingMoney = False

        elif self.inSettingsMode:
            self.submitSettingButton.mousePressed(event)
            self.usernameBox.mousePressed(event)
            self.passwordBox.mousePressed(event)
            self.nameBox.mousePressed(event)

            # close pane if click off it it
            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-200<event.y<self.height/2+200):
                self.inSettingsMode = False

        elif self.checkingOut:
            self.captureImageButton.mousePressed(event)

            # close pane if click off of it
            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-200<event.y<self.height/2+200):
                self.checkingOut = False
                self.data.camera.release()
                self.data.cameraOn = False

        elif self.editingInventory:
            self.itemSubmitButton.mousePressed(event)
            self.itemNameInput.mousePressed(event)
            self.itemPriceInput.mousePressed(event)
            self.itemQtyInput.mousePressed(event)
            self.itemCategoryInput.mousePressed(event)

            # close pane if click off of it
            if not (self.width/2-200<event.x<self.width/2+200 and
                    self.height/2-200<event.y<self.height/2+200):
                self.editingInventory = False

        elif self.inSuggestedProductsMode:
            # close pane if clicik off of it
            if not (self.width/2-400<event.x<self.width/2+400 and
                    self.height/2-250<event.y<self.height/2+250):
                self.inSuggestedProductsMode = False

            self.suggestedProductsTable.mousePressed(event)

            # loop through inventory to check if button clicked, and then add to cart
            for row in self.suggestedProductsTable.rows:
                if row.button.clicked:
                    
                    # if there is enough inventory
                    if row.qty > 0:
                        # if item already in cart, then add to quantity
                        if any(row.prodId in i for i in self.cart):

                            for item in self.cartTable.rows:
                                if item.prodId == row.prodId:
                                    item.qty += 1
                        else:
                            self.cartTable.addRow(row.prodId, row.name, row.price, mode='Remove', qty=1)

                        # subtract 1 from suggested products ammount
                        row.qty -= 1

                        # subtract 1 from the inventory ammount
                        for item in self.inventoryTable.rows:
                            if item.prodId == row.prodId:
                                item.qty -= 1

                        break
        else:
            self.logoutButton.mousePressed(event)
            self.settingsButton.mousePressed(event)
            self.addMoneyButton.mousePressed(event)
            self.removeMoneyButton.mousePressed(event)
            self.checkoutButton.mousePressed(event)
            self.addItemButton.mousePressed(event)
            self.removeItemButton.mousePressed(event)
            self.suggestedProductsButton.mousePressed(event)

            # table mouse pressed for scrolling
            self.inventoryTable.mousePressed(event)
            self.cartTable.mousePressed(event)

            # loop through inventory to check if button clicked, and then add to cart
            for row in self.inventoryTable.rows:
                if row.button.clicked:
                    
                    # if there is enough inventory
                    if row.qty > 0:
                        # if item already in cart, then add to quantity
                        if any(row.prodId in i for i in self.cart):

                            for item in self.cartTable.rows:
                                if item.prodId == row.prodId:
                                    item.qty += 1
                        else:
                            self.cartTable.addRow(row.prodId, row.name, row.price, mode='Remove', qty=1)

                        # subtract 1 from inventory ammount
                        row.qty -= 1
                        break

            # loop through the cart rows to check if button clicked, and then remove from cart
            for row in self.cartTable.rows:
                if row.button.clicked:
                    # if qty > 1 then subt 1 from qty
                    if row.qty > 1:
                        row.qty -= 1
                    else:
                        self.cartTable.removeRow(row)

                    # add the item back to the inventory
                    for item in self.inventoryTable.rows:
                        if item.prodId == row.prodId:
                            item.qty += 1

                    break

        # set the cart to the items in the table rows, and update the cart toatal
        self.cart = [(row.prodId, row.name, row.price, row.qty) for row in self.cartTable.rows]
        self.cartTotal = sum([price*qty for (prodId, name, price, qty) in self.cart])

        if self.logoutButton.clicked:
            self.onLogoutButtonClickEvent()
        if self.addMoneyButton.clicked:
            self.addMoneyButton.mouseReleased(event)
            self.onMoneyClickEvent(1) # add $
        if self.removeMoneyButton.clicked:
            self.removeMoneyButton.mouseReleased(event)
            self.onMoneyClickEvent(-1) #remove $
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
        if self.addItemButton.clicked:
            self.addItemButton.mouseReleased(event)
            self.onInventoryModifyButtonClickEvent(+1) #add item
        if self.removeItemButton.clicked:
            self.removeItemButton.mouseReleased(event)
            self.onInventoryModifyButtonClickEvent(-1) #remove item
        if self.itemSubmitButton.clicked:
            self.itemSubmitButton.mouseReleased(event)
            self.onItemSubmitButtonClickEvent()
        if self.suggestedProductsButton.clicked:
            self.suggestedProductsButton.mouseReleased(event)
            self.onSuggestedProductsButtonClickEvent()

    # get a list of suggested products for a user based on cart, and add it to a table
    def onSuggestedProductsButtonClickEvent(self):
        self.inSuggestedProductsMode = True

        # clear the suggested products table and list
        self.suggestedProducts = []
        self.suggestedProductsTable.clear()


        suggestedItemsDict = dict()

        # loop through all items in users cart
        for custCartItem in self.cart:

            # loop through all previous carts and check if the item is in that cart
            for prevCart in user.previousCarts:

                # if the previous carts contains the item, then loop through the cart and add items to a dictionary
                if custCartItem[0] in prevCart:

                    for prevCartItem in prevCart:

                        if not prevCartItem in [itemId for (itemId, itemName, itemPrice, itemQty) in self.cart]:
                            suggestedItemsDict[prevCartItem] = suggestedItemsDict.get(prevCartItem, 0) + 1

        # in the dictionary loop through keys and get the top 5 item ids
        # this line sorts the dictionary based on the value of each item and returns a list of tuples (key, value)
        # Found in pydocs: https://docs.python.org/3/library/functions.html#sorted
        sortedDictList = sorted(suggestedItemsDict.items(), key= lambda item: item[1])[::-1]

        # grab only the keys from the sorted list
        sortedKeyList = [key for (key, count) in sortedDictList]
        
        # try getting the top 8 items, if less than five than return all items
        try:
            top = set(sortedKeyList[:8])

        except:
            top = set(sortedKeyList[:])

        # add the items into the suggested products list, and table
        # if a merchant is not longer selling a certain item, it will not be suggested
        for item in self.inventory:

            if item["item_id"] in top:

                self.suggestedProducts.append(item)
                self.suggestedProductsTable.addRow(item["item_id"], item['item_name'], item["item_price"], item["item_qty"], mode='Add')


    # add/remove an item from the inventory
    def onItemSubmitButtonClickEvent(self):
        itemName = self.itemNameInput.inputText
        itemPrice = self.itemPriceInput.inputText
        

        # if adding item
        if self.inventoryModifyMode == 1:

            itemQty = self.itemQtyInput.inputText
            itemCost = Decimal(itemPrice)/4
            itemCategory = self.itemCategoryInput.inputText

            # if item already in inventory
            if (itemName, Decimal(itemPrice)) in [(row.name, row.price) for row in self.inventoryTable.rows]:
                self.data.sql.updateItemQty(user.inventoryTableName, itemName, itemPrice, itemQty)
            else:
                self.data.sql.addItemToInventory(user.inventoryTableName, itemName, itemPrice, itemQty, itemCost, itemCategory)

            # charge the merchant for the items
            user.balance -= int(itemQty)*itemCost
            self.data.sql.modifyAccountBalance(user.id, user.balance)
        # removing item
        elif self.inventoryModifyMode == -1:
            self.data.sql.removeItemFromInventory(user.inventoryTableName, itemName, itemPrice)

        # update user inventory
        self.inventory = self.data.sql.getInventoryData(user.inventoryTableName)
        # make the inventory table
        self.inventoryTable.clear()
        # add the items to the table
        for item in self.inventory:
            self.inventoryTable.addRow(item["item_id"], item['item_name'], item["item_price"], item["item_qty"], mode='Add')

        # close window pane
        self.editingInventory = False
        self.itemNameInput.inputText = self.itemNameInput.name
        self.itemPriceInput.inputText = self.itemPriceInput.name
        self.itemQtyInput.inputText = self.itemQtyInput.name
        self.itemCategoryInput.inputText = self.itemCategoryInput.name
    
    def onInventoryModifyButtonClickEvent(self, mode):
        self.editingInventory = True
        self.inventoryModifyMode = mode

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

            # add transaction info to database
            self.data.sql.logTransaction(transactionCustId, user.id, self.cartTotal, self.cart)

            # get the customer name to display on the screen
            self.transCust = self.data.sql.getUserNameById(transactionCustId)['user_firstName']

            # update the customers inventory quantities
            for item in self.cartTable.rows:
                self.data.sql.updateItemQty(user.inventoryTableName, item.name, item.price, -item.qty)

            
            # once transaction is done, reset cart
            self.cart = []
            self.cartTotal = 0
            self.cartTable.clear()


        # close window
        self.checkingOut = False
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
        elif self.editingInventory:
            self.itemSubmitButton.mouseReleased(event)
        elif self.inSuggestedProductsMode:
            self.suggestedProductsTable.mouseReleased(event)
        else:
            self.logoutButton.mouseReleased(event)
            self.settingsButton.mouseReleased(event)
            self.addMoneyButton.mouseReleased(event)
            self.removeMoneyButton.mouseReleased(event)
            self.checkoutButton.mouseReleased(event)
            self.addItemButton.mouseReleased(event)
            self.removeItemButton.mouseReleased(event)
            self.suggestedProductsButton.mouseReleased(event)

            # row mouse released
            for row in self.inventoryTable.onScreen:
                row.mouseReleased(event)

            # table mouse released for scrolling
            self.inventoryTable.mouseReleased(event)
            self.cartTable.mouseReleased(event)

    def keyPressed(self, event, data):
        super().keyPressed(event, data)

        if self.editingInventory:
            self.itemNameInput.keyPressed(event)
            self.itemPriceInput.keyPressed(event)
            self.itemQtyInput.keyPressed(event)
            self.itemCategoryInput.keyPressed(event)

    def drawSuggestedProductsPane(self, canvas):
        canvas.create_image(0,0,image=self.tkTransparent)
        canvas.create_rectangle(self.width/2-400, self.height/2-250, self.width/2+400, self.height/2+250, fill='#FFFFFF')
        canvas.create_text(self.width/2-360, self.height/2-230, text="Suggested Products", anchor='nw', font='Helvetica 30')

        self.suggestedProductsTable.draw(canvas)

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

    def drawInventoryEditPane(self, canvas):
        canvas.create_image(0,0,image=self.tkTransparent)
        canvas.create_rectangle(self.width/2-200, self.height/2-160, self.width/2+200, self.height/2+220, fill='#FFFFFF')
        canvas.create_text(self.width/2-160, self.height/2-140, text="Inventory Management", anchor='nw', font='Helvetica 30')
        self.itemSubmitButton.draw(canvas)
        self.itemNameInput.draw(canvas)
        self.itemPriceInput.draw(canvas)
        

        if self.inventoryModifyMode == 1:
            self.itemQtyInput.draw(canvas)
            self.itemCategoryInput.draw(canvas)

    def redrawAll(self, canvas, data):

        # draw the table
        self.inventoryTable.draw(canvas)
        self.cartTable.draw(canvas)

        # draw total
        canvas.create_text(25, 600, text=f'Total: ${self.cartTotal}', anchor='nw', font='Helvetic 36 bold')

        # buttons
        self.checkoutButton.draw(canvas)
        self.addItemButton.draw(canvas)
        self.removeItemButton.draw(canvas)
        self.suggestedProductsButton.draw(canvas)

        super().redrawAll(canvas, data)

        if self.transactionFailed == True:
            canvas.create_text(300, 600, text="Transaction Failed. Try again.", anchor='nw', font='Helvetic 16', fill='red')
        elif self.transactionFailed == False:
            canvas.create_text(300, 600, text=f"Thank you, {self.transCust}", anchor='nw', font='Helvetic 16', fill='green')

        if self.checkingOut:
            self.drawFaceCapturePane(canvas)
        elif self.editingInventory:
            self.drawInventoryEditPane(canvas)
        elif self.inSuggestedProductsMode:
            self.drawSuggestedProductsPane(canvas)
