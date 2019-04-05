import requests
import cfscrape
from bs4 import BeautifulSoup as bs
import json
import sys
sys.path.append('..')
from ferramentas import util
from pprint import pprint

class Carnival:
    def __init__(self,proxies=None):
        print("<<<<< carnival cinema process started >>>>>")
        # proxies = '0'; #validate_proxies(proxies,MAIN_URL+'/')
        link = 'https://carnivalcinemas.sg/#/{0}/{1}'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://carnivalcinemas.sg/',
            'Origin': 'https://carnivalcinemas.sg',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Token': 'ckg0amY4dTFGUGxDc2pwdjhrRmkzU2QzVmllNEZEY3hKMStlck8rbk9ZRT18aHR0cHM6Ly9jYXJuaXZhbGNpbmVtYXMuc2cvIy9Nb3ZpZXN8NjM2OTAwNTkwMzA2NTkwMDAwfHJ6OEx1T3RGQlhwaGo5V1FmdkZo',
        }

        params = (('locationName', 'Mumbai'),)
        allmov_url = 'https://service.carnivalcinemas.sg/api/QuickSearch/GetAllMovieDetail'
        response = requests.get(
            allmov_url,
            headers=headers,
            params=params
        )

        res_am = response.json()['responseMovies']
        {
        'code': 'CC00001198',
        'name': 'LUCIFER',
        'censor': 'PG13',
        'language': 'MALAYALAM',
        'duration': 170,
        'genre': '',
        'description': 'Lucifer is an upcoming Indian Malayalam-language \
            film directed by Prithviraj Sukumaran and written by Murali Gopy',
        'openingDate': '2019-03-29T00:00:00',
        'imageURL': 'CC00001198.JPG',
        'actor': ' MOHANLAL ,MANJU WARRIER',
        'director': ' Prithviraj  Sukumaran',
        'YouTubeURL': 'https://www.youtube.com/embed/zUMWAK4ZJ'
        }
        for film in res_am:
            fname = film['name']
            params = (
                ('location', 'Mumbai'),
                ('cinemaCode', 'STSG'),
                ('movieCode', film['name']),
            )
            sdates_url = requests.get(
                'https://service.carnivalcinemas.sg/api/QuickSearch/GetShowDateByMoviesAndCinema',
                headers=headers,
                params=params
            )
            try:
                dates = json.loads(sdates_url.content)['responseShowDates']
            except Exception as e:
                print(e)
                continue
            for date in dates:
                qdate = date['showDateValue']
                params = (
                    ('location', 'Mumbai'),
                    ('movieCode', 'Super Deluxe'),
                    ('date', '2019-04-05T00:00:00'),
                )
                times_url = requests.get(
                    'https://service.carnivalcinemas.sg/api/QuickSearch/GetCinemaAndShowTimeByMovie',
                    headers=headers,
                    params=params
                )
                try:
                    times = json.loads(times_url.content)['responseCinemaWithShowTime']
                except Exception as e:
                    print(e)
                    continue
                for t in times:
                    cinemaname = ' '.join(t['cinemaName'].split()[2:])
                    if cinemaname.count('Shaw Tower'):
                        cinemaname = 'Beach Road'
                    dd = qdate.split('T')[0].split('-')
                    dd.reverse()
                    if t['showTime'].count(','):
                        ts = [x.strip()[:-1] for x in t['showTime'].split(',')]
                        for ti in ts:
                            ti.strip()
                            if ti.count('T'):
                                ti = ti[:-1]
                            line = '"' + fname.strip() + '","' + cinemaname + '","' + 'Carnival' + '","' + '/'.join(dd) + '","' + ti.strip() + '","' + link.format(fname,fname).replace(' ','%20') + '"'
                            print(line)
                            # fileWrite(line)
                    else:
                         line = '"' + fname.strip() + '","' + cinemaname + '","' + 'Carnival' + '","' + '/'.join(dd) + '","' + t['showTime'].strip()[:-1] + '","' + link.format(fname,fname).replace(' ','%20') +'"'
                         print(line)
                         # fileWrite(line)

        print("<<<<< carnival cinema process ended >>>>>")

    def loadSoup(self,scraper,url):
        try:
            response = scraper.get(url)
            soup = bs(response.text,"html.parser")
            return soup
        except Exception as e:
            return 0

    def debug(self):
        from pdb import set_trace
        set_trace()
