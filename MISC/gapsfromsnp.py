import sys
import datetime
import numpy as np

snp = sys.argv[1]

lines = []
for l in open(snp):
    lines.append(l.strip())

gaps = []
beg = None
for i, line in enumerate(lines):
    lastline = lines[i-1]
    if ("data_valid=off" in line):
        beg = datetime.datetime.strptime(lastline, "!%Y.%j.%H:%M:%S")
    if ("disk_record=on" in line):
        end = datetime.datetime.strptime(lastline, "!%Y.%j.%H:%M:%S")
        # Filter out expired times
        if beg!=None and (beg > datetime.datetime.now()):
            gap = (end-beg).total_seconds()
            if gap > 60:
                gaps.append([str(beg), str(end), gap])
gaps = np.array(gaps)
gaps_sort = gaps[gaps[:,1].argsort()]
print(gaps)
