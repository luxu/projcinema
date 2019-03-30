
def we(proxies=None):
    print("<<<<< we cinema process started >>>>>")
    url = "https://www.wecinemas.com.sg/buy-ticket.aspx"
    proxies = validate_proxies(proxies,url)
    soup = scrape(url,proxies=proxies,lxml_grab=True)
    if soup ==0:
        return 0
    days = soup.xpath('/html/body/form/div[6]/table/tr/td/div/div/div[7]/div/table/tr[2]/td/table/tr/td[1]/table/tr[1]/td/table/tr/td/table/tr[6]/td/table/tr/td/table/tr[5]/td/table/tr/td/table/tr/td/table')
    for day in xrange(len(days)):
        date = days[day].xpath('tr[1]/td/div[@class="showtime-date-con"]/div[@class="showtime-date"]/text()')[0].split(' ')
        date = '/'.join([str(date[0]),str(month_string_to_number(date[1])),str(date[2].split(',')[0])])
        dm = soup.xpath('/html/body/form/div[6]/table/tr/td/div/div/div[7]/div/table/tr[2]/td/table/tr/td[1]/table/tr[1]/td/table/tr/td/table/tr[6]/td/table/tr/td/table/tr[5]/td/table/tr/td/table/tr[%s]/td/table/tr[3]/td'%str(day+1+2*day))
        for x in xrange(len(dm[0].xpath('table/tr'))):
            fname = dm[0].xpath('table/tr[%s]/td/h3/a/text()'%str(2+7*x))
            if len(fname)>0:
                times = dm[0].xpath('table/tr[%s]/td/table/tr[2]/td/div[@class="showtimes-but"]/a'%str(5+7*x))
                for t in times:
                    if fname[0].count('First Class'):
                        hall = '321 Clementi (First Class)'
                    else:
                        hall = '321 Clementi'
                    line = '"' + fname[0] + '","' + hall + '","' + 'WE-Clementi' + '","' + date + '","' + ' '.join([re.findall('\d+:\d+',t.text)[0],t.text[-2:]]) + '","' + t.xpath('@href')[0] + '"'
                    fileWrite(line)
    print("<<<<< we cinema process ended >>>>>")
