#!/usr/bin/python
import socket, os, datetime, time, re, sys

# Get flexbuff info from mk5ad.ctl file
mk5ad = "/usr2/control/mk5ad.ctl"
ip = ""
port = ""
me = socket.gethostname()
DEBUG=False # Print jive5ab return messages, which are parsed for results

# Figure out telescope name based on computer host name. Will be used for paths, filenames etc.
if me=="freja":
    tel = "S" # OTTS
elif me=="fulla":
    tel = "N" # OTTN

# Set output directory and temporary data filenames on the recording computer
mk5_dir = "/data/check_data/OTT-{0}".format(tel)
disk2fileout = mk5_dir + "/vgos_ddc_8_8.dat"
vmuxout = mk5_dir + "/vgos_ddc_1_64.dat"

for line in open(mk5ad):
    if not line.startswith("*"):
        ls = line.split()
        ip = ls[0]
        port = ls[1]

if ip=="" or port=="":
    print("Flexbuff IP or port not found in " + mk5ad + ". Please check that file")
    sys.exit()

def fbcmd(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))
    sock.send(message)
    #print('INFO: sent to '+ip+':'+port + ':' + message)
    data = sock.recv(1024)
    #print('INFO: answer: ', data)
    sock.close()
    return data

# Run disk2file to extract some time from the current scan selected by scan_set
fbcmd("scan_set?")
fbcmd("scan_set=:+3.0s:+0.2s")
fbcmd("disk2file=" + disk2fileout + ":::w")
time.sleep(1) # Wait for disk2file to finish

# If disk2file still running, abort
disk2file = fbcmd("disk2file?").split(":")[1].strip()
if disk2file=="active":
    print("disk2file running longer than expected, aborting it!")
    fbcmd("reset=abort")

# Kill any running vmux processes
os.system("ssh oper@{0} pkill -x vmux".format(ip))
# Convert from 8 threads 8 channels to 1 thread 64 channels
os.system("ssh oper@{0} /usr/local/difx-2.6.2_ompi_4.0.3_icc/bin/vmux -q {1} 8224 15625 0,1,2,3,4,5,6,7 {2}".format(ip,disk2fileout,vmuxout))
# Use m5 tools to create plots from the 64channel-data
os.system("ssh oper@{0} /home/oper/bin/chk_vgos_ddc_64ch.sh VDIF_65536-8192-64-2 {1} {2}".format(ip,vmuxout,mk5_dir))
# Copy plot to FS computer, where gv_bpass will find it and (if open) display on screen
os.system("scp oper@{0}:{1}/bandpass.ps /usr2/oper/".format(ip,mk5_dir))
