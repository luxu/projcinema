import requests
import cfscrape
from bs4 import BeautifulSoup as bs
import sys
sys.path.append('..')
from ferramentas import util
from pprint import pprint

class Fg:
    def __init__(self, proxies=None):
        print("<<<<< fg cinema process started >>>>>")
        url = "http://fgcineplex.com.sg/"
        sess = requests.session()
        sess.headers = {
            'User-Agent': 'Mozilla/5.0 \
            (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
        }
        scraper = cfscrape.create_scraper(sess,delay=40)
        soup = self.loadSoup(scraper,url)
        imgs = soup.select(".tour-img > a img")
        links = [i.a['href'] for i in soup.select(".show-read-more")]
        for link in links:
            soup = self.loadSoup(scraper,link)
            film = soup.select('.movie-list-indvisuals > h2 > b')[0].text
            for caixa in soup.select('.movie-cinema-main'):
                hall = caixa.find('div', class_='cinema-title').text.split('-')[1].strip()
                for caixa in soup.findAll('div', id='content'):
                    self.debug()
                    link = caixa.select('.cinema-time-table > ul > li > a')[0]['href']
                    time = caixa.select('.cinema-time-table > ul > li > a')[0].text.strip()
                    for dt in caixa.select('#tabs > li > a > span'):
                        date = dt.text.strip()
                        line = f'{film},{hall},{hall},{date},{time},{link}'
                        util.fileWrite(line )

        print("<<<<< fg cinema process ended >>>>>")

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
