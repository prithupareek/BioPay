# Prithu Pareek - Created 11/19/19
# Customer Portal Mode
# Holds the class for the customer portal

from portalMode import *

# inherits from generic portal mode class
class CustomerPortalMode(PortalMode):
    def __init__(self, data):
        super().__init__(data)

        self.type = 'Customer'

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
        self.transactions = data.sql.getTransactionHistory(user.id)
        for item in self.transactions:
            transId = item['trans_id']
            transPrice = item['trans_amount']
            merchName = data.sql.getUserNameById(item['recipient_id'])['user_firstName']
            self.transactionTable.addRow(transId, merchName, transPrice, mode='noButton')
        
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

        # listen for other button clicks in the main portal mode
        else:
            self.logoutButton.mousePressed(event)
            self.settingsButton.mousePressed(event)
            self.addMoneyButton.mousePressed(event)
            self.removeMoneyButton.mousePressed(event)
            self.changeFaceButton.mousePressed(event)

            self.transactionTable.mousePressed(event)

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
        print(len(text))
        text = text.decode('utf-8')
        print(len(text))

        # save to database
        self.data.sql.updateFaceImage(user.id, text)

        # update face encoding...
        # opencv stores images in BGR order, so first need to convert to rgb order
        # From https://github.com/ageitgey/face_recognition/issues/441
        rgbImage = self.data.frame[:, :, ::-1]
        myFaceEncoding = face_recognition.face_encodings(rgbImage)[0]

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
        print("Releasing camera!")
        self.data.camera.release()
        self.data.cameraOn = False

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
        else:
            self.logoutButton.mouseReleased(event)
            self.settingsButton.mouseReleased(event)
            self.addMoneyButton.mouseReleased(event)
            self.removeMoneyButton.mouseReleased(event)
            self.changeFaceButton.mouseReleased(event)

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

    def redrawAll(self, canvas, data):

        # change face button
        self.changeFaceButton.draw(canvas)

        if user.face != None:
            # userface image
            canvas.create_image(self.width-187, 455, image=self.tkUserImage)

        # draw trans history table
        self.transactionTable.draw(canvas)

        super().redrawAll(canvas, data)

        if self.changingFace:
            self.drawFaceCapturePane(canvas)

