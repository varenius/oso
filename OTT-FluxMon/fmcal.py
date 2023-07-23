import numpy as np
import sys, os
import datetime

# NOTE: run with fits file as argument "casa -c fmcal.py fm3013.fits"
infits = sys.argv[1]
e = infits.split(".")[0]
gainfile = e+"oe+ow.gain"
antabfile = e+"oe+ow.antab"

# Should not need to change anything below
msn = e+".ms" # ms name
gaint = e+".ct.gain"#gain
tsyst = e+".ct.tsys" #tsys
bpt = e+".ct.bandpass" # bandpass
act = e+".ct.accor" # accor
split1ms = msn+".split1" 
split2ms = msn+".split2"
split3ms = msn+".split3"
frt = e+".ct.fring"
plotdir = "frscan_plots"
if not os.path.exists(plotdir):
    os.makedirs(plotdir)
            
whattodo = {'prepare_fits':True,
            'load_data': True,
            'listobs1': True,
            'gencal': True,
            'pcflag': True,
            'edgeflag': True,
            'accor': True,
            'rflag1': True,
            'extraflag': True,
            'plotms1': False,
            'fring1' : True,
            'bandpass' : True,
            'applycal1' :True,
            'rflag2': True,
            'split1' :True,
            'listobs2': True,
            'plotms2': False,
            'getflux': True,
            }
        
# define Perley-Butler models, x in GHz
def pb_3c286(x):
    """Spectrum for 3c286, Perley and Butler (2017) """
    return 10**(1.2481-0.4507*np.log10(x)-0.1798*(np.log10(x))**2+0.0357*(np.log10(x))**3)
def pb_3c147(x):
    """Spectrum for 3c147, Perley and Butler (2017) """
    return 10**(1.4516-0.6961*np.log10(x)-0.2007*(np.log10(x))**2+0.0640*(np.log10(x))**3-0.0464*(np.log10(x))**4+0.0289*(np.log10(x))**5)
def pb_3c295(x):
    """Spectrum for 3c295, Perley and Butler (2017) """
    return 10**(1.4701-0.7658*np.log10(x)-0.2780*(np.log10(x))**2+0.0347*(np.log10(x))**3-0.0399*(np.log10(x))**4)

if whattodo['prepare_fits']:
    # ONLY NEEDED ONCE AS IT UPDATES THE ACTUAL INPUT FITS FILE!
    # BUT DOES NOT HARM TO RUN TWICE, WILL JUST REPLACE
    import pyfits as fits
    hdul = fits.open(e+".fits", mode='update')
    print("FITS Table structure before edit:")
    hdul.info()
    toremove = []
    for i,tab in enumerate(hdul):
        if tab.name=="SYSTEM_TEMPERATURE" or tab.name=="GAIN_CURVE":
            toremove.append(i)
    toremove.reverse()
    for i in toremove:
        print("INFO:: Removing FITS extension table " + hdul[i].name)
        hdul.__delitem__(i)
    hdul.flush()
    print("FITS Table structure after edit:")
    hdul.info()
    hdul.close()
    # Then, append the correct info using casa:
    if not os.path.exists("../casa-vlbi.git"):
        os.system("git clone https://github.com/jive-vlbi/casa-vlbi.git ../casa-vlbi.git")
    os.system("casa --nologger -c ../casa-vlbi.git/gc.py "+ antabfile + " " + gainfile)
    os.system("casa --nologger -c ../casa-vlbi.git/append_tsys.py " + antabfile + " " + infits)
    hdul = fits.open(e+".fits", mode='update')
    print("FITS Table structure after adding proper TSYS:")
    hdul.info()
    hdul.close()

if whattodo['load_data']:
    rmtables(msn)
    importfitsidi(vis=msn, fitsidifile=[infits], scanreindexgap_s=15)

if whattodo['listobs1']:
    listobs(vis=msn, listfile = msn+".listobs", overwrite=True)

# Get first scan of 3C286 as delay-reference scan
ms.open(msn)
mssum=ms.summary()
for i in range(1,len(mssum)):
    if mssum['scan_'+str(i)]['0']['FieldName']=="3C286":
        frscan = str(i)
        print("Using first scan of 3C286 to calibrate delays and bandpass, i.e. frscan="+frscan)
        break
ms.done()

if whattodo['gencal']:
    gencal(vis=msn, caltype='gc', infile=gainfile, caltable=gaint)
    gencal(vis=msn, caltype='tsys', caltable=tsyst)

