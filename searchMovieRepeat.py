import csv
import pymysql.cursors
from time import sleep
from datetime import datetime
import os
import configparser

# Carrega as configurações de arquivo externo
config = configparser.ConfigParser()
config.read('config.ini')


def getConnection(sql,fields):
    if (os.name != 'posix'):
        connection = pymysql.connect(
            host="localhost",  # your host
            user="root",  # username
            passwd="iu00q71o",  # password
            db="2sw53e15l",  # name of the database
            connect_timeout=20,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
    else:
        connection = pymysql.connect(
            host="db-2sw53e15l.aliwebs.com",
            user="2sw53e15l",
            passwd=config['passwd'],
            db="2sw53e15l",
            connect_timeout=20,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

    if 'INSERT' in sql or 'UPDATE' in sql or 'DELETE' in sql:
        try:
            with connection.cursor() as cursor:
                # print(sql,fields)
                cursor.execute(sql, fields)
            connection.commit()
        finally:
            connection.close()
    else:
        try:
            with connection.cursor() as cursor:
                # print(sql,fields)
                cursor.execute(sql, fields)
                return cursor.fetchall()
        finally:
            connection.close()


def getMovies():
    sql = 'SELECT `Movie_name` FROM `movies`'
    fields = []
    return getConnection(sql,fields)

# with open('movie_data_old.csv') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     for row in readCSV:
#         movieName = row[0]

def delete_movie(id):
    if id:
        sql = 'DELETE FROM showtime WHERE id = %s'
        fields = [id]
        getConnection(sql,fields)
    else:
        print('Não veio ID nenhum')

def loadRepeteMovie():
    sql = 'SELECT s.id, s.Movie_Url, s.theatre_id, s.movie_id, s.start_at, COUNT(*) FROM showtime AS s ' \
          ' GROUP BY s.Movie_Url, s.theatre_id, s.movie_id, s.start_at ' \
          ' HAVING COUNT(*) > 1' \
          ' AND s.start_at > "2019-05-30"'
    fields = []
    return getConnection(sql, fields)

def main(rows):
    for row in rows:
        qtdade = row['COUNT(*)']
        print(f"({qtdade}){row['id']}\n{row['Movie_Url']}")
        sql = 'SELECT `id` FROM `showtime` WHERE `Movie_Url` like %s'
        fields = [f"%{row['Movie_Url']}%"]
        rowsId = getConnection(sql, fields)
        tam = len(rowsId)
        print(f'Tam.:{tam}')
        for i in rowsId[1:]:
            print(f"ID deleted.: {i['id']}")
            delete_movie(i['id'])
        break

if __name__=='__main__':
    start_time = datetime.now()
    while True:
        rows = loadRepeteMovie()
        size = len(rows)
        if size > 0:
            print(f'Size.: {size}')
            main(rows)
        else:
            print(f'Size.: {size} - End of repetitions! :-)')
            end_time = datetime.now()
            print(f'Working time - {end_time} - {start_time}')
            break
