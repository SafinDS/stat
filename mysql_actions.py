from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


class MysqlActions:
    def __init__(self):
        self.__conn = ''
        self.status_con = ''
        self.connect()


        self.query = ''
        self.lastrowid = 0
        self.error = ''

    def connect(self):
        """ Connect to MySQL database """

        db_config = read_db_config()

        try:
            # Connecting to MySQL database
            self.__conn = MySQLConnection(**db_config)
            #self.__conn.cmd_init_db()

            if self.__conn.is_connected():
                self.status_con = 'connected'
            else:
                self.status_con = 'connection failed'

        except Error as error:
            print(error)

    def close_connect(self):
        self.__conn.close()

    def query_one(self, query : str):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)

            row = cursor.fetchone()

            return row

        except Error as e:
            self.error = e

        finally:
            cursor.close()


    def query_all(self, query : str):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()

            return rows

        except Error as e:
            self.error = e

        finally:
            cursor.close()

    def execute_function(self, query: str):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)
            result_args = cursor.fetchone()
            return result_args[0]
        except Error as e:
            print(query, ' -- ERROR: ', e)
        finally:
            cursor.close()

    def insert(self, query: str):
        try:
            cursor = self.__conn.cursor()
            cursor.execute(query)

            if cursor.lastrowid:
                self.lastrowid = cursor.lastrowid
            else:
                self.lastrowid = 0

            self.__conn.commit()

        except Error as e:
            #cursor.rollback()
            self.error = e

        finally:
            cursor.close()

    # def __del__(self):
    #     self.__conn.close()


def call_find_by_isbn(query: str):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()

        # args = ['Круассан с варен сгущ 0,075кг п/уп (Краснодар', '4607104244635',
        #         'UnKnown', 1, 'НДС 10%', 'шт. или ед.']
        # query = """select insert_product() """
        cursor.execute(query)
        result_args = cursor.fetchone()
        return result_args[0]

        # print(result_args[0])

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

# if __name__ == '__main__':
#     call_find_by_isbn()
