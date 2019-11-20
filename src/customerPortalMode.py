# Prithu Pareek - Created 11/19/19
# Customer Portal Mode

from mode import *
import loginMode

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

    def mousePressed(self, event, data):
        self.logoutButton.mousePressed(event)

        if self.logoutButton.clicked:
            self.onLogoutButtonClickEvent()

    def onLogoutButtonClickEvent(self):
        user = Struct()
        self.data.loginMode = loginMode.LoginMode(self.data)
        self.data.activeMode = self.data.loginMode

    def mouseReleased(self, event, data):
        self.logoutButton.mouseReleased(event)

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

        # footer
        canvas.create_rectangle(0,self.height,self.width, self.height/2+250, fill=MAIN_COLOR)
        canvas.create_text(self.width/2, self.height/2+275, text='Created By Prithu Pareek 2019', fill='#FFFFFF')