if whattodo['pcflag']:
    flagcmd = ""
    tb.open(msn+'/SPECTRAL_WINDOW')
    freqlist = tb.getcol("CHAN_FREQ")
    tb.close()
    for spw in range(32):
        chans = freqlist[:,spw]
        for ch,f in enumerate(chans):
            ispcal = False
            fm = f/1e6
            # Check if channel is less than 0.1 MHz from pcal frequency (0,5,10,... MHz)
            #if (abs(fm-5*round(fm/5)) < 0.1):
            # Check if if channel is less than 0.1 MHz from integer MHz frequency (0,1,...). 
            # This should not be needed, every 5 MHz should be enough, but it seems we almost always
            # have spurious peaks at ever 5 MHz +- 1 MHz as well. Maybe Pcal malfunction.
            if (abs(fm-1*round(fm/1)) < 0.1):
                ispcal = True
            if ispcal:
                flagcmd += ","+str(int(spw))+':'+str(int(ch))
    flagcmd = flagcmd[1:] # Remove initial comma
    flagdata(vis=msn, spw=flagcmd, mode="manual", antenna="OE&&OW")

if whattodo['edgeflag']:
    flagdata(vis=msn, mode="manual", spw="*:0~31;304~319", antenna="OE&&OW")

if whattodo['accor']:
    rmtables(act+"*")
    accor(vis=msn, caltable = act, corrdepflags=True, solint="inf", combine="scan,field")

if whattodo['rflag1']:
    for spw in range(32):
        flagdata(vis=msn, mode="rflag", freqdevscale=5.0, timedevscale=5.0, spw=str(spw), antenna="OE&OW", datacolumn="data", extendflags=True, ntime="scan")

if whattodo['extraflag']:
    pass
    #Flag manually extra bad stuff found during data reduction
    # Source 0552+398 appears to arrive late on source in some exps
    # so we need to remove first 20 seconds
    #if e in ["fm2141", "fm2142", "fm2143", "fm2144", "fm2145", "fm2146", "fm2147", "fm2148"]:
    #    flagdata(vis=split1ms, field = "0552+398", mode="quack", quackinterval = 20, quackmode = "beg")

if whattodo['plotms1']:
    os.system("rm "+plotdir+"/frscan_before_fringefit*")
    for spw in range(32):
        plotms(vis=msn, scan=str(frscan), correlation="XX,YY", title = "Oe-Ow frscan amp before fring, spw {}".format(spw), xaxis="frequency", yaxis="amp", plotfile=plotdir+"/frscan_before_fringefit_amp_spw{0}.pdf".format(spw), showgui=False, spw=str(spw), coloraxis="corr", antenna="OE&&OW", ydatacolumn='data')
        plotms(vis=msn, scan=str(frscan), correlation="XX,YY", title = "Oe-Ow frscan phase before fring, spw {}".format(spw), xaxis="frequency", yaxis="phase", plotfile=plotdir+"/frscan_before_fringefit_phase_spw{0}.pdf".format(spw), showgui=False, spw=str(spw), coloraxis="corr", antenna="OE&&OW", ydatacolumn='data')
        
if whattodo['fring1']:
    os.system("rm -rf " + frt+"*")
    fringefit(vis=msn, scan=str(frscan), refant="OE", caltable=frt, solint="120s", globalsolve=False, corrdepflags=True, delaywindow = [100,160], zerorates=True, antenna="OE&&OW")

if whattodo['bandpass']:
    rmtables(bpt+"*")
    bandpass(vis=msn, gaintable=[frt,], scan=str(frscan), refant="OE", solnorm=True, caltable=bpt, solint = "120s", fillgaps=10, minblperant=1, corrdepflags=True)

if whattodo['applycal1']:
    #applycal(vis = msn, gaintable=[frt,bpt]) # No Tsys and gain
    applycal(vis = msn, gaintable = [gaint, tsyst, act, frt, bpt], interp=["", ",nearest", "","",""])

if whattodo['rflag2']:
    # Remove large peaks, mainly band A
    flagdata(vis=msn, mode="rflag", freqdevscale=7.0, timedevscale=7.0, antenna="OE&OW", datacolumn="corrected", extendflags=True, ntime="scan")

if whattodo['split1']:
    # Average to 1 data point per scan per spw per pol. Assuming 320 chans and max 360 s scans in input data. Also removing auto-correlations by "antenna" syntax.
    os.system("rm -rf " + split1ms+"*")
    split(vis=msn, outputvis = split1ms, width=320, timebin = "360s", datacolumn="corrected", antenna="OE&OW", keepflags=False)

