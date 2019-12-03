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

        self.connection.commit()

        return result

    def findUserByUsername(self, username):
        with self.connection.cursor() as cursor:

            sql = f"SELECT * FROM `user_info` WHERE `user_name`='{username}'"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def getUserNameById(self, userid):
        with self.connection.cursor() as cursor:

            sql = f"SELECT `user_firstName` FROM `user_info` WHERE `user_id`='{userid}'"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def updateAccountBalance(self, userid):
        with self.connection.cursor() as cursor:

            sql = f'SELECT `user_balance` FROM `user_info` WHERE `user_id` = {userid}'
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def modifyAccountBalance(self, userid, amount):
        with self.connection.cursor() as cursor:

            sql = f"UPDATE `user_info` SET `user_balance` = '{amount}' WHERE `user_info`.`user_id` = {userid};"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def modifyAccount(self, userid, username, password, firstName):
        with self.connection.cursor() as cursor:

            sql = f"UPDATE `user_info` SET `user_name` = '{username}', `user_password` = '{password}', `user_firstName` = '{firstName}' WHERE `user_info`.`user_id` = {userid}"
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def getImage(self, userid):
        with self.connection.cursor() as cursor:

            sql = f'SELECT `user_face` FROM `user_info` WHERE `user_id` = {userid};'
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def updateFaceImage(self, userid, image):
        with self.connection.cursor() as cursor:

            sql = f'UPDATE `user_info` SET `user_face` = "{image}" WHERE `user_info`.`user_id` = {userid}'
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def updateFaceEncoding(self, userid, encoding):
        with self.connection.cursor() as cursor:

            sql = f"""UPDATE `user_info` SET `user_face_encoding` = '{encoding}' WHERE `user_info`.`user_id` = {userid};"""
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def createMerchantInventoryTable(self, userid):
        with self.connection.cursor() as cursor:

            sql = f"""
                    CREATE TABLE M_{userid}_Inventory(
                        item_id INT(100) AUTO_INCREMENT PRIMARY KEY,
                        item_name VARCHAR(100),
                        item_price DECIMAL(10, 2)
                    );
                   """
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def setInventoryReference(self, userid):
        with self.connection.cursor() as cursor:

            sql = f'UPDATE `user_info` SET `user_inventory` = "M_{userid}_Inventory" WHERE `user_info`.`user_id` = {userid}'
            cursor.execute(sql)
            result = cursor.fetchone()

        self.connection.commit()

        return result

    def getInventoryData(self, tableName):
        with self.connection.cursor() as cursor:

            sql = f'SELECT * FROM `{tableName}`;'
            cursor.execute(sql)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def getCartData(self, cartId):
        with self.connection.cursor() as cursor:

            sql = f'SELECT * FROM `{cartId}`;'
            cursor.execute(sql)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def getFaceEncodings(self):
        with self.connection.cursor() as cursor:

            sql = f"SELECT `user_id`, `user_face_encoding` FROM `user_info` WHERE `user_typ`='C'"
            cursor.execute(sql)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def transferMoney(self, senderId, recpId, amount):
        with self.connection.cursor() as cursor:

            sub = f"UPDATE `user_info` SET `user_balance` = (SELECT `user_balance` WHERE `user_id`={senderId}) - {amount} WHERE `user_id` = {senderId};"
            cursor.execute(sub)
            add = f"UPDATE `user_info` SET `user_balance` = (SELECT `user_balance` WHERE `user_id`={recpId}) + {amount} WHERE `user_id` = {recpId};"
            cursor.execute(add)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def addItemToInventory(self, inventoryTableName, itemName, itemPrice, itemQty, itemCost, itemCategory):
        with self.connection.cursor() as cursor:

            sql = f"INSERT INTO `{inventoryTableName}`(`item_name`, `item_price`, `item_qty`, `item_cost`, `item_category`) VALUES ('{itemName}',{itemPrice}, {itemQty}, {itemCost}, '{itemCategory}')"
            cursor.execute(sql)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def updateItemQty(self, inventoryTableName, itemName, itemPrice, itemQtyIncrease):
        with self.connection.cursor() as cursor:

            sql = f"UPDATE `{inventoryTableName}` SET `item_qty` = (SELECT `item_qty` WHERE `item_name`='{itemName}' AND `item_price`='{itemPrice}') + {itemQtyIncrease} WHERE `item_name`='{itemName}' AND `item_price`='{itemPrice}';"
            cursor.execute(sql)
            result = cursor.fetchall()

        self.connection.commit()

        return result


    def removeItemFromInventory(self, inventoryTableName, itemName, itemPrice):
        with self.connection.cursor() as cursor:

            sql = f"DELETE FROM `{inventoryTableName}` WHERE `item_name` = '{itemName}' AND `item_price` = {itemPrice}"
            cursor.execute(sql)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def logTransaction(self, senderId, recpId, amount, itemList):
        with self.connection.cursor() as cursor:

            # first create at row with the transaction info
            addSql = f"INSERT INTO `transaction_history`(`sender_id`, `recipient_id`, `trans_amount`) VALUES ({senderId},{recpId},{amount});"
            cursor.execute(addSql)
            getIdSql = f'SELECT @@IDENTITY AS "id";'
            cursor.execute(getIdSql)
            result = cursor.fetchall()
            transId = result[0]['id']
            
            # create the table for the cart
            cartTableSql = f"""
                    CREATE TABLE cart_{transId}(
                        item_id INT(255),
                        item_name VARCHAR(100),
                        item_price DECIMAL(10, 2),
                        item_qty INT(255)
                    );
                   """
            cursor.execute(cartTableSql)

            # add the items into the cart table
            for item in itemList:

                (prodId, name, price, qty) = (item[0], item[1], item[2], item[3])

                addToCartSql = f"INSERT INTO `cart_{transId}`(`item_id`, `item_name`, `item_price`, `item_qty`) VALUES ({prodId}, '{name}', {price}, {qty})"
                cursor.execute(addToCartSql)

            # add the cart tablename to the transaction history table
            addCartNameSql = f"UPDATE `transaction_history` SET `item_list`='cart_{transId}' WHERE `trans_id` = {transId};"
            cursor.execute(addCartNameSql)


        self.connection.commit()

        return result

    def getTransactionHistory(self, userid):
        with self.connection.cursor() as cursor:

            sql = f"SELECT * FROM `transaction_history` WHERE `sender_id` = {userid}"
            cursor.execute(sql)
            result = cursor.fetchall()

        self.connection.commit()

        return result

    def getPreviousCarts(self, userid):
        with self.connection.cursor() as cursor:

            listOfCarts = []

            getItemListNamesSql = f"SELECT `item_list` FROM `transaction_history`"
            cursor.execute(getItemListNamesSql)
            getItemListNamesSqlResult = cursor.fetchall()

            # for each cart table name
            for cart in getItemListNamesSqlResult:

                # get the cart table, but only the ids
                getCartTableSql = f"SELECT `item_id` FROM `{cart['item_list']}`"
                getCartTableSqlResult = cursor.execute(getCartTableSql)
                getCartTableSqlResult = cursor.fetchall()

                # convert dict to set
                cartSet = set([list(item.values())[0] for item in getCartTableSqlResult])

                # add the set to listOfCarts
                listOfCarts.append(cartSet)

        self.connection.commit()

        return listOfCarts

    def closeConn(self):
        self.connection.close()