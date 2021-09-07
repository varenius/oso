#2021.250.03:33:53.61?ERROR dn  -20 DBBC3 multicast: no message received, multicast may not be running
#2021.250.03:33:58.36?ERROR dn   20 DBBC3 multicast: receiving multicast messages again.
import sys
import matplotlib.pyplot as plt
import datetime

fslogs = sys.argv[1:]

f,ax = plt.subplots()

for fslog in fslogs:
    for l in open(fslog):
        if "ERROR dn  -20 DBBC3 multicast: no message received, multicast may not be running" in l:
            time = l.split("?")[0]
            beg = datetime.datetime.strptime(time, "%Y.%j.%H:%M:%S.%f")
        elif "ERROR dn   20 DBBC3 multicast: receiving multicast messages again" in l:
            time = l.split("?")[0]
            end = datetime.datetime.strptime(time, "%Y.%j.%H:%M:%S.%f")
            ax.plot([beg, end], [1,1], markersize = "14")
            plt.show()
            sys.exit()
