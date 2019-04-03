import requests
import random
import json

def carnival(proxies=None):
    print("<<<<< carnival cinema process started >>>>>")
    headers = {
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-GB,en;q=0.5',
        'Host':'service.carnivalcinemas.sg',
        'Origin':'https://carnivalcinemas.sg',
        'Referer':'https://carnivalcinemas.sg/',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux) Gecko/20100101 Firefox/60.0',
        'Token':'bXpFNVc2bHR1d3IvK3lSb3F3UHVFVDJqNE8rN2VWN3ZiNEJ0Mnd3TXorbz18aHR0cHM6Ly9jYXJuaXZhbGNpbmVtYXMuc2cvIy9ib29rU2VhdHw2MzY2NjEzNDAwNzA2MzAwMDB8cno4THVPdEZCWHBoajlXUWZ2Rmg='
    }
    MAIN_URL = 'https://carnivalcinemas.sg/#'
    proxies = '0'; #validate_proxies(proxies,MAIN_URL+'/')
    allmov_url = 'http://service.carnivalcinemas.sg/api/QuickSearch/GetAllMovieDetail?locationName=Mumbai'
    sdates_url = 'http://service.carnivalcinemas.sg/api/QuickSearch/GetShowDatesByMovies?location=Mumbai&movieCode={0}'
    times_url = 'http://service.carnivalcinemas.sg/api/QuickSearch/GetCinemaAndShowTimeByMovie?location=Mumbai&movieCode={0}&date={1}'
    link = 'https://carnivalcinemas.sg/#/{0}/{1}'
    if len(proxies)>0:
        ss = requests.session()
        ss.headers = headers
        ss.proxies = random.choice(proxies)
        ss.timeout = 10
    else:
        ss = requests.session()
        ss.headers = headers
    try:
        res_am = json.loads(ss.get(allmov_url).content)['responseMovies']
    except Exception as e:
        print(e)
        # raise Exception

    for film in res_am:
        fname = film['name']
        try:
            dates = json.loads(ss.get(sdates_url.format(fname)).content)['responseShowDates']
        except Exception as e:
            print(e)
            continue
        for date in dates:
            qdate = date['showDateValue']
            try:
                times = json.loads(ss.get(times_url.format(fname,qdate)).content)['responseCinemaWithShowTime']
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
                     # fileWrite(line)

    print("<<<<< carnival cinema process ended >>>>>")
