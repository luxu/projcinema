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
        proxies = util.validate_proxies(proxies,url)
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
        '''
         for data in soup.select('.showtime-date'): print(data.text)
            # 17 APRIL 2019, WEDNESDAY

         namefilm = soup.select(
         '#DataListCinemas_DataListDate_0_DataListMovietitle_0 > tr > td > tr'
         )[0].text.strip()
         Disney's Dumbo (Digital)

         hrs = soup.select(
            '#DataListCinemas_DataListDate_0_DataListMovietitle_0_DataListShowtimes_0'
         )[0]

         '''



        '''
        line = '"' + fname[0] +
            '","' + hall +
            '","' + 'WE-Clementi' +
            '","' + date +
            '","' + ' '.join([re.findall('\d+:\d+',t.text)[0],t.text[-2:]]) +
            '","' + t.xpath('@href')[0] + '"'
        "Believer (Digital)",
        "321 Clementi",
        "WE-Clementi",
        "9/7/2018",
        "11:10 AM",
        "http://tickets.wecinemas.com.sg/
            Ticketing/visSelectSeats.aspx
            ?cinemacode=5001&txtSessionId=69539&args7=78F9C95434406353FDCE1E99790FFDA322645"
        '''
        self.debug()
        datas = soup.select('.showtime-date')
        for dt in soup.findAll('div', class_='showtime-date'):
            data = dt.text

        for t in soup.select('#DataListCinemas_DataListDate_0_DataListMovietitle_0 > tr'):
            t.find('h3')

        for r in soup.select(
            '#DataListCinemas_DataListDate_0_DataListMovietitle_0 > tr > td > tr > td > h3 > a'
        ):
            print(r.text)

        soup.select(
            '#DataListCinemas_DataListDate_0 #DataListCinemas_DataListDate_0_DataListMovietitle_0 tr:nth-of-type(2) > td > h3 > a')

        soup.select(
            '#DataListCinemas_DataListDate_0 #DataListCinemas_DataListDate_0_DataListMovietitle_0 tr:nth-of-type(5) .showtimes-but'
        )[0].text

        tag = [u"#DataListCinemas_DataListDate_0 #DataListCinemas_DataListDate_0_DataListMovietitle_0 tr:nth-of-type({}) > td > h3".format(i) for i in range(1,120)]
        for tg in tag: soup.select(tg)

        cx = soup.findAll('table', id='DataListCinemas_DataListDate_0_DataListMovietitle_0')
        for link in links:
            # url = u'{}{}'.format('https://www.wecinemas.com.sg', link)
            # soup = self.loadSoup(scraper, url)
            namefilm = soup.find('span', id='lblMovieTitle').text
            hall = "321 Clementi"
            date = ''
            linkFilm = ''
            showtimes = soup.select(
                '#DataListCinemas_DataListShowtimes_0'
            )[0].text.strip()
            line = u'"{}","{}","{}","{}","{}","{}"'.format(
                namefilm,
                hall,
                'WE-Clementi',
                date,
                showtimes,
                linkFilm
            )
            util.fileWrite(line)
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
