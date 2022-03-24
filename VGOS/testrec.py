#!/usr/bin/python
import socket, os, datetime, time, re, sys

# Get flexbuff info from mk5ad.ctl file
mk5ad = "/usr2/control/mk5ad.ctl"
ip = ""
port = ""
me = socket.gethostname()
DEBUG=False # Print jive5ab return messages, which are parsed for results

def check_rate(scraw, tstat_rate, ev):
    sc = scraw.split(":")
    if DEBUG:
        print(sc)
    sc_pkt_size = int(sc[9].split()[0])
    sc_rate_re = re.match("([0-9\.]*)(.*)", sc[7].strip())
    sc_rate = int(sc_rate_re.group(1))
    sc_rate_unit = sc_rate_re.group(2)
    sc_nchan = int(sc[4].strip())
    sc_t_re = re.match("([0-9\.]*)(.*)", sc[6].strip())
    sc_t = sc_t_re.group(1)
    sc_t_unit = sc_t_re.group(2)
    # Scan_check packet size * n_pkts received / scan time
    evlbi_rate = int((sc_pkt_size * 8 * ev / float(sc_t)))/1.0e6
    message = ""
    
    # Print final rate comparison between the methods
    if tstat_rate < sc_rate * sc_nchan * 0.9 or tstat_rate > sc_rate * sc_nchan * 1.1:
        message = "WARNING: Rates from scan_check and tstat are not within 10% of each other! scan_check:"+ str(sc_rate * sc_nchan)+ "Mbps; tstat:"+ str(tstat_rate)+ "Mbps."
    elif tstat_rate < evlbi_rate * 0.9 or tstat_rate > evlbi_rate * 1.1:
        message = "WARNING: Rates from elvbi and tstat are not within 10% of each other! evlbi:"+ str(evlbi_rate)+ "Mbps; tstat:"+ str(tstat_rate)+ "Mbps"
    else:
        message = "Rate check OK!"
    summary = str(sc_nchan)+ " chans, "+ str(sc_rate * sc_nchan) + " " + sc_rate_unit + ", " + str(sc_t) + " s."
    return message, summary

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
    if DEBUG:
        print('INFO: sent to '+ip+':'+port + ':' + message)
    data = sock.recv(1024)
    if DEBUG:
        print('INFO: answer: ', data)
    sock.close()
    return data
recsec = 10 # length to record in seconds
scan_name = "testrec_" + me + "_"+datetime.datetime.utcnow().strftime("%y%m%d_%H%M%S")

version = fbcmd("version?").split(":")
jive5abv = version[2]
host = version[5]
rtime = fbcmd("rtime?").split(":")
rtime_space = rtime[2].strip()
rtime_perc = rtime[3].strip()
print("Found jive5ab version" + jive5abv + "running on" + host +"with free space: " + rtime_space + " (" + rtime_perc + ").")
datastream = fbcmd("datastream?")
if "thread" in datastream:
    print("NOTE: jive5ab datastreams are configured, this probably means multi-file recording. ")

mode = fbcmd("mode?").split(":")[1].strip()
print("Will record "+ str(recsec) + " sec to file " + scan_name + " with mode (set from FS?): " + mode + "...")

#Assume recording mode has already been sent by the FS, otherwise can send manually like this:
#mode = "mode=VDIF_8192-8192-1-2" # 8192 byte UDP packet, 8Gbps data rate in total, 1 channel, 2 bits
# See also https://www.jive.nl/~verkout/evlbi/jive5ab-documentation-1.10.pdf sect. 7.1.
#fbcmd(mode)

fbcmd("tstat=")
fbcmd("record=on:"+scan_name)
fbcmd("tstat=")
print("...recording any packets arriving...")
# Need to ensure tstat runs after data flows have started, so sleep 1 sec
time.sleep(1)
# Run first tstat
tstat1 = fbcmd("tstat=").split(":")
time.sleep(1)
# Run second tstat, against which to calcualte the difference
tstat2 = fbcmd("tstat=").split(":")
# Wait for rest of time to pass
time.sleep(recsec-2)
# Turn off recording
fbcmd("record=off")
print("...done! Checking stats...")

if DEBUG:
    print(tstat1)
    print(tstat2)
# Calculate rate from tstat=
tstat_bdiff = (float(tstat2[4])-float(tstat1[4]))
tstat_tdiff = (float(tstat2[1])-float(tstat1[1]))
tstat_rate = 8*tstat_bdiff / (tstat_tdiff * 1000**2)
#print("Tstat rate: {:4.0f} Mbps (including overheads)".format(tstat_rate)) #only python3
#print("Tstat rate: Mbps (including overheads):", tstat_rate) # python2 and python3

# Get rate from evlbi? and scan_check?
evlbi = fbcmd("evlbi?").split(":")
if DEBUG:
    print(evlbi)
ev_loss = int(evlbi[4].split()[0])
ev_loss_pct = re.match(".*?([0-9\.]*%).*", "".join(map(str, evlbi[4].split()[1:]))).group(1)
ev_ooo = int(evlbi[6].split()[0])
ev_ooo_pct = re.match(".*?([0-9\.]*%).*", "".join(map(str, evlbi[6].split()[1:]))).group(1)
ev_tot = int(evlbi[2])
# Check for packet loss
if ev_loss > 0:
        print "Warning: " + str(ev_loss) + " packets lost (" + ev_loss_pct + ")"

if ev_ooo > 0:
        print "Warning: " + str(ev_ooo) + " packets recevied out of order (" + ev_ooo_pct + ")"

scraw = fbcmd("scan_check?:4000000")
if " does not exist" in scraw:
    print("NOTE: Did not find " +scan_name+ " on disk. Checking for matching multifile suffixes...")
    mf_found = []
    for i in range(8):
        mfname = scan_name+"_"+str(i)
        set_mf = fbcmd("scan_set="+mfname) # Assume we have multi-file name instead
        scraw_mf = fbcmd("scan_check?:4000000")
        if not " does not exist" in scraw_mf:
            mf_found.append(i)
    if len(mf_found)==0:
        print()
        print("ERROR: scan_check did not find any data - investigate !!!" )
        print("Some (but not all) possible things to check:")
        print("- No mode= command sent to jive5ab since starting jive5ab?")
        print("- FiLa10G VDIF output not started? Check with FS command fila10g=sysstat.")
        print("  If it says 'output: stopped', and/or 'output 0 format: raw', then run the")
        print("  command 'fila10g=start vdif' and try again with a few testrec.py calls.")
        print("- Bad fibre connection from FiLa to flexbuff?")
        print("...exiting test... try again after changing something!")
        print("NOTE: To run jive5ab commands from FS, use 'mk5=' syntax e.g. mk5=datastream=clear")
        sys.exit(1)
    print("Found "+str(len(mf_found)) + " files on disk for this scan. Checking each:")
    for i in mf_found:
        mfname = scan_name+"_"+str(i)
        # Check rates for each multifile found
        res, fsum = check_rate(scraw_mf, tstat_rate/len(mf_found), ev_tot/len(mf_found))
        print("FILE: " + mfname + " RESULT: " + res + " SUMMARY: " + fsum)
       
else:
    print("Found single (possibly multi-thread) VDIF on disk called " + scan_name)
    res, fsum = check_rate(scraw, tstat_rate, ev_tot)
    print("FILE: " + scan_name + " RESULT: " + res + " SUMMARY: " + fsum)

