import requests

class Scrapping:
    ...

def scrape(next_page_url,lxml_grab=None,proxies=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    if proxies !=0 and len(proxies)>0:
        plist = proxies[:]
        status_code=0
        while len(plist)>0 and status_code!=200:
            choiced = choice_proxy(plist)
            try:
                response = requests.get(next_page_url, headers=headers,timeout=10,proxies=choiced)
                status_code=response.status_code
            except:
                pass
            plist.remove(choiced)
    else:
        response=requests.get(next_page_url, headers=headers,timeout=10)
        if response.status_code !=200:
            return 0
    if lxml_grab is None:
        soup = BeautifulSoup(response.text, "html5lib")
    else:
        soup = paged(response.text)
    return soup