if whattodo['listobs2']:
    os.system("rm -rf "+split1ms+".listobs")
    listobs(vis=split1ms, listfile = split1ms+".listobs")

if whattodo['plotms2']:
    os.system("rm "+plotdir+"/frscan_after_fringefit*")
    for spw in range(32):
        plotms(vis=split1ms, scan=str(frscan), correlation="XX,YY", title = "Oe-Ow frscan amp after fring, spw {}".format(spw), xaxis="frequency", yaxis="amp", plotfile=plotdir+"/frscan_after_fringefit_amp_spw{0}.pdf".format(spw), showgui=False, spw=str(spw), coloraxis="corr", antenna="OE&&OW", ydatacolumn='corrected')
        plotms(vis=split1ms, scan=str(frscan), correlation="XX,YY", title = "Oe-Ow frscan phase after fring, spw {}".format(spw), xaxis="frequency", yaxis="phase", plotfile=plotdir+"/frscan_after_fringefit_phase_spw{0}.pdf".format(spw), showgui=False, spw=str(spw), coloraxis="corr", antenna="OE&&OW", ydatacolumn='corrected')

if whattodo['getflux']:
    vis = split1ms
    msmd.open(vis) 
    fieldnames = msmd.fieldnames()
    msmd.done()     
    data = {}
    for field in fieldnames:
    #for field in ["3C286", "3C147", "3C295"]:
        fdata = []
        for spw in range(0,32):
            #print("Processing field " + field + ", SPW "+str(spw))
            ms.open(vis)
            ms.selectinit(datadescid=spw)
            staql={'field':field, 'spw':str(spw)}
            ms.msselect(staql)
            msum =ms.summary()
            if msum:
            # If we got some data (all could be flagged)
                start = msum['BeginTime']
                stop = msum['EndTime']
                avgtime = start+0.5*(start-stop)
                d = ms.getdata(["amplitude","axis_info"], ifraxis=True) # ifraxis to reformat into baseline structure
                f = d["axis_info"]["freq_axis"]["chan_freq"][0][0]
                corrs = list(d["axis_info"]["corr_axis"])
                xx = d["amplitude"][corrs.index("XX")][0][0] # Last index is 0 because only cross-correlations remain in these data
                #xy = d["amplitude"][corrs.index("XY")][0][0]
                #yx = d["amplitude"][corrs.index("YX")][0][0]
                yy = d["amplitude"][corrs.index("YY")][0][0]
                stokesi =  0.5*(np.mean(xx)+np.mean(yy)) # Average over scans, and XX+YY
            ms.done()
            fdata.append([f, stokesi, avgtime])
        data[field] = fdata
    ampcals = ["3C286", "3C147", "3C295"]
    ampscales = []
    for cal in ampcals:
        if cal in data.keys():
            calscale = []
            for spw in range(0,32):
                frq = data[cal][spw][0] / 1e9 # converted to GHz
                amp = data[cal][spw][1]
                if cal == "3C286":
                    mod = pb_3c286(frq)
                elif cal == "3C147":
                    mod = pb_3c147(frq)
                elif cal == "3C295":
                    mod = pb_3c295(frq)
                calscale.append(mod/amp)
            ampscales.append(calscale)
    ampscales = np.array(ampscales)
    scalemean = np.mean(ampscales, axis=0)
    scalestd = np.std(ampscales, axis=0)
    info = open("scaling_factors.txt", "w")
    info.write("scalemean: " + str(scalemean) + "\n")
    info.write("scalestd: " + str(scalestd) + "\n")
    info.close()

    fluxdir = "./fluxdata/"
    if not os.path.exists(fluxdir):
        os.makedirs(fluxdir)
    allflux = []
    for field in data.keys():
        print("Writing data for field " + field)
        of = open(fluxdir+field+".flux","w")
        of.write("#MJD FREQ[HZ] STOKES-I[JY]\n")
        rawamp = np.array(data[field])[:,1]
        scaled = rawamp*scalemean
        for spw in range(32):
            avgtime = data[field][spw][2]
            freq = data[field][spw][0]
            samp = scaled[spw]
            res = "{0} {1: 16.1f} {2: 8.3f}".format(avgtime, freq, samp)
            of.write(res+"\n")
            print(res)
        of.close()
        
