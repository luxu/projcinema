import requests
import cfscrape
from bs4 import BeautifulSoup as bs
import sys
sys.path.append('..')

from ferramentas import util

def cathay(proxies = None):
    print("<<<<< cathay cinema process started >>>>>")
    url = "http://www.cathaycineplexes.com.sg/showtimes.aspx"
    sess = requests.session()
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 \
        (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
    scraper = cfscrape.create_scraper(sess,delay=40)
    try:
        response = scraper.get(url)
        status = response.status_code
        soup = bs(response.text,"html.parser")
        # soup = scrapping.paged(response.text)
    except Exception as e:
        print(e)
        status = 0
    if status!=200:
        response = requests.session()
        sess = requests.session()
        scraper = cfscrape.create_scraper(sess,delay=40)
        response = scraper.get(url)
        try:
            soup = scrapping.paged(response.text)
        except Exception as e:
            print(e)
            return 0
    divArray = [
        'ContentPlaceHolder1_wucSTPMS_tabs',
        'ContentPlaceHolder1_wucST_tabs',
        'ContentPlaceHolder1_wucST1_tabs',
        'ContentPlaceHolder1_wucST2_tabs',
        'ContentPlaceHolder1_wucST3_tabs',
        'ContentPlaceHolder1_wucST4_tabs',
        'ContentPlaceHolder1_wucST5_tabs',
        'ContentPlaceHolder1_wucST6_tabs',
    ]
    titles = [
        'AMK HUB',
        'CAUSEWAY POINT',
        'CINELEISURE ORCHARD',
        'DOWNTOWN EAST',
        'JEM',
        'PARKWAY PARADE',
        'THE CATHAY',
        'WEST MALL',
        'Platinum Movie Suite'
    ]
    # for i in range(0, len(divArray)):
    size = 0
    for _div in divArray:
        # div = divArray[i]
        title = titles[size]
        try:
            # tabs = soup.xpath('//div[@id="%s"]'%div)[0]
            tabs = soup.find('div', id=f'{_div}')
            # dates = tabs.xpath('ul/li/a/span[@class="smalldate"]/text()')
            dates = tabs.findAll('span', class_="smalldate")
            # containers = tabs.xpath('div[@class="tabbers"]')
            containers = tabs.find('div', class_="tabbers")
            size = 0 #len(containers)
            # for i in range(len(containers)):
            for container in containers:
                # movie_containers = container.xpath('div')
                movie_containers = container.find('div')
                date = dates[size]
                # timediv = date.split(' ')
                # date = str(timediv[0]) + '/' \
                # + str(month_string_to_number(timediv[1])) + '/' \
                # + str(datetime.now().year)
                # for j in range(len(movie_containers)):
                for movie in movie_containers:
                    hall = ''
                    # hall_div = movie_containers[j].xpath(
                    #     'div[@class="movie-desc"]/strong'
                    # )
                    hall_div = container.find('div', class_="movie-desc").strong
                    # [link.find('strong').text for link in soup.findAll('div', class_="movie-desc")]
                    if (len(hall_div) > 1):
                        hall = hall_div.text
                    film = ''
                    # film_div = movie_containers[j].xpath(
                    #     'div[@class="movie-desc"]/span[@class="mobileLink"]/strong/a'
                    # )
                    film_div = \
                        [link.find('span', class_="mobileLink").text \
                        for link in container.findAll('div', class_="movie-desc")]
                    if (len(film_div) > 0):
                        film = film_div
                    # if (film == ''):
                    #     continue
                    # if (hall == ''):
                    #     hall = title
                    # times = movie_containers[j].xpath(
                    #     'div[@class="movie-timings"] \
                    #     /div[@class="showtimeitem_time_pms"]/a'
                    # )
                    times = \
                        [fx.a for fx in container. \
                        findAll(class_="showtimeitem_time_pms")]
                    # from pdb import set_trace
                    # set_trace()
                    for k in times:
                        if k.get('data-href') is None:
                            continue
                        # line = '"' + film[0]
                        # line += '","' + title + '","' + hall + '","' + date
                        # line += '","' + k.span.text + '","'
                        # line += k.get('data-href') + '"'
                        line = f'{film[0]},{title}{hall},{date},{k.span.text},{k.get("data-href")}'
                        line = line.encode('ascii', 'ignore')
                        util.fileWrite(line)
                size=+1
        except Exception as e:
            # warnings.append('(Cathay) Error extraction %s '%(title))
            print(f'ERRO.: %s' % e)
            # raise ParserError
    print("<<<<< cathay cinema process ended >>>>>")
