import pymysql
import pymysql.cursors

# Connect to the datab
connection = pymysql.connect(host='35.237.8.126',
                             user='root',
                             password='password',
                             db='biometric_payment_database',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

userName = input("Enter your username: ")
userPass = input("Enter your password: ")
firstName = input("Enter your name: ")

try:
    with connection.cursor() as cursor:

        # Create a new record
        sql = f"INSERT INTO `user_info`(`user_name`, `user_password`, `user_firstName`) VALUES ('{userName}','{userPass}','{firstName}')"
        cursor.execute(sql)

        sql = "SELECT * FROM `user_info` ORDER BY `user_id` DESC LIMIT 1"
        cursor.execute(sql)
        print(cursor.fetchone())

    connection.commit()

finally:
    connection.close()