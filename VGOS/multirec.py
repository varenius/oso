#!/usr/bin/python
import socket, os, datetime, time, re, sys

# Get flexbuff info from mk5ad.ctl file
mk5ad = "/usr2/control/mk5ad.ctl"
ip = ""
port = ""
me = socket.gethostname()
DEBUG=False # Print jive5ab return messages, which are parsed for results

# Start jiveab instances manually on recodring machine with IP given in mk5ad.ctl, e.g. like this:
# for control_port in 3621 3622 3623 3624 3625 3626 3627 3628 ; do (/usr/local/bin/jive5ab-3.1.0-64bit-Debug -m 3 -p ${control_port} 1>/tmp/out${control_port} 2>&1 &); done

for line in open(mk5ad):
    if not line.startswith("*"):
        ls = line.split()
        ip = ls[0]
        port = ls[1]

if ip=="" or port=="":
    print("Flexbuff IP or port not found in " + mk5ad + ". Please check that file")
    sys.exit()

def fbcmdq(message, mp):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(mp)))
    sock.send(message)
    sock.close()
    print(datetime.datetime.utcnow().strftime("%y%m%d_%H%M%S"),"DEBUG,fmcmdq",message)

def fbcmd(message, mp):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(mp)))
    sock.send(message)
    if DEBUG:
        print('INFO: sent to '+ip+':'+mp + ':' + message)
    data = sock.recv(1024)
    if DEBUG:
        print('INFO: answer: ', data)
    sock.close()
    return data

recsec = float(sys.argv[1]) # length to record in seconds
scan_name = "testrec_" + me + "_"+datetime.datetime.utcnow().strftime("%y%m%d_%H%M%S")

# Set runtime net_ports
if me=="freja":
    np="2641"
elif me=="fulla":
    np="2631"
# Assuming default runtime 0 should not have netport where data is coming in
fbcmd("runtime={0}; net_port={1}{0}; mode=VDIF_8000-4096-8-2; mtu=9000; net_protocol=udpsnor:768M:256M:4; record=nthread::4; ".format("0",np),port)
# Then set rest from 1-8
for rt in range(1,9):
    cp = 3620+rt
    fbcmd("net_port={1}{0}; mode=VDIF_8000-4096-8-2; mtu=9000; net_protocol=udpsnor:768M:256M:4; record=nthread::4; ".format(str(rt),np),cp)
time.sleep(1)
# Start recording
for rt in range(1,9):
    cp = 3620+rt
    fbcmdq("record=on:{1}_{0}".format(str(rt),scan_name),cp)
print("sleep"+str(recsec))
time.sleep(recsec)
# Stop recording
for rt in range(1,9):
    cp = 3620+rt
    fbcmdq("record=off".format(str(rt)),cp)
for rt in range(1,9):
    cp = 3620+rt
    print(fbcmd("evlbi?".format(str(rt)),cp))
