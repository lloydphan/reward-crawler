import mysql.connector as mysql
import logging


class MySql:
    __host = None
    __user = None
    __database = None
    __passwd = None
    db = None

    def __init__(self, host, user, passwd, database):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__database = database
        self.db = mysql.connect(
            host=self.__host,
            user=self.__user,
            passwd=self.__passwd,
            database=self.__database
        )

    def insert_value(self, values):
        cursor = self.db.cursor()
        query = "INSERT INTO products (code, image, description, price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, values)
        self.db.commit()
        logging.debug("Inserted:" + str(values))
