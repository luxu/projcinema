import requests
import cfscrape
import time
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
import sys
sys.path.append('..')
from ferramentas import util

class Gv:
    def __init__(self,proxies=None):
        print("<<<<< gv cinema process started >>>>>")
        proxies = ''#validate_proxies(get_proxys(),"https://www.gv.com.sg")
        dateArray = []
        dateArray.append(int(time.mktime(datetime.now().date().timetuple()) * 1000))
        for i in range(1, 7):
            newDate = (datetime.now() + timedelta(days=i)).date()
            unixtime = time.mktime(newDate.timetuple())
            dateArray.append(int(unixtime * 1000))
        for j in dateArray:
            sess = requests.session()
            if proxies != 0:
                # sess.proxies = {'http':choice_proxy(proxies)}
                sess.headers = {'User-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
            scraper = cfscrape.create_scraper(sess,delay = 15)
            url = "https://www.gv.com.sg/.gv-api/v2buytickets"
            print(str(j))
            payload = '{"cinemaId":"","filmCode":"","date":' + str(j) + ',"advanceSales":false}'
            headers = {
                'origin': "https://www.gv.com.sg",
                'accept-encoding': "gzip, deflate, br",
                'x_developer': "ENOVAX",
                'accept-language': "en-US,en;q=0.8",
                'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                'content-type': "application/json; charset=UTF-8",
                'accept': "application/json, text/plain, */*",
                'referer': "https://www.gv.com.sg/GVBuyTickets",
                'authority': "www.gv.com.sg",
                #'cookie': "__cfduid=d848fb1f803ddc4406880fd4dfceb7eca1511894040; __atuvc=1%7C49; JSESSIONID=0GRgIfUqqxpuAKKEsKrO95dt.undefined; _ga=GA1.3.640411893.1511894050; _gid=GA1.3.1043315194.1512306186; _gat=1",
                'cookie' : "__cfduid=db4aa507ed20675598e5500ff69d2dc841525162952; _ga=GA1.3.1520606575.1525163281; _gid=GA1.3.638964924.1525163281; _gat=1; publica_session_id=ef4d7367-4966-3ac1-c21b-b2ca57c6ec72; JSESSIONID=20AA6103A27DE2F707B4D624064B18EE",
                'cache-control': "no-cache",
                'path': '/.gv-api/v2buytickets?t=387_1525167473252'
                #'postman-token': "872dd435-61f6-8021-6e2f-cc9fba3a40cf"
            }
            headers = {
                'origin': 'https://www.gv.com.sg',
                'content-type': 'application/json; charset=UTF-8',
                'referer': 'https://www.gv.com.sg/GVBuyTickets',
                'x_developer': 'ENOVAX',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
            }
            try:
                response = scraper.post(url, data=payload, headers=headers)
            except Exception as e:
                print(e)
                warnings.append('(Gv) Error extraction %s '%(str(j)))
            try:
                data_return = ((response.content))
            except:
                continue
            data = json.loads(data_return)
            halls = (data['data']['cinemas'])
            # cinemas = getCinemas(proxies=proxies)
            for j in halls:
                # hall = cinemas[j['id']]
                hall = j['id']
                for k in j['movies']:
                    film = k['filmTitle']
                    for n in k['times']:
                        timeNow = n['time12'][:-2]+' '+n['time12'][-2:]
                        date = n['showDate'].replace('-','/')
                        link = "https://www.gv.com.sg/GVSeatSelection#/cinemaId/" + j['id'] + "/filmCode/" + k['filmCd'] + "/showDate/" + n['showDate'] + "/showTime/" + n['time24'] + "/hallNumber/" + n['hall']
                        line = '"' + film.strip() + '","' + hall + '","' + hall + '","' + date + '","' + timeNow.strip() + '","' + link + '"'
                        print(line)
                        # fileWrite(str(line.encode('ascii', 'ignore').decode('ascii')) )
        print("<<<<< gv cinema process ended >>>>>")

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
