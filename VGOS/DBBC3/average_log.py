import sys
import datetime
import numpy as np
#from datetime import timezone

def avg_dates(dates):
  # From https://stackoverflow.com/questions/19681703/average-time-for-datetime-list
  any_reference_date = datetime.datetime(1900, 1, 1)
  return any_reference_date + sum([date - any_reference_date for date in dates], datetime.timedelta()) / len(dates)

fslog = sys.argv[1]
sefdlog = sys.argv[2]
outfile = fslog + ".sefd"

#2020.132.18:00:01.04:data_valid=on
#2020.132.18:00:30.00:data_valid=off
scans = []
for l in open(fslog):
    if "data_valid=on" in l:
        time = l.split(":d")[0]
        beg = datetime.datetime.strptime(time, "%Y.%j.%H:%M:%S.%f")
        #beg = beg.replace(tzinfo=timezone.utc)
    if "data_valid=off" in l:
        time = l.split(":d")[0]
        end = datetime.datetime.strptime(time, "%Y.%j.%H:%M:%S.%f")
        #end = end.replace(tzinfo=timezone.utc)
        scans.append([beg, end])

lines = []
for l in open(sefdlog):
    if "BBC0" in l:
        lines.append(l)

# margin of data to include before and after scan
dt = datetime.timedelta(seconds = 1)
# Averaging time
at = datetime.timedelta(seconds = 5)

dates = []
sefds = []
sid = 0 # scan id
for i, line in enumerate(lines):
        ls = line.split()
        bbc=ls[2][3:6]+"l" # skip last colon, but add u/l
        # 
        if "001" in bbc:
            bbcvals = []
            dr = ls[0].split(".")[0] # use integer seconds only
            d = datetime.datetime.strptime(dr,'%Y-%m-%dT%H:%M:%S')
            #d = d.replace(tzinfo=timezone.utc)
            while (d > scans[sid][1]+dt): # if we are past the end of the scan, shift scan index
                print(line)
                if sid < len(scans)-1:
                    sid +=1
                else:
                    break
            if (d > scans[sid][0]-dt) and (d < scans[sid][1]+dt): # we are inside scan
                dates.append(d)
        # Now add bbc values, if inside scan
        if (d > scans[sid][0]-dt) and (d < scans[sid][1]+dt): # we are inside scan
            sefdl = ls[6]
            if sefdl=="INF":
                sefd = -1e9
            sefdl=float(sefdl)
            bbcvals.append(sefdl)
            if "064" in bbc:
                sefds.append(bbcvals)

# Avg values
avgd = []
avgs = []

# Buffer
td = []
ts = []
for i, d in enumerate(dates):
    if len(td)==0:
        td.append(dates[i])
        ts.append(sefds[i])
    elif len(td)==1:
        # Check if distance between old point and new point is bigger than average time
        dt = d - td[-1]
        if dt > at:
            # Add the previous point to the actual list of data
            avgd.append(dates[i])
            avgs.append(sefds[i])
            # Reset average buffers
            td = []
            ts = []
        # Add new point to average list, potentially starting a new chunk
        td.append(dates[i])
        ts.append(sefds[i])
    elif len(td)>1:
        # Check if distance between old point and new point is different from previous two points.
        # If yes, we start a new series
        dtPrev = td[-1] - td[-2]
        dtNew = d - td[-1]
        # Or, check if we have enough points to average.
        if ((dtNew != dtPrev) or (dtNew * len(td)>=at)):
            # We start a new series, so average the existing points together
            avgd.append(avg_dates(td))
            avgs.append(np.average(np.array(ts), axis=0))
            # Reset average buffers
            td = []
            ts = []
        # Add new point to average list, potentially starting a new chunk
        td.append(dates[i])
        ts.append(sefds[i])
        # Check if this is the last data segment; if so, add remaining points 
        # even if not full average period
        if i==len(dates)-1:
            avgd.append(avg_dates(td))
            avgs.append(np.average(np.array(ts), axis=0))

with open(outfile,"w") as of:
    of.write("#DATE [UTC], SEFDL for BBC1, BBC2...\n")
    for i in range(len(avgd)):
        of.write(avgd[i].strftime("%Y-%m-%dT%H:%M:%S.%f") + "," + ",".join([str(k) for k in avgs[i]]) + "\n")
