# Prithu Pareek - Created 11/19/19
# Customer Portal Mode

from mode import *

class CustomerPortalMode(Mode):
	def __init__(self, data):
		print(user.firstName)

	def redrawAll(self, canvas, data):
		canvas.create_text(200, 200, text='Customer', font='Helvetica 30 bold')