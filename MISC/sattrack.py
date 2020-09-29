import matplotlib.pyplot as plt
import numpy as np

# The list of links with TLE data
#GPS https://celestrak.com/NORAD/elements/gps-ops.txt
#GALILEO https://celestrak.com/NORAD/elements/galileo.txt
#GLONASS https://celestrak.com/NORAD/elements/glo-ops.txt
#BEIDOU https://celestrak.com/NORAD/elements/beidou.txt
#stations 'http://celestrak.com/NORAD/elements/stations.txt'

import time
from skyfield.api import Topos, load

#https://rhodesmill.org/skyfield/earth-satellites.html
gps = load.tle_file("https://celestrak.com/NORAD/elements/gps-ops.txt")
galileo = load.tle_file("https://celestrak.com/NORAD/elements/galileo.txt")
glonass = load.tle_file("https://celestrak.com/NORAD/elements/glo-ops.txt")
beidou = load.tle_file("https://celestrak.com/NORAD/elements/beidou.txt")
#satellites = gps + galileo + glonass + beidou
#satellites = galileo + glonass 
#satellites = gps + galileo
satellites = gps + beidou
#print('Loaded', len(satellites), 'satellites')

# create dict where we can fetch a satellite using its name as key
sats_by_name = {sat.name: sat for sat in satellites}

# Define observatory for az,el calculation
obs = Topos('57.393109 N', '11.917798 E') # OSO25m

# Define timerange. First time will be used for azelplot, 
# full range for SNAP file creation
#https://rhodesmill.org/skyfield/time.html
ts = load.timescale()
#tlist = [ts.now() + ]
tlist = ts.utc(2020, 9, 29, 12, 20, range(0,60*20,5))

# Make azelplot with names
fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='polar')
for sat in satellites:
    t = tlist[0]
    # Calculate difference, used to get alt/az further down
    difference = sat - obs
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()
    #alts.append(alt.degrees)
    #azs.append(az.degrees)
    #names.append(sat.name)
    ax.scatter(az.degrees, alt.degrees)
    ax.annotate(sat.name, (az.degrees, alt.degrees))
#ax.set_theta_zero_location("S")  # theta=0 at the top
#ax.set_theta_direction(-1)  # theta increasing clockwise
ax.set_rlim(bottom=90, top=20)
plt.show()

#gps1 = "GPS BIIR-10 (PRN 22)"
#glonass = "COSMOS 2457 (733)"
#galileo = "GSAT0104 (PRN E20)"
#gps2 = "GPS BIIF-2  (PRN 01)"
#beid = "BEIDOU-3 M2 (C20)"
target = sats_by_name[beid]
print("\" SNAP FILE FOR " + str(target))
for t in tlist:
    # Calculate difference, used to get alt/az further down
    difference = target - obs
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()
    ra, dec, distance = topocentric.radec()
    #print("!"+t.utc_strftime('%Y.%m.%d.%H:%M:%S'))
    #print("!"+t.utc_strftime('%Y.%m.%j.%H:%M:%S'))
    print("!"+t.utc_datetime().strftime('%Y.%j.%H:%M:%S'))
    a_r = ra.hms()
    b_r = dec.dms()
    a = [np.abs(i) for i in a_r]
    b = [np.abs(i) for i in b_r]
    asign = ""
    bsign = ""
    if a_r[0] <0:
        asign = "-"
    if b_r[0] <0:
        bsign = "-"
    print("source={},{}{:02d}{:02d}{:05.2f},{}{:02d}{:02d}{:05.2f},2000.0".format(target.name.split()[0],asign, int(a[0]), int(a[1]), a[2], bsign, int(b[0]), int(b[1]), b[2]))
    #print(alt, az)
