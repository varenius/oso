import sys
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import argparse

#EXAMPLE USAGE:
#oper@gyller:~/eskil/eskil.oso.git/VGOS$ python fs_log_rate.py -l /mnt/raidz0/fs_logs/2019/b19351/b19351is.log -o test.png -s 2019.351.18:20:00.00 -e 2019.351.20:00:00.0
#Running with arguments: Namespace(etime=['2019.351.20:00:00.0'], logfile=['/mnt/raidz0/fs_logs/2019/b19351/b19351is.log'], outfile=['test.png'], stime=['2019.351.18:20:00.00'])
#Infile: /mnt/raidz0/fs_logs/2019/b19351/b19351is.log
#Reftime 2019y351d18h30m02s
#Refclock: 1.6681598888 us
#Rate: 1.83985298569e-13 s/s (0.000662347074849 us/h)
#*RESULT IN VEX FORMAT:
#*NOTE: Using peculiar offset 1.246 us from reference 'VO009 VgosDB from haystack'. Make sure this is correct!
#*                  valid from           clock_early    clock_early_epoch        rate
#def Is;  clock_early = 2019y351d18h30m02s : 1.668 usec : 2019y351d18h30m02s : 0.184e-12; enddef;
#*NOTE: You probably want to set the 'valid from' time to a at least a few minutes before the experiment start to make sure you cover all scans.

# List peculiar offsets in us, relative to clock_early
peculiaroff = {"Ow": [6.183,"from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
               "Oe": [6.211,"from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
               "On": [1.350,"from multiple exp from Bonn"],
               "Is": [1.268,"from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
               "Yj": [-0.108, "from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
               "O8": [5.18, "From Bob C, EVN: O8 = +5.78,  On = +1.95 --> O8 = 5.78-(1.95-1.350)=5.18"]
               }

parser = argparse.ArgumentParser()
parser.add_argument('-l','--logfile', nargs=1, help='FS log file to parse, e.g. b19344is.log.', required=True, type=str)
parser.add_argument('-s','--stime', nargs=1, help='Start time; ignore log values before this time. In FSLOG format, e.g. 2019.344.18:30:30.00. Note: decimal seconds (e.g. .0) is required. ', required=False, type=str)
parser.add_argument('-e','--etime', nargs=1, help='End time; ignore log values after this time. In FSLOG format, e.g. 2019.344.19:30:30.00. Note: decimal seconds (e.g. .0) is required. ', required=False, type=str)
parser.add_argument('-o','--outfile', nargs=1, help='Save plot of fit results to this filename. ', required=False, type=str)
args = parser.parse_args()

print("Running with arguments: {}".format(args))

fslog = args.logfile[0]
if not os.path.exists(fslog):
    print("Logfile {0} does not exist. Check that you gave the full path.".format(fslog))
    sys.exit(1)

if args.stime is not None:
    try:
        st = datetime.datetime.strptime(args.stime[0], "%Y.%j.%H:%M:%S.%f")
    except:
        print("Cannot parse start time. Check syntax.")
        sys.exit(1)
else:
    # no range given, use all data
    st = datetime.datetime(1, 1, 1, 0)
if args.etime is not None:
    try:
        et = datetime.datetime.strptime(args.etime[0], "%Y.%j.%H:%M:%S.%f")
    except:
        print("Cannot parse end time. Check syntax.")
        sys.exit(1)
else:
    # no range given, use all data
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
# Filtering should really be done first fitting once without filters, removing linear trend, then filter outliers. 
# But this works well enough for Onsala big jumps as is.
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

reftime = dd[0].strftime("%Yy%jd%Hh%Mm%Ss") # Integer seconds; we don't need more precision

# Get fitted clock, add peculiar offset
pecoff = peculiaroff[station]
refclock = p(xx.min()) + pecoff[0]*1e-6
rate = pf[0]/(24*3600) # convert to s/s
rate2 = 1e6*pf[0]/(24.0) # convert to us/hour for easy check
print("Infile: "+fslog)
print("Reftime {0}".format(reftime))
print("Refclock: {0} us [NO PECOFF]".format(p(xx.min())*1e6))
print("Refclock: {0} us".format(refclock*1e6))
print("Rate: {0} s/s ({1} us/h)".format(rate, rate2))
print("*RESULT IN VEX FORMAT:")
print("*NOTE: Using peculiar offset {0} us from reference '{1}'. Make sure this is correct!".format(pecoff[0], pecoff[1]))
print("*                  valid from           clock_early    clock_early_epoch        rate")
print("def {:s};  clock_early = {:s} : {:.3f} usec : {:s} : {:.3f}e-12; enddef;".format(station,reftime,refclock*1e6,reftime,rate*1e12))
print("*NOTE: You probably want to set the 'valid from' time to a at least a few minutes before the experiment start to make sure you cover all scans.")

f, a1 = plt.subplots(1)
a1.set_title(fn + ", Reftime: {:s},\n Clock: {:.3f} us, Rate: {:.3f} ps/s".format(reftime,refclock*1e6, rate*1e12))
a1.plot(times, 1e6*vals, 'o', label='data')
a1.plot(dd, 1e6*p(xx), '--', label='fit')
if args.outfile is not None:
    f.savefig(args.outfile[0])
    print("Rate-plot saved to " + args.outfile[0])
plt.show()
