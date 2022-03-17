#!/usr/bin/python
import sys, os

if (not len(sys.argv)==5) or (sys.argv[1]== "-h") or (sys.argv[1]=="--help"):
    print("Usage: etransfer.py FLEXBUFF CORRELATOR EXPERIMENT ANTENNA")
    print("Example usage: etransfer.py gyller gsi b22076 oe")
    print("Allowed values for CORRELATOR are: 'gsi vien shao bonn'. BUT: 'bonn' will just mount the data, not transfer.")
    print("INFO: This script will start a screen at the given flexbuff. In this screen, it will:")
    print("      - mkdir /mnt/etransfer/CORRELATOR/EXPERIMENT_ANTENNA (in case it doesn't exist)")
    print("      - fusermount -u /mnt/etransfer/CORRELATOR/EXPERIMENT_ANTENNA (in case it has already been used)")
    print("      - vbs_fs /mnt/etransfer/CORRELATOR/EXPERIMENT_ANTENNA -I 'EXP_ANT*' (to mount the data before transfer)")
    print("      - etc '/mnt/etransfer/CORRELATOR/EXPERIMENT_ANTENNA/*' TARGET' (where TARGET is the selected correlator standard data folder")
    print("NOTE: You can check the transfer by 'ssh flexbuff' and 'screen -r etransfer_CORRELATOR_EXP_ANT'.")
    print("NOTE: Once the transfer is done, you can 'exit' the screen.")
    sys.exit(1)

fb = sys.argv[1].lower()
destination = sys.argv[2].lower()
exp = sys.argv[3].lower()
ant = sys.argv[4].lower()

screenid = "etransfer_{0}_{1}_{2}".format(destination, exp, ant)
fbdir = "/mnt/etransfer/{0}/{1}_{2}".format(destination, exp, ant)

if destination == "gsi":
    sendcmd = "etc '{0}/*' 210.146.79.7#2642:/export/vlbi/data/{1}{2}/ --resume --udt-mss 9000".format(fbdir, exp, ant)
elif destination == "vien":
    sendcmd = "etc '{0}/*' 193.170.79.54#2620:/gpfs/cdata/incoming/{1}/ --resume".format(fbdir, ant) 
elif destination == "shao":
    sendcmd = "etc '{0}/*' 202.127.3.153:/vgos/vg03/{1}/{2}/ --resume".format(fbdir, exp, ant.capitalize()) 
elif destination == "bonn":
    sendcmd = "# DATA MOUNTED AT {0} FOR BONN TO FETCH, LET THEM KNOW!".format(fbdir)
elif destination == "skirner": # FOR TESTING ONLY
    sendcmd = "etc '{0}/*' skirner_x#43992:/mnt/disk0/eskil/ --resume --udt-mss 9000".format(fbdir, exp, ant) 
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
