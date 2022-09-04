import pymysql
import mysql
import mysql.connector
from mysql.connector import Error


class Create_conn():


    def __init__(self, host_name, user_name, user_password, db_name):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.db_name = db_name
        self.connection = None
        self.get_connect()
        # self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db)
        self.cursor = None

    def get_connect(self):

        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password,
                database=self.db_name
            )
            # print("Connection to MySQL DB successful")

        except Error as e:
            print(f"The error '{e}' occurred")

    def insert(self, query):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

# my_con = Create_conn('localhost', 'root', 'merhaba0109', 'checks')
# my_con.get_connect()
# print(my_con.connection.cmd_statistics())

# def create_connection(host_name, user_name, user_password, db_name):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             passwd=user_password,
#             database=db_name
#         )
#         print("Connection to MySQL DB successful")
#     except Error as e:
#         print(f"The error '{e}' occurred")
#
#     return connection


# with create_connection('localhost', 'root', 'merhaba0109', 'checks') as con:
#    print(con.cmd_statistics())
#
# def get_table(con, name):
