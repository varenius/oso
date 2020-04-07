# From FS log
#2019.170.16:40:20.11/fila10g_mode/,0xf0000f,,(128.000),128000000
#2019.170.16:40:20.11/mk5c_mode/VDIF_8000-1024-4-2,,,(128.),VDIF,8,128.,8000
#2019.170.16:40:20.11/form/geo
#2019.170.16:40:20.11&dbbc14f/bbc01=323.42,a,64.00
#2019.170.16:40:20.11&dbbc14f/bbc02=26.75,a,64.00
#2019.170.16:40:20.11&dbbc14f/bbc09=323.42,c,64.00
#2019.170.16:40:20.11&dbbc14f/bbc10=26.75,c,64.00
#2019.170.16:40:20.11&ifd14/ifa=1,agc,2,38000
#2019.170.16:40:20.11&ifd14/ifc=1,agc,2,38000
#2019.170.16:40:20.11&ifd14/lo=
#2019.170.16:40:20.11&ifd14/lo=loa,1220.00,usb,rcp,off
#2019.170.16:40:20.11&ifd14/lo=loc,1220.00,usb,lcp,off
# --> We want to extract RCP with center freq 1575.42, i.e. bbc01. 
#     We assume the BBCs are stored in this order, i.e. index [0] below is bbc01, index [1] is bbc02 etc...

# Define infile [vdif] and outfile [ASCII]
inf = "gsa05_o8_0055.102731.vdif"
outf = inf + ".bbc01.ascii"

import baseband
from baseband import vdif
import astropy.units as u

# Read file
fh = vdif.open(inf, 'rs', sample_rate=128*u.MHz) # Need to specify sample rate. Likely because truncated in time.
finf = fh.info()
print("Reading file ", inf, "...")
print("")
print(finf)

# Ensure file pointer is at beginning of file
fh.seek(0)
# Read all data until end
data = fh.read()
# Close infile
fh.close()
# Slice out bbc01 from all data
ind = 0 
print("...data read! Selecting bbc/thread index", ind, "...")
bbc01 = data[:, ind].astype(int)  # first bbc, converted to 4 integer states (2-bit)
print("...done!")
# Write data to outfile, ASCII values
print("Writing ASCII to ", outf)
with open(outf, 'w') as f:
    for b in bbc01:
        f.write("%s\n" % b)
