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
            self.inventoryTable.addProductRow(item['item_name'], item["item_price"])

        self.cart = []
        self.cartTotal = 0

        # make table for cart (empty at first)
        self.cartTable = Table(25, 375, 600, 3, name='Cart')

        # checkout button
        self.checkoutButton = DarkButton(self.width-350, 395,
                                  self.width-25,
                                  name='Checkout')


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
        else:
            self.logoutButton.mousePressed(event)
            self.settingsButton.mousePressed(event)
            self.addMoneyButton.mousePressed(event)
            self.removeMoneyButton.mousePressed(event)
            self.checkoutButton.mousePressed(event)

            # inventory row mouse pressed to add items to cart
            for row in self.inventoryTable.onScreen:
                row.mousePressed(event)
                if row.button.clicked:
                    self.cart.append((row.name, row.price))
                    self.cartTable.addCartRow(self.cart[-1][0], self.cart[-1][1])
                    self.cartTotal += self.cart[-1][1]

            # mouse pressed to remove items from cart
            index = 0
            while index < len(self.cart):
                row = self.cartTable.rows[index]
                row.mousePressed(event)
                if row.button.clicked:
                    self.cartTotal -= self.cart.pop(index)[1]
                    self.cartTable.rows.pop(index)
                else:
                    index += 1

            # table mouse pressed for scrolling
            self.inventoryTable.mousePressed(event)
            self.cartTable.mousePressed(event)

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

    def mouseReleased(self, event, data):
        if self.modifyingMoney:
            self.submitMoneyButton.mouseReleased(event)
        elif self.inSettingsMode:
            self.submitSettingButton.mouseReleased(event)
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

    def redrawAll(self, canvas, data):

        # draw the table
        self.inventoryTable.draw(canvas)
        self.cartTable.draw(canvas)

        # draw total
        canvas.create_text(25, 600, text=f'Total: ${self.cartTotal}', anchor='nw', font='Helvetic 36 bold')

        # checkout button
        self.checkoutButton.draw(canvas)

        super().redrawAll(canvas, data)
