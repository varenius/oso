import matplotlib.pyplot as plt
import numpy as np
import sys
import datetime

inf = sys.argv[1]

dates = []
sefd = []

for line in open(inf):
    if not line.startswith("#"):
        ls = line.split(",")
        d = datetime.datetime.strptime(ls[0], "%Y-%m-%dT%H:%M:%S.%f")
        dates.append(d)
        sefd.append([float(k) for k in ls[1:]])

dates = np.array(dates)
sefd = np.array(sefd)
fig, (a, b, c, d) = plt.subplots(4, sharex=True)
a.plot(dates, sefd[:,0:8], color="black")
a.plot(dates, sefd[:,8:16], color="blue")
a.set_ylabel('Band A SEFD [Jy]]')
b.plot(dates, sefd[:,16:24], color="black")
b.plot(dates, sefd[:,24:32], color="blue")
b.set_ylabel('Band B SEFD [Jy]]')
c.plot(dates, sefd[:,32:40], color="black")
c.plot(dates, sefd[:,40:48], color="blue")
c.set_ylabel('Band C SEFD [Jy]]')
d.plot(dates, sefd[:,48:56], color="black")
d.plot(dates, sefd[:,56:64], color="blue")
d.set_ylabel('Band D SEFD [Jy]]')
#fig.suptitle(inf + "_SEFD.png")
#fig.savefig(inputFile + "CORR.png", dpi=300)
plt.show()
