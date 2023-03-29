import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    print("Успешно полдключена база данных")
    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('База данных успешно создана')
    except Error as e:
        print(f'Ошибка {e}')
    return cursor

connection = create_connection('localhost', 'root', 'password', 'base')
print(connection)
query_database = 'CREATE DATABASE base'
create_database(connection, query_database)



