import sys
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fslog = sys.argv[1]

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
        val = float(ls[2])
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

reftime = dd[0].strftime("%Y.%j.%H:%M:%S.%f")
refclock = p(xx.min())
rate = pf[0]/(24*3600) # convert to s/s
rate2 = 1e6*pf[0]/(24.0) # convert to us/hour for easy check
print("Infile: "+fslog)
print("Reftime {0}".format(reftime))
print("Refclock: {0} us".format(refclock*1e6))
print("Rate: {0} s/s ({1} us/h)".format(rate, rate2))
print("NOTE: CHECK SIGN AND PECULIAR OFFSET!")

f, a1 = plt.subplots(1)
a1.set_title(fslog)
a1.plot(times, 1e6*vals, 'o', label='data')
a1.plot(dd, 1e6*p(xx), '--', label='fit')
plt.show()
