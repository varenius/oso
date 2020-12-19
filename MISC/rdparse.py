import sys
o8f = sys.argv[1]
vmf = sys.argv[2]

scans = []
for line in open(o8f):
    ls = line.split()
    sc = ls[0].split("/")[-1].split("_")[-1][0:8]
    scans.append(sc)

for line in open(vmf):
    ls = line.split()
    sc = ls[2].split("/")[-1].split("_")[-1][0:8]
    if sc in scans:
        lmod = line.replace("0,1,2,3,4,5,6,7", "2,3")
        lmod = lmod.replace("_all", "_B")
        lmod = lmod.replace("\n", "")
        print(lmod)
