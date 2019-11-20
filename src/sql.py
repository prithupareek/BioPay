# Prithu Pareek - Created 11/19/19
# SQL Connect Class

import pymysql
import pymysql.cursors

class SQLConnection(object):
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(host, user, password, db,
                                          charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    def login(self, username, password):

        with self.connection.cursor() as cursor:

            # get the record based on username and password
            sql = f"SELECT * FROM `user_info` WHERE `user_name`='{username}' AND `user_password`='{password}'"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def createAccount(self, username, password, name, acctType):
        with self.connection.cursor() as cursor:

            # Create a new record
            sql = f"INSERT INTO `user_info`(`user_name`, `user_password`, `user_firstName`, `user_typ`) VALUES ('{username}','{password}','{name}','{acctType}')"
            cursor.execute(sql)

            sql = "SELECT * FROM `user_info` ORDER BY `user_id` DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            # print(result)

        self.connection.commit()

        return result

    def findUserByUsername(self, username):
        with self.connection.cursor() as cursor:

            sql = f"SELECT * FROM `user_info` WHERE `user_name`='{username}'"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def closeConn(self):
        self.connection.close()