import sys
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

fslog = sys.argv[1]

# List peculiar offsets in us, relative to clock_early
peculiaroff = {"Ow": [6.28,"average from Date: 2019/01/08 00:00:00 and Date: 2019/01/23 00:00:00 Haystack"],
               "Oe": [6.32,"average from Date: 2019/01/08 00:00:00 and Date: 2019/01/23 00:00:00 Haystack"],
               "On": [1.35,"from multiple exp from Bonn"],
               "Is": [1.246, "VO009"]
               }

try:
    stime = sys.argv[2]
    etime = sys.argv[3]
    st = datetime.datetime.strptime(stime, "%Y.%j.%H:%M:%S.%f")
    et = datetime.datetime.strptime(etime, "%Y.%j.%H:%M:%S.%f")
except:
    # no range given, use all data
    st = datetime.datetime(1, 1, 1, 0)
    et = datetime.datetime(3000, 1, 1, 0)


vals = []
times = []
for l in open(fslog):
    if ("/gps-fmout/" in l ) or ("/gps-maser/" in l) or ("/gps-dbbcout2/" in l):
        ls = l.split("/")
        time = datetime.datetime.strptime(ls[0], "%Y.%j.%H:%M:%S.%f")
        val = -float(ls[2]) # negative, as fmout-gps is the "clock early" convention
        if (time > st) and (time < et):
            vals.append(val) # Seconds
            times.append(time)
    elif ("/fmout-gps/" in l ):
        ls = l.split("/")
        time = datetime.datetime.strptime(ls[0], "%Y.%j.%H:%M:%S.%f")
        val = float(ls[2]) # pos, as fmout-gps is the "clock early" convention
        if (time > st) and (time < et):
            vals.append(val) # Seconds
            times.append(time)
    elif ("!dbe_gps_offset?" in l ):
        ls = re.split(r"/|[?]0:|;",l.strip())
        time = datetime.datetime.strptime(ls[0], "%Y.%j.%H:%M:%S.%f")
        val = float(ls[3])
        if (time > st) and (time < et):
            vals.append(val) # Seconds
            times.append(time)

vals = np.array(vals)
times = np.array(times)

# Filter outliers
avg = np.average(vals)
std = np.std(vals)
diff = np.abs(vals-avg)
cut = 3*std
bad = np.where(diff>cut)
vals = np.delete(vals, bad)
times = np.delete(times,bad)

x = mdates.date2num(times) # decimal days
pf = np.polyfit(x, vals, 1)
p = np.poly1d(pf)

xx = np.linspace(x.min(), x.max(), 100)
dd = mdates.num2date(xx)

fn = os.path.basename(fslog)
station = fn[-6:-5].upper()+fn[-5:-4].lower()

reftime = dd[0].strftime("%Yy%jd%Hh%Mm%Ss") # Integer seconds
#, otherwise difx seems to behave strangely (create more jobs, output contains
#some strange timestamps etc.) HOWEVER: This could be since the "valid from"
#started after the first data chunk when I tested that on b19344. Could test
#that again. In any case, sub-second precision is not necessary here.

# Get fitted clock, add peculiar offset
refclock = p(xx.min()) + peculiaroff[station][0]*1e-6
rate = pf[0]/(24*3600) # convert to s/s
rate2 = 1e6*pf[0]/(24.0) # convert to us/hour for easy check
print("Infile: "+fslog)
print("Reftime {0}".format(reftime))
print("Refclock: {0} us".format(refclock*1e6))
print("Rate: {0} s/s ({1} us/h)".format(rate, rate2))
#print("NOTE: CHECK SIGN AND INCLUDE ANY PECULIAR OFFSET!")
print("**                  valid from           clock_early    clock_early_epoch        rate")
print("def {:s};  clock_early = {:s} : {:.3f} usec : {:s} : {:.3f}e-12; enddef;").format(station,reftime,refclock*1e6,reftime,rate*1e12)

f, a1 = plt.subplots(1)
a1.set_title(fn + ", Reftime: {:s},\n Clock: {:.3f} us, Rate: {:.3f} ps/s".format(reftime,refclock*1e6, rate*1e12))
a1.plot(times, 1e6*vals, 'o', label='data')
a1.plot(dd, 1e6*p(xx), '--', label='fit')
f.savefig(fn+".ratefit.png")
plt.show()
