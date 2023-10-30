from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import sys

inf24h = sys.argv[1]
infint = sys.argv[2]
year = sys.argv[3]
data = {}
data['Oe'] = []
data['Ow'] = []
data['On'] = []

for line in open(inf24h):
    for tel in data.keys():
        if tel in line:
            ls = line.split("|")
            exp = ls[3]
            DOY = ls[4].replace(" ", "0")
            HHCMM = ls[5]
            DURR = ls[6].split(":")
            DUR = float(DURR[0]) + float(DURR[1])/60.0
            start_notz = datetime.strptime(year+DOY+HHCMM, '%Y%j%H:%M') # Assumes UTC
            start = start_notz.replace(tzinfo=pytz.UTC)
            stop = start + timedelta(hours=DUR)
            data[tel].append([exp, start, stop])

for line in open(infint):
    for tel in data.keys():
        if tel in line:
            ls = line.split("|")
            exp = ls[3]
            DOY = ls[4].replace(" ", "0")
            HHCMM = ls[5]
            DURR = ls[6].split(":")
            DUR = float(DURR[0]) + float(DURR[1])/60.0
            start_notz = datetime.strptime(year+DOY+HHCMM, '%Y%j%H:%M') # Assumes UTC
            start = start_notz.replace(tzinfo=pytz.UTC)
            stop = start + timedelta(hours=DUR)
            data[tel].append([exp, start, stop])
            
for tel in data.keys():
    cal = Calendar()
    cal.add('prodid', '-')
    cal.add('version', '2.0')
    cal.add('X-WR-TIMEZONE', 'UTC')
    for e in data[tel]:#[0:1]:
        event = Event()
        if tel == "On":
            title = "Geo S/X "+e[0]
        else:
            title=e[0]
        event.add('summary', title)
        event.add('dtstart', e[1])
        event.add('dtend', e[2])
        cal.add_component(event)
    f = open(tel+'.ics', 'wb')
    f.write(cal.to_ical())
    f.close()
