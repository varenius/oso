#!/usr/bin/python
import sys, os

if (not len(sys.argv)==5) or (sys.argv[1]== "-h") or (sys.argv[1]=="--help"):
    print("Example usage: etransfer.py gyller gsi b22076 oe")
    sys.exit(1)

fb = sys.argv[1].lower()
destination = sys.argv[2].lower()
exp = sys.argv[3].lower()
ant = sys.argv[4].lower()

screenid = "etransfer_{0}_{1}_{2}".format(destination, exp, ant)
fbdir = "/mnt/etransfer/{0}/{1}_{2}".format(destination, exp, ant)

if destination == "gsi":
    sendcmd = "etc '{0}/*' 210.146.79.7#2642:/export/vlbi/data/{1}{2}/ --resume".format(fbdir, exp, ant)
elif destination == "vien":
    sendcmd = "etc '{0}/*' 193.170.79.54#2620:/gpfs/cdata/incoming/{1}/ --resume".format(fbdir, ant) 
elif destination == "bonn":
    sendcmd = "# DATA MOUNTED AT {0} FOR BONN TO FETCH, LET THEM KNOW!".format(fbdir)
elif destination == "skirner": # FOR TESTING ONLY
    sendcmd = "etc '{0}/*' skirner_x#43992:/mnt/disk0/eskil/ --resume".format(fbdir, exp, ant) 
else:
    print("ERROR: Destination {0} not supported yet. Aborting.".format(destination))
    sys.exit()

screen = "ssh {0} 'screen -dmS {1}'".format(fb, screenid)
mkdir = "ssh {0} \"screen -S {1} -p 0 -X stuff 'mkdir -p {2}^M'\"".format(fb, screenid, fbdir)
umount = "ssh {0} \"screen -S {1} -p 0 -X stuff 'fusermount -u {2}^M'\"".format(fb, screenid, fbdir)
mount = "ssh {0} \"screen -S {1} -p 0 -X stuff 'vbs_fs {2} -I {3}_{4}*^M'\"".format(fb, screenid, fbdir, exp, ant)
send = "ssh {0} \"screen -S {1} -p 0 -X stuff \\\"{2}^M\\\"\"".format(fb, screenid, sendcmd)

for c in [screen, mkdir, umount, mount, send]:
    print"Running command: {}".format(c)
    os.system(c)
