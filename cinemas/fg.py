import requests
import cfscrape
from bs4 import BeautifulSoup as bs
import sys
sys.path.append('..')
from ferramentas import util
from pprint import pprint

def loadSoup(scraper,url):
    try:
        response = scraper.get(url)
        soup = bs(response.text,"html.parser")
        return soup
    except Exception as e:
        return 0

def debug():
    from pdb import set_trace
    set_trace()

def fg(proxies=None):
    print("<<<<< fg cinema process started >>>>>")
    url = "http://fgcineplex.com.sg/"
    proxies = ''#validate_proxies(proxies,url)
    sess = requests.session()
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 \
        (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
    scraper = cfscrape.create_scraper(sess,delay=40)
    soup = loadSoup(scraper,url)
    imgs = soup.select(".tour-img > a img")
    links = [i.a['href'] for i in soup.select(".show-read-more")]
    for img, link in zip(imgs, links):
        soup = carregarSoup(scraper,link)
        image = img['src']
        details = [f.find('span',class_="detial-last").text.strip() for f in soup.select('.firstul > li')]
        synopsis = [f.p.text.strip() for f in soup.select('.tabsmode2')]
        pprint(image)
        pprint(details)
        pprint(synopsis)
        print('*'*66)
    print("<<<<< fg cinema process ended >>>>>")
