#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os

cmd = "ncftpput -u ivsincoming -p vlbi2000 ivs.bkg.bund.de / /usr2/log/`lognm`.log"

os.system(cmd)
