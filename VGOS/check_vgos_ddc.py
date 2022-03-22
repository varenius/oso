#!/usr/bin/python
import socket, os, datetime, time, re, sys

# Get flexbuff info from mk5ad.ctl file
mk5ad = "/usr2/control/mk5ad.ctl"
ip = ""
port = ""
me = socket.gethostname()
DEBUG=False # Print jive5ab return messages, which are parsed for results

for line in open(mk5ad):
    if not line.startswith("*"):
        ls = line.split()
        ip = ls[0]
        port = ls[1]

if ip=="" or port=="":
    print("Flexbuff IP or port not found in " + mk5ad + ". Please check that file")
    sys.exit()

# Make plot
os.system("ssh oper@{0} python3 /data/check_data/checkdata.py {0} {1} 32 256 8".format(ip,port))
# Copy plot to FS computer, where gv_bpass will find it and (if open) display on screen
os.system("scp oper@{0}:/data/check_data/bandpass.pdf /usr2/oper/".format(ip))
