# Prithu Pareek - Created 11/19/19
# Merchant Portal Mode

from mode import *

class MerchantPortalMode(Mode):
	def __init__(self, data):
		print(user.firstName)

	def redrawAll(self, canvas, data):
		canvas.create_text(200, 200, text='Merchant', font='Helvetica 30 bold')