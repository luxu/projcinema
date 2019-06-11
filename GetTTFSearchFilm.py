import pymysql.cursors
from requests import get
from bs4 import BeautifulSoup as bs
import os
import configparser

# Carrega as configurações de arquivo externo
config = configparser.ConfigParser()
config.read('config.ini')

errors = []

def getMovies():
    sql = 'SELECT `Movie_name` FROM `movies`'
    fields = []
    return getConnection(sql,fields)

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

    if 'INSERT' in sql:
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, fields)
            connection.commit()
        finally:
            connection.close()
    else:
        try:
            with connection.cursor() as cursor:
                print(sql,fields)
                cursor.execute(sql, fields)
                return cursor.fetchall()
        finally:
            connection.close()

def getTTF(name):
    film = name.split()
    film = '+'.join(film)
    # url = 'https://www.imdb.com/find?ref_=nv_sr_fn&q=A+Ghost+Story&s=tt'
    url = f'https://www.imdb.com/find?ref_=nv_sr_fn&q={film}&s=tt'
    html = get(url)
    return bs(html.content, 'html.parser')

def main(movie_name,errors=None):
    soup = getTTF(movie_name)
    try:
        ttf = soup.find('td',class_="result_text").find('a')['href']
        imdb_id = ttf.split('/title/')[1][:-1]
        sql = 'SELECT `movies_id` FROM `movies` WHERE `Movie_name` = %s'
        fields = []
        fields.append(movie_name)
        rows = getConnection(sql,fields)
        movie_id = rows[0]['movies_id']
        sql = 'SELECT * FROM `movies_to_update` WHERE `imdb_id` = %s'
        fields = []
        fields.append(imdb_id)
        rows = getConnection(sql,fields)
        if rows:
            print(f'imdb_id:{imdb_id} already added!')
        else:
            print(f'imdb_id:{imdb_id} does not exist in base!')
            sql = 'INSERT INTO `movies_to_update` \
                (`imdb_id`,`movie_id`) VALUES (%s,%s)'
            fields = []
            fields.append(imdb_id)
            fields.append(movie_id)
            getConnection(sql,fields)
    except Exception as err:
        errors.append(f'Name Film.: {movie_name} have error.: {err}')
        # continue

def readFile(file):
    with open(file, encoding="utf8") as _file:
        text = _file.readlines()
    return text

if __name__ == '__main__':
    # file = '../film.txt'
    # for movie_name in readFile(file):
    #     print(movie_name)
    #     main(movie_name,errors)
    # main()
    # for film in getMovies()[:10]:
    for film in getMovies():
        movie_name = film['Movie_name'].strip()
        main(movie_name,errors)
    # if errors:
    #     for err in errors:
    #         print(err)
