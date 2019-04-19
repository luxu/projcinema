import requests
from bs4 import BeautifulSoup as bs
import random
from datetime import datetime, timedelta

data = []
warnings = []

def get_proxys():
    url = 'https://hidemy.name/ru/loginx'
    url1 = 'https://hidemy.name/api/proxylist.txt?out=plain&lang=ru'
    data = {'c':'976402971148490'}
    s = requests.session()
    s.get(url1)
    s.post(url,data=data)
    res = s.get(url1)
    result = res.text.split('\r\n')
    return result

def validate_proxies(proxies,url):
    proxys = []
    random.shuffle(proxies)
    qtdadeProxy = 2
    stime = datetime.now()+timedelta(minutes=30)
    for proxy in proxies:
        if stime < datetime.now():
            break
        bad_proxy = is_bad_proxy(proxy,url)
        if not bad_proxy:
            print(proxy, "APPROVED!")
            proxys.append({'http':proxy})
            if len(proxys) == qtdadeProxy:
                break
        elif str(bad_proxy)[0] == '5' and len(proxys) == 0:
	           print('This service is now unavailable (site from scraping is unavailable)')
    if len(proxys) == 0:
        return 0
    return proxys

def scrape(next_page_url, lxml_grab=None, proxies=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    # if proxies != 0 and len(proxies) > 0:
    # se tiver um array de proxies entra aqui
    if len(proxies) > 0:
        # separa o ip da porta
        plist = proxies[:]
        status_code = 0
        # debug()
        while len(plist) > 0 and status_code != 200:
            choiced = choice_proxy(plist)
            try:
                response = requests.get(
                    next_page_url,
                    headers=headers,
                    timeout=10,
                    proxies=choiced
                )
                status_code=response.status_code
            except:
                pass
            plist.remove(choiced)
    else:
        response=requests.get(
            next_page_url,
            headers=headers,
            timeout=10
        )
        if response.status_code != 200:
            return 0
    if lxml_grab is None:
        # soup = loadSoup(next_page_url)
        # soup = bs(response.text, "html.parser")
        soup = loadSoup(response)
    else:
        soup = paged(response.text)
    return soup

def loadSoup(response):
    try:
        # response = scraper.get(url)
        soup = bs(response.text, "html.parser")
        return soup
    except Exception as e:
        return 0

def choice_proxy(proxies):
    return proxies[random.randint(0,len(proxies)-1)]

def is_bad_proxy(pip,url):
    try:
        res = requests.get(
            url,
            proxies={'http':pip},
            headers={'User-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'},
            timeout=10
        )
    except Exception as detail:
        print("ERROR: %s" % detail)
        return 1
    if res.status_code ==200:
        return 0
    else:
        print(res.status_code)
        return 1

def paged(string):
    htmlparser = etree.HTMLParser()
    return etree.parse(StringIO(string),htmlparser)

def timeConvert(timeStr):
    time = timeStr.split(':')
    type = ''
    if (int(time[0]) > 11):
        if (int(time[0]) == 12):
            time = time[0] + ":" + time[1]
        else:
            time = str(int(time[0]) - 12) + ':' + time[1]
        type = ' PM'
    else:
        time = time[0] + ':' + time[1]
        type = ' AM'
    return time+type

def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

def dateConvert(dateStr):
    date = dateStr.split(' ')
    month = str(month_string_to_number(date[2]))
    year = str(datetime.now().year)
    return date[1]+'/'+month+'/'+year

def fileWrite(string):
    print(string)
    data.append(string)

def getData():
    return data

def setWarning(string):
    warnings.append(string)

def getWarning():
    return warnings

def debug():
    from pdb import set_trace
    set_trace()
