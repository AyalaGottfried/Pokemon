import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="DB_Pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def insert(command):
    with connection.cursor() as cursor:
        cursor.execute(command)
        connection.commit()


def select(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def delete(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()


def update(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
