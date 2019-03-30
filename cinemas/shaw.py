import sys
sys.path.append('..')

from ferramentas import scrapping

class Shaw:
    ...

def cinemashaw(proxies = None):
    print("<<<<< shaw cinema process started >>>>>")
    # url = "http://www.shaw.sg/sw_buytickets.aspx"
    url = "https://www.shaw.sg/movie"
    baseUrl = "https://www.shaw.sg/"
    proxies = ''
    # proxies = validate_proxies(proxies,url)
    # print('Proxies.: %s' % proxies)
    soup = scrapping.scrape(url,proxies=proxies) # linha 68
    if soup == 0:
        return 0
    viewState = soup.select('input#__VIEWSTATE')[0]['value']
    optionList = soup.select('select#ctl00_Content_ddlShowDate > option')
    for k in optionList:
        date = k['value']
        print(date)
        try:
            soup = scrapeUrlshaw(viewState, date,proxies=proxies)
            date = date.split('/')
            date = date[1] + '/' + date[0] + '/' + date[2]
            schedules = soup.select('table.panelSchedule')
            hall = ''
            film = ''
            for i in schedules:
                filmDiv = i.select('td.txtScheduleHeaderCineplex')
                if (len(filmDiv) > 0):
                    hall = filmDiv[0].text.split('(')[0].encode('ascii', 'ignore')
                else:
                    timeDiv = i.select('a.txtSchedule')
                    if (len(timeDiv) > 0):
                        film = timeDiv[0].text
                        for j in timeDiv[1:]:
                            time = j.text
                            time = time[:time.index('M') + 1]
                            link = ("http://www.shaw.sg/" + j['href'])
                            link = link.replace('/imax/index.htm?page=seatselect&', '/imax_ticketing/sw_seatselect.aspx?')
                            link = link.replace('/premiere/movies.html?page=seatselect&',
                                                '/premiere_ticketing/sw_seatselect.aspx?')
                            link = link.replace(' ', '%20')
                            line = '"' + film + '","' + hall + '","' + hall + '","' + date + '","' + time + '","' + link + '"'
                            fileWrite(line )
        except Exception as e:
            warnings.append('(Gv) Error extraction %s '%(str(date)))
            print(e)
    print("<<<<< shaw cinema process ended >>>>>")
