
from ConnectToPostgresDB import ConnectToPostgresDB
from PostgreSqlLoader import PostgreSqlLoader

db = ConnectToPostgresDB()
connection = db.connectToDB(db_name="hostel_db")
PostgreSqlLoader.hostel_db_creation(connection)

rooms_file_path = input("Enter file_path to rooms file\n")
students_file_path = input("Enter file_path to students file\n")
output_format = input("Enter the output file format: json or xml\n")

PostgreSqlLoader.load_table(rooms_file_path, 'rooms')
PostgreSqlLoader.load_table(students_file_path, 'students')

rooms_lst_with_students_amount = '''SELECT rooms.name, count(students.id) 
                    FROM rooms INNER JOIN students ON rooms.id = students.room
                    GROUP BY rooms.name'''

rooms_with_min_student_age = ''' SELECT rooms.name
                        FROM rooms INNER JOIN students ON rooms.id = students.room
                        GROUP BY rooms.name
                        ORDER BY AVG(age(students.birthday))
                        LIMIT 5'''
rooms_with_max_age_diff = ''' SELECT rooms.name, (DATE_PART('day', MAX(students.birthday) - MIN(students.birthday))) as age_diff
                        FROM rooms INNER JOIN students ON rooms.id = students.room
                        GROUP BY rooms.name
                        ORDER BY age_diff DESC
                        LIMIT 5'''
rooms_with_different_sex = ''' SELECT rooms.name
                        FROM rooms INNER JOIN students ON rooms.id = students.room
                        GROUP BY rooms.name
                        HAVING COUNT(DISTINCT (students.sex)) = 2
                        LIMIT 5'''
queries_lst = [rooms_lst_with_students_amount, rooms_with_min_student_age, rooms_with_max_age_diff, rooms_with_different_sex]
filenames = ['res' + str(i) +'.' + output_format for i in range(len(queries_lst))]
if output_format == 'json':
    PostgreSqlLoader.load_queries_results_to_json(queries_lst, filenames)
elif output_format == 'xml':
    PostgreSqlLoader.load_queries_results_to_xml(queries_lst, filenames)

PostgreSqlLoader.drop_tables(connection)
connection.close()




