from requests import get, post
import json
from os import chdir, path, remove
import cfscrape
from bs4 import BeautifulSoup as bs
import sys
sys.path.append('..')
from ferramentas import util
from pprint import pprint

class Shaw:
    def __init__(self,proxies=None):
        print("<<<<< shaw cinema process started >>>>>")
        cookies = {
            '_ga': 'GA1.2.1626712709.1554123147',
            '_gid': 'GA1.2.505595873.1554123147',
            'joe-chnlcustid': '1179089963',
            '_fbp': 'fb.1.1554123147788.60010941',
            'spd-custhash': '44cdff717f1a4ee634a3248bd96619be47d7963a',
            'pnctest': '1',
            '_gat_EcommerceTracker': '1',
            '_gat_gtag_UA_2073474_116': '1',
        }

        headers = {
            'Origin': 'https://www.shaw.sg',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,vi;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Content-Type': 'application/json;',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }

        data = '{"strAction":"MOVIE_LIST_VISUALGROUP","vStrEventVisualGroupName":"Now Showing"}'
        url = 'https://www.shaw.sg/DataForHandleBars'

        response = post(
            url,
            headers=headers,
            cookies=cookies,
            data=data
        )
        print("<<<<< shaw cinema process ended >>>>>")

    def writeJson():
        # Saves the folder being run in the script
        file = f'shaw.json'
        dict_save = json.dumps(
            response.json(),
            indent=4,
            ensure_ascii=False
        )
        try:
            file = open(file, "w", encoding='utf8')
            file.write(dict_save)
            file.close()
        except Exception as erro:
            print("There was an error loading file.")
            print("The error is: {}".format(erro))

    # Read JSON file
    def readJson():
        texts = json.loads(open('shaw.json', encoding='utf8').read())
        for cont in range(len(texts)):
            try:
                print(f'Name.: %s' % texts[cont]['movie_title_primary'])
                print(f'Duration.: %s' % texts[cont]['movie_duration'])
                print(f'Synopsis Short.: %s' % texts[cont]['movie_synopsis_short'])
                print(f'Cast.: %s' % texts[cont]['movie_cast_list'])
                print(f'Genre.: %s' % texts[cont]['movie_genre_name_list'])
                print(f'Media.: %s%s' %
                        ('https://ngsprodstorage1.blob.core.windows.net/prd',
                            texts[cont]['movie_release_media_path_reference']
                        )
                    )
                print('*'*66)

            except:
                continue

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
