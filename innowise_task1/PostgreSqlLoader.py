import pandas as pd
from sqlalchemy import create_engine

class PostgreSqlLoader:

    def __init__(self):
        pass

    @staticmethod
    def hostel_db_creation(connection):
        create_rooms_table = '''CREATE TABLE ROOMS
            (id INT PRIMARY KEY NOT NULL,
            name VARCHAR)'''
        create_students_table = '''CREATE TABLE STUDENTS 
             (birthday TIMESTAMP,
             id INT PRIMARY KEY NOT NULL,
             name VARCHAR NOT NULL,
             room INT NOT NULL,
             sex CHAR(1),
             FOREIGN KEY (room) REFERENCES rooms (id));'''
        connection.cursor().execute(create_rooms_table)
        connection.cursor().execute(create_students_table)
    @staticmethod
    def load_table(file_path, table_name):
        df_students = pd.read_json(file_path)
        print(df_students)
        engine = create_engine('postgresql://postgres:1111@127.0.0.1:5432/hostel_db')
        df_students.to_sql(table_name, engine, if_exists='append', index=False)

    @staticmethod
    def drop_tables(connection):
        connection.cursor().execute("DROP TABLE students")
        connection.cursor().execute("DROP TABLE rooms")

    @staticmethod
    def load_queries_results_to_json(queries: list, file_names: list):
        engine = create_engine('postgresql://postgres:1111@127.0.0.1:5432/hostel_db')
        for i in range(len(queries)):
            df = pd.read_sql_query(queries[i], con=engine)
            df.to_json(file_names[i], orient='split', index=False)

    @staticmethod
    def load_queries_results_to_xml(queries: list, file_names: list):
        engine = create_engine('postgresql://postgres:1111@127.0.0.1:5432/hostel_db')
        for i in range(len(queries)):
            df = pd.read_sql_query(queries[i], con=engine)
            df.to_xml(file_names[i], index=False)

