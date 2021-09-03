import sys
import datetime
import numpy as np

snp = sys.argv[1]

lines = []
for l in open(snp):
    lines.append(l.strip())

recs = []
for i, line in enumerate(lines):
    lastline = lines[i-1]
    if ("disk_record=on" in line):
        beg = datetime.datetime.strptime(lastline, "!%Y.%j.%H:%M:%S")
    if ("data_valid=off" in line):
        end = datetime.datetime.strptime(lastline, "!%Y.%j.%H:%M:%S")
        # Filter out expired times
        if beg > datetime.datetime.now():
            recs.append([beg, end])
gaps = []
for i,r in enumerate(recs[1:]):
    prevend = recs[i-1][1]
    gap = (r[0]-prevend).total_seconds()
    if gap>100:
        gaps.append([str(prevend), gap])
gaps = np.array(gaps)
print(np.shape(gaps))
gaps_sort = gaps[gaps[:,1].argsort()]
print(gaps)
