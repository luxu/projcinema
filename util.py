data = []

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
