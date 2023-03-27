#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys

# Give logfile path as argument, e.g.
# sendlog.py /usr2/log/vo3068oe.log
fslog = sys.argv[1]
bkgpassword = "ENTERPASS"
print("Sending logfile {}...".format(fslog))
cmd = "lftp -c 'debug -t 9; set ftp:ssl-force true; open -u {} ivs.bkg.bund.de; put -a {}; close; bye;' >> /usr2/log/lftp_BKG.log 2>&1".format(bkgpassword, fslog)
os.system(cmd)
print(cmd)
print("...done!")
