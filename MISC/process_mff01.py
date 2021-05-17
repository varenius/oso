# NOTE: This script assumes that we have a "fits" file with Tsys attached, and a ".gain" folder with the gain curve info.
# Simple summary to do obtain this:
#For some reason, DiFX attaches a nonsense gain curve to the data. 
#First we remove this using python2 (important, since there is some issues with opening the fits tables in python3 astropy):
#
#python2
#>>> import pyfits as fits
#>>> hdul = fits.open("mff01.fits", mode='update')
#>>> hdul.info()
#>>> hdul.info()
#Filename: mff01.fits
#No.    Name      Ver    Type      Cards   Dimensions   Format
#  0  PRIMARY       1 GroupsHDU       30   ()      0 Groups  0 Parameters
#  1  ARRAY_GEOMETRY    1 BinTableHDU     55   2R x 8C   [8A, 3D, 3E, 0D, 1J, 1J, 3E, 1E]   
#  2  SOURCE        1 BinTableHDU     89   3R x 26C   [1J, 16A, 1J, 4A, 1J, 32E, 32E, 32E, 32E, 32E, 32E, 1D, 1D, 8A, 1D, 1D, 32D, 8A, 8A, 32D, 1D, 1D, 1E, 1D, 1D, 1D]   
#  3  ANTENNA       1 BinTableHDU     52   2R x 13C   [1D, 1E, 8A, 1J, 1J, 1J, 1J, 1A, 32E, 0E, 1A, 32E, 0E]   
#  4  FREQUENCY     1 BinTableHDU     35   1R x 6C   [1J, 32D, 32E, 32E, 32J, 32J]   
#  5  INTERFEROMETER_MODEL    1 BinTableHDU     82   30R x 20C   [1D, 1E, 1J, 1J, 1J, 1J, 1E, 32E, 192D, 6D, 192D, 6D, 1E, 1E, 192D, 6D, 192D, 6D, 1E, 1E]   
#  6  CALC          1 BinTableHDU     75   5R x 11C   [1D, 1D, 1D, 1D, 1A, 2D, 1A, 1D, 1D, 1D, 1D]   
#  7  MODEL_COMPS    1 BinTableHDU     86   30R x 21C   [1D, 1J, 1J, 1J, 1J, 1D, 1D, 1D, 1D, 1D, 1D, 32E, 32E, 1E, 1E, 1D, 1D, 32E, 32E, 1E, 1E]   
#  8  UV_DATA       1 BinTableHDU     93   1614R x 13C   [1E, 1E, 1E, 1D, 1D, 1J, 1J, 1J, 1J, 1E, 128E, 0J, 81920E]   
#  9  PHASE-CAL     1 BinTableHDU     61   34R x 17C   [1D, 1E, 1J, 1J, 1J, 1J, 1D, 128E, 224D, 224E, 224E, 224E, 128E, 224D, 224E, 224E, 224E]   
# 10  GAIN_CURVE    1 BinTableHDU     62   0R x 19C   [1J, 1J, 1J, 32J, 32J, 32J, 32J, 32E, 192E, 192E, 32E, 32J, 32J, 32J, 32J, 32E, 192E, 192E, 32E]   
#>>> hdul.__delitem__(10) # Remove GAIN-CURVE table, no 10 in list
#>>>hdul.flush()
#>>>hdul.close()
#
# Then, append the correct info using casa:
#casa -c casa-vlbi.git/gc.py mff01oe+ow.antab mff01oe+ow.gain
#casa -c casa-vlbi.git/append_tsys.py mff01oe+ow.antab mff01.fits
#
# If the above has been done, we can run the script... 
import numpy as np
import sys

# NOTE: The infits, gainfile, e and frscan needs to be defined
infits = "mff01.fits"
gainfile = "mff01oe+ow.gain"
e = "mff01" # Experiment name
frscan = "1" # Scan number to use for single-band fringe-finding. To find
             # a good one, check e.g. the "listobs output" and/or any observing notes.

# Should not need to change anything below
bands = ["A", "B", "C","D"] # relevant after split1
ms = e+".ms"
gaint = e+".ct.gain"#gain
tsyst = e+".ct.tsys" #tsys
bpt = e+".ct.bandpass" # bandpass
act = e+".ct.accor" # accor
split1ms = ms+".split1"
split2ms = ms+".split2"
frt = e+".ct.sbfring" # fringsb
frmbt = e+".ct.mbfring" # fringmb

