import sys

inf = sys.argv[1]
lines = []
starts = []
for l in open(inf):
    ls = l.strip().split()
    sta = ls[1]
    if not sta in starts:
        lines.append(l)
        starts.append(sta)

with open(inf+".wash","w") as f:
    for l in lines:
        f.write(l)
