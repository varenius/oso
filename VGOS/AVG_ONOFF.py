import sys
import numpy as np

#infile = sys.argv[1]
infile = "/usr2/log/vo0132oe.log"

BBCdata = {}

for line in open(infile):
    if "VAL" in line:
        ls = line.split()
        det = ls[4]
        if len(det)==4:
            tcalJy = ls[11]
            if not "$$$" in tcalJy:
                if not det in BBCdata.keys():
                    BBCdata[det] = []
                BBCdata[det].append(float(tcalJy))

AVGdata = []
for bbc in sorted(BBCdata.keys()):
    dat = np.array(BBCdata[bbc])
    print(bbc, dat)
    avg = round(np.average(np.array(BBCdata[bbc])),3)
    AVGdata.append([bbc, avg])

print("bbcd={")
print("#BBC: Tcal[Jy]")
for d in AVGdata:
    print("    '{0}': {1:.3f},".format(d[0],d[1]))
print("}")
