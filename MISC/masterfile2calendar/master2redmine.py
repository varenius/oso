from datetime import datetime, timedelta
import pytz
import sys
import numpy as np

inf24h = sys.argv[1]
infint = sys.argv[2]
year = sys.argv[3]

ds = []
for line in open(inf24h):
    ls = line.split("|")
    on = False
    oe = False
    ow = False
    if ("On" in line):
        on = True
    if ("Oe" in line):
        oe = True
    if ("Ow" in line):
        ow = True
    if on or oe or ow:
        exp = ls[3]
        DOY = ls[4].replace(" ", "0")
        HHCMM = ls[5]
        DURR = ls[6].split(":")
        DUR = float(DURR[0]) + float(DURR[1])/60.0
        tels = ls[7]
        corr = ls[9]
        start_notz = datetime.strptime(year+DOY+HHCMM, '%Y%j%H:%M') # Assumes UTC
        start = start_notz.replace(tzinfo=pytz.UTC)
        stop = start + timedelta(hours=DUR)
        ds.append([exp, on, oe, ow, start, stop, corr])

for line in open(infint):
    ls = line.split("|")
    on = False
    oe = False
    ow = False
    if ("On" in line):
        on = True
    if ("Oe" in line):
        oe = True
    if ("Ow" in line):
        ow = True
    if on or oe or ow:
        exp = ls[3]
        DOY = ls[4].replace(" ", "0")
        HHCMM = ls[5]
        DURR = ls[6].split(":")
        DUR = float(DURR[0]) + float(DURR[1])/60.0
        tels = ls[7]
        corr = ls[9]
        start_notz = datetime.strptime(year+DOY+HHCMM, '%Y%j%H:%M') # Assumes UTC
        start = start_notz.replace(tzinfo=pytz.UTC)
        stop = start + timedelta(hours=DUR)
        ds.append([exp, on, oe, ow, start, stop, corr])

ds = np.array(ds)
ds = ds[ds[:,4].argsort()]

#print("| START [UTC]      | DUR [h]  | STOP [UTC]       | EXP    | TEL | TEAM | SHIPPED | REMOVED | COMMENT |")     
#print("| --- | ---: | --- | --- | --- | ---  | --- | --- | --- |")     
print("| START [UTC] | DUR [h] | EXP | On | Oe | Ow | TEAM | CORRELATOR | SHIPPED | REMOVED | COMMENT |")     
print("| --- | --: | --- | --- | --- | --- | --- | --- | --- | --- | --- |")     
for e in ds:
    line = "| {0} | {1:4.1f} | {3} | {4} | {5} | {6} | | {2} | | | |"
    exp = e[0]
    on = "On" if e[1] else "-"
    oe = "Oe" if e[2] else "-"
    ow = "Ow" if e[3] else "-"
    start = e[4].strftime('%Y-%m-%d %H:%M')
    stop = e[5].strftime('%Y-%m-%d %H:%M')
    dur = (e[5]-e[4]).total_seconds()/3600.0
    corr = e[6]
    #print(line.format(start, dur, stop, e[0], tel))
    print(line.format(start, dur, corr, exp, on, oe, ow))
