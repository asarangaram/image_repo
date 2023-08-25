from dateutil import parser
import datetime

dates = ['2016-12-14 08:16:04',]

for date in dates:
    temp = parser.parse(date, yearfirst=True)
    print(temp)