whattodo = {'load_data': True,
            'listobs': True,
            'gencal': True,
            'pcflag': True,
            'antflag': True,
            'edgeflag': True,
            'accor': True,
            'rflag1': True,
            'applycal' :True,
            'split1' :True,
            'listobs1': True,
            # Steps below done per band
            'fring' : True,
            'bpass' : True,
            'applycal2' :True,
            'split2' :True,
            'listobs2': True,
            'getflux': True,
            }

#TODO: Get IF from ms instead of static list
ifs = np.array([
# IF LOWEREDGE[GHz]  WIDTH[kHz]   CHANNELWIDTH[kHz]
[ 1-1, 3.00040000,32000.0020,100.0000],
[ 2-1, 3.03240000,32000.0020,100.0000],
[ 3-1, 3.06440000,32000.0020,100.0000],
[ 4-1, 3.19240000,32000.0020,100.0000],
[ 5-1, 3.28840000,32000.0020,100.0000],
[ 6-1, 3.35240000,32000.0020,100.0000],
[ 7-1, 3.41640000,32000.0020,100.0000],
[ 8-1, 3.44840000,32000.0020,100.0000],
[ 9-1, 5.24040000,32000.0020,100.0000],
[10-1, 5.27240000,32000.0020,100.0000],
[11-1, 5.30440000,32000.0020,100.0000],
[12-1, 5.43240000,32000.0020,100.0000],
[13-1, 5.52840000,32000.0020,100.0000],
[14-1, 5.59240000,32000.0020,100.0000],
[15-1, 5.65640000,32000.0020,100.0000],
[16-1, 5.68840000,32000.0020,100.0000],
[17-1, 6.36040000,32000.0020,100.0000],
[18-1, 6.39240000,32000.0020,100.0000],
[19-1, 6.42440000,32000.0020,100.0000],
[20-1, 6.55240000,32000.0020,100.0000],
[21-1, 6.64840000,32000.0020,100.0000],
[22-1, 6.71240000,32000.0020,100.0000],
[23-1, 6.77640000,32000.0020,100.0000],
[24-1, 6.80840000,32000.0020,100.0000],
[25-1,10.20040000,32000.0020,100.0000],
[26-1,10.23240000,32000.0020,100.0000],
[27-1,10.26440000,32000.0020,100.0000],
[28-1,10.39240000,32000.0020,100.0000],
[29-1,10.48840000,32000.0020,100.0000],
[30-1,10.55240000,32000.0020,100.0000],
[31-1,10.61640000,32000.0020,100.0000],
[32-1,10.64840000,32000.0020,100.0000]])

def getPCALchans(IF):
    PCALchans = []
    fmin = IF[1]*1e3 # to MHz
    fmax = fmin + IF[2]*1e-3 # MHz
    chres = IF[3]*1e-3 # MHz
    nchan = int((fmax-fmin) / chres)
    pcf = 5.0 # MHz, pcal separation
    for n in range(0,nchan):
        f = fmin + n*chres
        if f % pcf < 2*chres: 
            # Close enough to flag!
            PCALchans.append(n)
            # Also flag other regular suspicious peaks
            if n-10>0:
                PCALchans.append(n-10)
            if n-20>0:
                PCALchans.append(n-20)
            if n+10<nchan:
                PCALchans.append(n+10)
            if n+20<nchan:
                PCALchans.append(n+10)
    return PCALchans

if whattodo['load_data']:
    rmtables(ms)
    importfitsidi(vis=ms, fitsidifile=[infits], scanreindexgap_s=15)

if whattodo['listobs']:
    listobs(vis=ms, listfile = ms+".listobs")

if whattodo['gencal']:
    gencal(vis=ms, caltype='gc', infile=gainfile, caltable=gaint)
    gencal(vis=ms, caltype='tsys', caltable=tsyst)

# Todo: better use of flagdata, don't iterate per channel, just create a list directly
if whattodo['pcflag']:
    for if2flag in ifs:
        chns = getPCALchans(if2flag)
        flagstr = str(if2flag[0])+':'+str(int(chns[0]))
        for ch in chns[1:]:
            flagstr += ";"+str(int(ch))
        flagdata(vis=ms, spw=flagstr, mode="manual", antenna="OE&&OW")

if whattodo['antflag']:
    flagdata(vis=ms, antenna="IS", mode="manual")

if whattodo['edgeflag']:
    flagdata(vis=ms, mode="manual", spw="*:0~63;304~319", antenna="OE&OW")

if whattodo['accor']:
    rmtables(act+"*")
    accor(vis=ms, caltable = act, corrdepflags=True, solint="7200s") # Checked, is stable in time

