import pymysql
from time import sleep
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
                cursor.execute(sql, fields)
            connection.commit()
        finally:
            connection.close()
    else:
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, fields)
                return cursor.fetchall()
        finally:
            connection.close()


def getCinemaCode(movie_id,theatre_id):
    sql = 'SELECT * FROM showtime AS s \
        WHERE s.movie_id = %s AND s.theatre_id = %s'
    fields = [movie_id,theatre_id]
    rows = getConnection(sql,fields)
    # codes = {}
    error = []
    # code_showTime = []
    # cont = 0
    save_film = []
    for row in rows[1:]:
        if not 'www.gv' in row["Movie_Url"]:
            save_film.append(row["Movie_Url"])
            # continue
        else:
            try:
                id = row["id"]
                movie_id = row["movie_id"]
                theatre_id = row["theatre_id"]
                linha = row["Movie_Url"].split('#')[1].split('/')
                # ['', 'cinemaId', '076', 'filmCode', '6516', 'showDate', '27-05-2019',
                # 'showTime', '2030', 'hallNumber', '6']
                cinemaId = linha[2]
                filmCode = linha[4]
                showDate = linha[6]
                showTime = linha[8]
                rt = f'{showTime} - {showDate} - {row["Movie_Url"]}'
                save_film.append(rt)
                hallNumber = linha[10]
                # cinemacode = linha[0].split('=')
                # txtSessionId = linha[1].split('=')
                # cont+=1
                # 'id': 332027, 'movie_id': 1599, 'theatre_id': 66 'Movie_Url'
                # print(f'{"*"*66}\n{id,movie_id,theatre_id, row["Movie_Url"]}')
                # print(f'{cinemaId,filmCode,showDate,showTime,hallNumber}')
                # save_film_gv.append(row["Movie_Url"])
            except Exception as err:
                # error.append(f'Film.: {row["Movie_Url"]}')
                # print(f'Film.: {row["Movie_Url"]} Error.: {err}')
                continue
    return save_film


def getMovies(movie_id,theatre_id):
    cinemacode='2001'
    txtSessionId='102844'
    Movie_Url = f'%https://tickets3.fgcineplex.com.sg/Ticketing/visSelectTickets.aspx?cinemacode={cinemacode}&txtSessionId={txtSessionId}&visLang=1%'
    sql = 'SELECT id, Movie_Url FROM showtime AS s \
            WHERE s.movie_id = %s \
            AND s.theatre_id = %s \
            AND s.Movie_Url like %s'
    fields = [movie_id,theatre_id,Movie_Url]
    return getConnection(sql,fields)


def getTheatre(id,id_end):
    sql = 'SELECT `Theatre_id` FROM `theatre` ' \
          'WHERE `Theatre_id` >= %s' \
          'AND `Theatre_id` <= %s'
    fields = [id,id_end]
    return getConnection(sql, fields)


def getFilmTableMovies():
    sql = 'SELECT `movies_id` FROM `movies`'
    fields = []
    return getConnection(sql, fields)


def getTableShowtime(idTheatre,movie_id):
    sql = 'SELECT id,movie_id,theatre_id,Movie_Url,start_at ' \
          'FROM `showtime` AS s ' \
          'WHERE s.start_at > %s ' \
          'AND s.theatre_id = %s '\
          'AND s.movie_id = %s'
    fields = ['2019-05-26',idTheatre,movie_id]
    return getConnection(sql, fields)


def delete_movie(id):
    if id:
        sql = 'DELETE FROM showtime WHERE id = %s'
        fields = [id]
        getConnection(sql,fields)
    else:
        print('Não veio ID nenhum')


def getTheatreAndMovie():
    id = '67'
    id_end = '79'
    arrayTheatre = getTheatre(id,id_end)
    size_theatre = len(arrayTheatre)
    for ex,id in enumerate(arrayTheatre):
        idTheatre = id['Theatre_id']
        print(idTheatre)
        for movie in getFilmTableMovies():
            arrayTableShowtime = getTableShowtime(idTheatre,movie['movies_id'])
            cont = 1
            id = 0
            for film in arrayTableShowtime:
                # 1612 - 72
                # 1617 - 72
                if film['movie_id'] != id:
                    id = film['movie_id']
                    if cont > 1:
                        print(f"{movie['movies_id']} - {idTheatre}")#\n{film}
                        print(cont)
                    else:
                        # print(f"{movie['movies_id']} - {idTheatre}")#\n{film}
                        cont=1
                else:
                    cont+=1


def getDeleteMovieDuplicated():
    arq = u'../listFilm.txt'
    with open(arq, encoding="utf8") as _file:
        texto = _file.readlines()
    seq = {}
    for t in texto:
        seq[str(t.split('-')[0])] = str(t.split('-')[1].strip())
    for key,value in seq.items():
        movie_id = key
        theatre_id = value
        # print(f'{"*"*66}\n{movie_id} - {theatre_id}\n{"*"*66}')
        codes = {}
        save_film = getCinemaCode(movie_id,theatre_id)
        sql = 'SELECT * FROM showtime AS s \
            WHERE s.movie_id = %s AND s.theatre_id = %s'
        fields = [movie_id,theatre_id]
        rows = getConnection(sql,fields)
        save_id = []
        # print(f'SizeSave_film.: {len(save_film)} - SizeRows.: {len(rows)}')
        for nro in range(1,len(save_film)):
            # print(f'Nro do save_film.: {nro}')
            for row in rows[1:]:
                # print(f'Movie_url de rows.: {row["Movie_Url"]}')
                if not 'www.gv' in row["Movie_Url"]:
                    if row["Movie_Url"] == save_film[nro]:
                        print(row['id'],row["Movie_Url"])
                        save_id.append(row['id'])
                        sleep(1)
                else:
                    # traco = '*'*66
                    # print(f'{traco}\n{row["Movie_Url"]}\n{save_film[nro].split(" - ")[2]}\n{traco}')
                    # ss = save_film[nro].split(' - ')
                    # print(ss[2])
                    # print(row["Movie_Url"])
                    # if row["Movie_Url"] == save_film[nro][2]:
                    if row["Movie_Url"] == save_film[nro].split(" - ")[2]:
                        print(row['id'],row["Movie_Url"])
                        save_id.append(row['id'])
                        sleep(0.1)
            if len(save_id) > 1:
                for id in save_id[1:]:
                    delete_movie(id)
                    print(f'Film Duplicate, deleted.: {id}')
                    sleep(0.1)
            save_id = []

if __name__ == '__main__':
    getDeleteMovieDuplicated()
