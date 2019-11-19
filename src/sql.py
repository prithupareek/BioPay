# Prithu Pareek - Created 11/19/19
# SQL Connect Class

import pymysql
import pymysql.cursors

class SQLConnection(object):
	def __init__(self, host, user, password, db):
		self.connection = pymysql.connect(host, user, password, db,
										  charset='utf8', cursorclass=pymysql.cursors.DictCursor)

	def login(self, username, password):
		try:
			with self.connection.cursor() as cursor:

				# get the record based on username and password
				sql = f"SELECT * FROM `user_info` WHERE `user_name`='{username}' AND `user_password`='{password}'"
				cursor.execute(sql)
				result = cursor.fetchone()

			self.connection.commit()

		finally:
			self.connection.close()

		return result