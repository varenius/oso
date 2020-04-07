#!/usr/bin/python
import socket, os, datetime, time, re, sys

# jive5ab info
ip = "129.16.208.51" # kare
port = "2621" # jive5ab control port
me = socket.gethostname()
DEBUG=False# Print jive5ab return messages, which are parsed for results

def fbcmd(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))
    sock.send(message.encode()) # convert message to bytestring
    if DEBUG:
        print('INFO: sent to '+ip+':'+port + ':' + message)
    data = sock.recv(1024)
    if DEBUG:
        print('INFO: answer: ', data.decode())
    sock.close()
    return data.decode()

scriptdir=os.path.dirname(os.path.realpath(__file__))
#vbsname = sys.argv[1] # filename to extract data from
vbsname = "gsa05_o8_0055.102731"
disk2fileout = scriptdir+"/"+vbsname+".vdif"

ans = ''
if os.path.exists(disk2fileout):
    ans = input("File " + disk2fileout + " exists! Type Yes to overwrite.")
else:
    ans="Yes"

if ans=="Yes":
    # Run disk2file to extract some time from scan selected by scan_set
    fbcmd("scan_set="+vbsname+":10s:10.1s")
    fbcmd("scan_set?")
    fbcmd("disk2file=" + disk2fileout + ":::w")
    print("WARNING: Please wait enough time for your disk2file extraction to finish.")
