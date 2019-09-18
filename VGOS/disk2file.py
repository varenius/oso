import socket
import time
ip = "127.0.0.1"
port = "2621"

# Simple script to set scan time and extract data with disk2file from jive5ab.
# Can of course also be done via vlbish, but at some point this was convenient.

def fbcmd(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))
    sock.send(message)
    print('INFO: sent to '+ip+':'+port + ':' + message)
    data = sock.recv(1024)
    print('INFO: answer: ', data)
    sock.close()
    return data

# Note: there must be spaces between the entities here, othewise it doesn't work
m = "scan_set = frb1ot_ow_no0024 : c : +10s "
fbcmd(m)
m = "scan_set?"
fbcmd(m)
m = "disk2file = /home/oper/eskil/frb1ot_oe_no0024_c+10s.vdif "
fbcmd(m)
time.sleep(2)
m = "disk2file?"
fbcmd(m)
