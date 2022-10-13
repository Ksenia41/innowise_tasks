import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class ConnectToPostgresDB:
    def __init__(self, db = "postgres", user ="postgres", passwd="1111", host="127.0.0.1",  port="5432"):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port


    def createDB(self, db_name: str):
        try:
            # Подключение к существующей базе данных
            connection = psycopg2.connect(user=self.user,
                                          password=self.passwd,
                                          host=self.host,
                                          port=self.port)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.db = db_name
            # Курсор для выполнения операций с базой данных
            cursor = connection.cursor()
            sql_create_database = f"create database {self.db}"
            cursor.execute(sql_create_database)
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                #connection.close()
                print("Соединение с PostgreSQL установлено, база дынных создана")
                self.db_connection = connection
                self.cursor = connection.cursor()
                return connection


    def connectToDB(self, db_name: str):
        if db_name:
            self.db = db_name
        try:
            connection = psycopg2.connect(database=self.db,
                                    user=self.user,
                                    password=self.passwd,
                                    host=self.host,
                                    port=self.port)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                print("Соединение с PostgreSQL установлено")
                self.db_connection = connection
                self.cursor = connection.cursor()
                return connection

    def stop_db_connection(self):
        try:
            self.db_connection.close()
        except (Exception) as exept:
            print("Can't close db connection", exept)

    def dropDB(self):

        drop_quiery = f'''DROP database {self.db}'''
        self.cursor.execute(drop_quiery)
        print("База", self.db, "удалена")


