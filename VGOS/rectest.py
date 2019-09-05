import socket, os, datetime, time

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

def fbcmd(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))
    sock.send(message)
    print('INFO: sent to '+ip+':'+port + ':' + message)
    data = sock.recv(1024)
    print('INFO: answer: ', data)
    sock.close()


mode = "mode=VDIF_8192-8192-1-2" # 8192 byte UDP packet, 8Gbps data rate in total, 1 channel, 2 threads
# See also https://www.jive.nl/~verkout/evlbi/jive5ab-documentation-1.10.pdf sect. 7.1.
recsec = 2 # length to record in seconds
scan_name = "rectest_" + datetime.datetime.utcnow().strftime("%y%m%d_%H%M%S")

fbcmd(mode)
fbcmd("record=on:"+scan_name)
fbcmd("tstat?")
time.sleep(recsec)
fbcmd("tstat?")
fbcmd("record=off")
fbcmd("evlbi?")
fbcmd("scan_check?:4000000")
