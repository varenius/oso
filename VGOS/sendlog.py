#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os

#cmd = "ncftpput -u ivsincoming -p PASSWORD ivs.bkg.bund.de / /usr2/log/`lognm`.log"
# Changed by Eskil 2022-08-18
cmd = "lftp -c 'set ftp:ssl-force true; open -u BKGPASSWORD ivs.bkg.bund.de; put -a /usr2/log/`lognm`.log; close; bye;' >> /usr2/log/lftp_BKG.log 2>&1"

os.system(cmd)
