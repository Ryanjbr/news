import datetime
import re
from dateutil import parser

str = 'Fri, 15 Apr 2022 07:00:00 GMT'
str2 = 'April 18, 2022'

# obj = datetime.datetime.strptime(str, '%d %m %Y %H:%M:S')

d = parser.parse(str)
d2 = parser.parse(str2)
print(int(d.strftime("%Y")))