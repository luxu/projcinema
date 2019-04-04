import requests
import cfscrape
from bs4 import BeautifulSoup as bs
import sys
sys.path.append('..')
from ferramentas import util
from pprint import pprint

class We:
    def __init__(self,proxies=None):
        print("<<<<< we cinema process started >>>>>")
        url = "https://www.wecinemas.com.sg/buy-ticket.aspx"
        proxies = ''#validate_proxies(proxies,url)
        sess = requests.session()
        sess.headers = {
            'User-Agent': 'Mozilla/5.0 \
            (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
        }
        scraper = cfscrape.create_scraper(sess,delay=40)
        soup = self.loadSoup(scraper, url)
        # soup = scrape(url,proxies=proxies,lxml_grab=True)
        if len(soup) < 1:
            return 0
        links = [s['href'] for s in soup.select('h3 > a')]
        for link in links:
            url = u'{}{}'.format('https://www.wecinemas.com.sg', link)
            soup = self.loadSoup(scraper, url)
            namefilm = soup.find('span', id='lblMovieTitle').text
            imgfilme = soup.select('#imgMovieKeyArt')[0]['src']
            opening_date = soup.find('span', id='lblMovieReleaseDate').text
            director = soup.find('span', id='lblMovieDirector').text
            cast = soup.find('span', id='lblMovieCast').text
            ratings = soup.find('span', id='lblMovieRating').text
            duration = soup.find('span', id='lblMovieRuntime').text
            language = soup.find('span', id='lblMovieLanguage').text
            genre = soup.find('span', id='lblMovieGenre').text
            synopsis = soup.find('span', id='lblMovieSynopsis').text
            showtimes = soup.select('#DataListCinemas_DataListShowtimes_0')[0].text.strip()
            pprint(namefilm)
            pprint(imgfilme)
            pprint(opening_date)
            pprint(director)
            pprint(cast)
            pprint(ratings)
            pprint(duration)
            pprint(language)
            pprint(genre)
            pprint(synopsis)
            pprint(showtimes)
            print('*'*66)
        print("<<<<< we cinema process ended >>>>>")

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
