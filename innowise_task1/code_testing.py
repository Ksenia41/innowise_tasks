from ConnectToPostgresDB import ConnectToPostgresDB
from PostgreSqlLoader import PostgreSqlLoader
db = ConnectToPostgresDB()
connection = db.connectToDB(db_name="hostel_db")
PostgreSqlLoader.drop_tables(connection)