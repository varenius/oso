#!/usr/bin/python
import socket, os, datetime, time, re, sys

# Get flexbuff info from mk5ad.ctl file
mk5ad = "/usr2/control/mk5ad.ctl"
ip = ""
port = ""
me = socket.gethostname()
DEBUG=False# Print jive5ab return messages, which are parsed for results

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

recsec = 5 # length to record in seconds
scan_name = "testrec_" + me + "_"+datetime.datetime.utcnow().strftime("%y%m%d_%H%M%S")

print("")
rtime = fbcmd("rtime?").split(":")
rtime_space = rtime[2].strip()
rtime_perc = rtime[3].strip()
print("jive5ab has " + rtime_space + " of space left, or " + rtime_perc + " of total space.")
print("")
print("Will record "+ str(recsec) + " seconds of data to file " + scan_name + "...")

#Assume recording mode has already been sent by the FS, otherwise can send manually like this:
#mode = "mode=VDIF_8192-8192-1-2" # 8192 byte UDP packet, 8Gbps data rate in total, 1 channel, 2 bits
# See also https://www.jive.nl/~verkout/evlbi/jive5ab-documentation-1.10.pdf sect. 7.1.
#fbcmd(mode)

fbcmd("record=on:"+scan_name)
fbcmd("tstat?")
print("...recording...")
time.sleep(recsec)
tstat = fbcmd("tstat?").split(":")
fbcmd("record=off")
evlbi = fbcmd("evlbi?").split(":")
sc = fbcmd("scan_check?:4000000").split(":")
print("...done! Checking stats...")

if DEBUG:
    print(tstat)
tstat_re = re.match("([0-9\.]*)(.*)", tstat[3].split()[1])
tstat_rate = float(tstat_re.group(1))
tstat_unit = tstat_re.group(2)

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

if DEBUG:
    print(evlbi)
ev_loss = int(evlbi[4].split()[0])
ev_loss_pct = re.match(".*?([0-9\.]*%).*", "".join(map(str, evlbi[4].split()[1:]))).group(1)
ev_ooo = int(evlbi[6].split()[0])
ev_ooo_pct = re.match(".*?([0-9\.]*%).*", "".join(map(str, evlbi[6].split()[1:]))).group(1)
ev_tot = int(evlbi[2])

if ev_loss > 0:
        print "Warning: " + str(ev_loss) + " packets lost (" + ev_loss_pct + ")"

if ev_ooo > 0:
        print "Warning: " + str(ev_ooo) + " packets recevied out of order (" + ev_ooo_pct + ")"

# Scan_check packet size * n_pkts received / scan time
#print sc_pkt_size * 8 * ev_tot / float(sc_t)
evlbi_rate = int((sc_pkt_size * 8 * ev_tot / float(sc_t)))/1.0e6

if tstat_unit == "Gbps":
    tstat_rate = tstat_rate * 1000

print ""
if tstat_rate < sc_rate * sc_nchan * 0.9 or tstat_rate > sc_rate * sc_nchan * 1.1:
    print "Data rates returned by scan_check and tstat are not within 10% of each other! scan_check:", sc_rate * sc_nchan, "Mbps; tstat:", tstat_rate, "Mbps"
elif tstat_rate < evlbi_rate * 0.9 or tstat_rate > evlbi_rate * 1.1:
    print "Data rates returned by scan_check/elvbi and tstat are not within 10% of each other! scan_check/evlbi:", evlbi_rate, "Mbps; tstat:", tstat_rate, "Mbps"
else:
    print("No rate warnings, seems good!")

print ""
print "Recorded data contains ", sc_nchan, " channels, with a total data rate of", sc_rate * sc_nchan, sc_rate_unit + ", and a recorded time of " + sc_t + " seconds"
