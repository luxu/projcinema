from cinemas import gv, cathay, shaw, carnival, fg, we
from datetime import datetime, timedelta
from ferramentas import util
# shaw.cinemashaw()
# carnival.carnival()
# cathay.cathay()
# shaw
# fg.fg()
# we.We
# carnival.Carnival()
# gv.Gv()

def get_proxys():
    url = 'zproxy.lum-superproxy.io'
    data = {'c':'976402971148490'}
    # Port: 22225
    # User: lum-customer-hl_f1cb561b-zone-static
    # Password: nkcj53d47rpn
    'http://lum-customer-hl_f1cb561b-zone-static-country-br:nkcj53d47rpn@zproxy.lum-superproxy.io:22225'
    s = requests.session()
    s.get(url1)
    s.post(url,data=data)
    res = s.get(url1)
    result = res.text.split('\r\n')
    return result

TRYING_QUOTA    = 5
# data            = []
proxies         = '' #get_proxys()
# warnings        = []

shaw_status     = 0
carnival_status = 0
cathay_status   = 0
fg_status       = 0
we_status       = 0
gv_status       = 0

start_time = datetime.now()
##########  SHAW  ####################
# shaw_counter = 0
# while shaw_status == 0 and TRYING_QUOTA > shaw_counter:
#     try:
#         shaw.Shaw(proxies=proxies)
#         shaw_status = 1
#     except Exception as e:
#         print(e)
#         warnings.append("Shaw error scraping")
#     shaw_counter +=1

#########  CARNIVAL ################## OK
# carnival_counter=0
#display = Display(visible=0, size=(800, 600))
#display.start()
# while carnival_status == 0 and TRYING_QUOTA > carnival_counter:
#     try:
#         carnival.Carnival(proxies=proxies)
#         carnival_status = 1
#     except Exception as e:
#         print(e)
#         warnings.append("Carnival error scraping")
#     carnival_counter += 1
#display.stop()
#########  CATHAY  ################### OK
# cathay_counter = 0
# while cathay_status == 0 and TRYING_QUOTA > cathay_counter:
#     try:
#         # cathay(proxies=proxies)
#         cathay.Cathay(proxies=proxies)
#         # cathay(proxies=proxies)
#         cathay_status = 1
#     except Exception as e:
#         print(e)
#         warnings.append("Cathay error scraping")
#     cathay_counter +=1

########  FG  ##########################
fg_counter = 0
while fg_status == 0 and TRYING_QUOTA > fg_counter:
    try:
        # fg(proxies=proxies)
        fg.Fg(proxies=proxies)
        fg_status = 1
    except Exception as e:
        print(e)
        util.warnings.append("Fg error scraping")
    fg_counter += 1

######## WE ############################
# we_counter = 0
# while we_status == 0 and TRYING_QUOTA > we_counter:
#     try:
#         we(proxies=proxies)
#         we_status = 1
#     except Exception as e:
#         print(e)
#         warnings.append("We error scraping")
#     we_counter += 1

########  GV  #########################
# gv_counter = 0
# while gv_status == 0 and TRYING_QUOTA > gv_counter:
#     try:
#         gv(proxies=proxies)
#         gv_status = 1
#     except Exception as e:
#         print(e)
#         warnings.append("Gv error scraping")
#     gv_counter +=1
#######################################
end_time = datetime.now()

warnings = util.getWarning()
for war in warnings:
    print(war)

data = util.getData()
data = list(set(data))
with open('movie_data.csv','w') as f:
# with open('/home/sriabt/databaseUpload/movie_data.csv','w') as f:
    for i in data:
        f.write(i+'\n')

print('Working time - ',end_time - start_time)
print(end_time)
print("##########################################")
print("Script ends")
print("##########################################")
