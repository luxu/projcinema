from cinemas import gv, cathay, shaw, carnival, fg, we
from datetime import datetime, timedelta
from ferramentas import util
from log_pdb import salvarLog, lerLog

TRYING_QUOTA    = 5
# data            = []
proxies         = util.get_proxys()
# proxies         = ''
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
# # display = Display(visible=0, size=(800, 600))
# # display.start()
# while carnival_status == 0 and TRYING_QUOTA > carnival_counter:
#     try:
#         carnival.Carnival(proxies=proxies)
#         carnival_status = 1
#     except Exception as e:
#         print(e)
#         warnings.append("Carnival error scraping")
#     carnival_counter += 1
# # display.stop()

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

########  FG  ########################## OK
# fg_counter = 0
# while fg_status == 0 and TRYING_QUOTA > fg_counter:
#     try:
#         # fg(proxies=proxies)
#         fg.Fg(proxies=proxies)
#         fg_status = 1
#     except Exception as e:
#         print(e)
#         util.warnings.append("Fg error scraping")
#     fg_counter += 1

######## WE ############################
# we_counter = 0
# while we_status == 0 and TRYING_QUOTA > we_counter:
#     try:
#         we.We(proxies=proxies)
#         we_status = 1
#     except Exception as e:
#         print(e)
#         util.warnings.append("Fg error scraping")
#         # warnings.append("We error scraping")
#     we_counter += 1

########  GV  #########################
gv_counter = 0
while gv_status == 0 and TRYING_QUOTA > gv_counter:
    try:
        gv.Gv(proxies=proxies)
        gv_status = 1
    except Exception as e:
        print(e)
        util.warnings.append("Gv error scraping")
    gv_counter +=1
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