if whattodo['rflag1']:
    for spw in range(32):
        flagdata(vis=ms, mode="rflag", freqdevscale=7.0, timedevscale=7.0, spw=str(spw), antenna="OE&OW")

if whattodo['applycal']:
    applycal(vis = ms, gaintable = [gaint, tsyst, act])

if whattodo['split1']:
    os.system("rm -rf " + split1ms+"_*")
    split(vis=ms, outputvis = split1ms+"_A", width=1, antenna="OE&OW", datacolumn="corrected",  spw="0~7")
    split(vis=ms, outputvis = split1ms+"_B", width=1, antenna="OE&OW", datacolumn="corrected",  spw="8~15")
    split(vis=ms, outputvis = split1ms+"_C", width=1, antenna="OE&OW", datacolumn="corrected",  spw="16~23")
    split(vis=ms, outputvis = split1ms+"_D", width=1, antenna="OE&OW", datacolumn="corrected",  spw="24~31")

if whattodo['listobs1']:
    for band in bands:
        listobs(vis=split1ms+"_"+band, listfile = split1ms+"_"+band+".listobs")

if whattodo['fring']:
    for band in bands:
        rmtables(frt+"_"+band)
        fringefit(vis=split1ms+"_"+band, refant="OE", caltable=frt+"_"+band, solint="3600s", globalsolve=False, scan=frscan, zerorates=True)
    for band in bands:
        rmtables(frmbt+"_"+band)
        fringefit(vis=split1ms+"_"+band, refant="OE", caltable=frmbt+"_"+band, solint="60s", combine='spw', gaintable=[frt+"_"+band], globalsolve=False, delaywindow = [-10,10])

if whattodo['bpass']:
    for band in bands:
        rmtables(bpt+"_"+band)
        bandpass(vis=split1ms+"_"+band, scan=frscan, refant="OE", gaintable=[frt+"_"+band, frmbt+"_"+band], spwmap=[[], 8*[0]], solnorm=True, caltable=bpt+"_"+band, solint = "inf", fillgaps=10, combine="scan", minblperant=1)

if whattodo['applycal2']:
    for band in bands:
        applycal(vis = split1ms+"_"+band, gaintable=[frt+"_"+band, frmbt+"_"+band, bpt+"_"+band], spwmap=[[], 8*[0],[]])

if whattodo['split2']:
    for band in bands:
        rmtables(split2ms+"_"+band)
        split(vis=split1ms+"_"+band, outputvis = split2ms+"_"+band, width=320, datacolumn="corrected")

if whattodo['listobs2']:
    for band in bands:
        os.system("rm -rf "+split2ms+"_"+band+".listobs")
        listobs(vis=split2ms+"_"+band, listfile = split2ms+"_"+band+".listobs")

if whattodo['getflux']:
    fluxdata = {}
    for band in bands:
        vis = e+".ms.split2_"+band
        
        msmd.open(vis) 
        fieldnames = msmd.fieldnames()   
        msmd.done()     
        
        for field in fieldnames:
            if not field in fluxdata.keys():
                fluxdata[field]= []
            tf = "tmp.cl"
            rmtables(tf)
            # Fit flux (only - assume position is in the center)
            print("Fitting " + field + " in band " + band)
            uvmodelfit(vis=vis, comptype = 'P', sourcepar = [1.0, 0.0, 0.0], varypar = [True, False, False], field=field, niter=10, outfile=tf) 
            try:
                cl.open(tf)  
                flux = cl.getfluxvalue(0)  
                unit = cl.getfluxunit(0) 
                cl.done()
                # Check if fitted flux is negative, if so set it to 0
                fi = flux[0]
                if fi<0:
                    fi = -1
            except RuntimeError:
                # Likely we have no data to fit, all flagged for this scan and band
                fi = -1
                unit = "Jy"
            fluxdata[field].append([fi, unit])
            rmtables(tf)
    skeys = sorted(fluxdata.keys())
    of = open(e+".flux", "a")
    of.write("#Flux values fitted for "+e+"\n")
    for name in skeys:
        # Hardcoded for 4 bands A, B, C, D right now
        val = fluxdata[name]
        A = val[0][0]
        B = val[1][0]
        C = val[2][0]
        D = val[3][0]
        res = "{0: <8} {1:.2f} {2:.2f} {3:.2f} {4:.2f}".format(name, A, B, C, D)
        print(res)
        of.write(res + "\n")
    of.close()
