import requests
import cfscrape
import sys
sys.path.append('..')
from ferramentas import util
from pprint import pprint
from log_pdb import salvarLog, lerLog

class Fg:
    def __init__(self, proxies=None):
        print("<<<<< fg cinema process started >>>>>")
        url = "http://fgcineplex.com.sg/"
        proxies = util.validate_proxies(proxies,url)
        soup = util.scrape(url,proxies=proxies)
        if soup == 0:
            return 0
        imgs = soup.select(".tour-img > a img")
        links = [i.a['href'] for i in soup.select(".show-read-more")]
        for link in links:
            # link = 'https://www.fgcineplex.com.sg/movies/details/3000000135'
            soup = util.scrape(link,proxies=proxies)
            # soup = self.loadSoup(link)
            film = soup.select('.movie-list-indvisuals > h2 > b')[0].text
            # verLog(film)
            # cada box do cinema é pego aqui: soup.select('.movie-cinema-box')
            # self.debug()
            for section in soup.select('.movie-cinema-box'):
                # nome do cinema:
                # caixa.find('div', class_='cinema-title').text.split('-')[1].strip()
                hall = section.find('div', class_='cinema-title').text.split('-')[1].strip()
                # verLog(hall)
                # cada conteúdo daqui: soup.findAll('div', id='content')
                # contém as datas e horas do cinema
                # self.debug()
                for div in section.select('#content > ul > li'):
                    date = div.select('.date')[0].text
                    cod = div.select('a')[0]['href']
                    div2 = section.select('#content')[0]
                    tabPane = div2.select(u'#{} > div > ul > li'.format(cod[1:]))
                    for tm in tabPane:
                        time = tm.a.text.strip()
                        link = tm.a['href']
                        line = f'{film},{hall},{hall},{date},{time},{link}'
                        util.fileWrite(line)
        print("<<<<< fg cinema process ended >>>>>")

    def loadSoup(url):
        try:
            response = requests.get(url)
            soup = bs(response.text, "html.parser")
            return soup
        except Exception as e:
            return 0

    def debug(self):
        from pdb import set_trace
        set_trace()
