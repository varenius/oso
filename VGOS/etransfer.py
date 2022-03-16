#!/usr/bin/python
import sys, os
# example usage: script.py gsi vt2049 oe
destination = sys.argv[1]
exp = sys.argv[2]
ant = sys.argv[3]

if destination == "gsi":
    target = "210.146.79.7#2642:/export/vlbi/data/{0}{1}/".format(exp,ant)
    #target = "skirner_x#43992:/mnt/disk0/eskil/"
else:
    print("ERROR: Only GSI supported now. Aborting.")
    sys.exit()

# Get flexbuff info from mk5ad.ctl file
mk5ad = "/usr2/control/mk5ad.ctl"
ip = ""
port = ""
for line in open(mk5ad):
    if not line.startswith("*"):
        ls = line.split()
        ip = ls[0]
        port = ls[1]

if ip=="" or port=="":
    print("Flexbuff IP or port not found in " + mk5ad + ". Please check that file")
    sys.exit()

umountc = "ssh -t {0} \"fusermount -u /mnt/etransfer/gsi\"".format(ip)
mountc = "ssh -t {0} \"vbs_fs /mnt/etransfer/gsi -I '{1}_{2}*'\"".format(ip, exp, ant)
sendc = "ssh -t {0} \"etc '/mnt/etransfer/gsi/{1}*' {2} --resume\"".format(ip, exp, target)

#TEST COMMANDS
#screenc = "screen -dmS etc_transfer_{1}{2} ssh -t {0} \"etc '/mnt/etransfer/gsi/{1}*' {2} --resume\"".format(ip, exp, ant)
#screenc = "ssh -t {0} screen -dmS etc_transfer_{1}{2}".format(ip, exp, ant)
#sendc = "ssh -t {0} screen -S etc_transfer_{1}{2} -p 0 -X stuff \"etc '/mnt/etransfer/gsi/{1}_{2}*' {3} --resume^M\"".format(ip, exp, ant, target)
#for c in [umountc, mountc, screenc, sendc]:

for c in [umountc, mountc, sendc]:
    print"Running command: {}".format(c)
    os.system(c)
