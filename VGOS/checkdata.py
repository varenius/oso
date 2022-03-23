#!/usr/bin/python
import socket, os, datetime, time, re, sys
import numpy as np
import matplotlib.pyplot as plt
from baseband import vdif
import astropy.units as u
from scipy.signal import resample_poly
import matplotlib.patches as patches

def fbcmd(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))
    sock.send(message.encode()) # convert message to bytestring
    if DEBUG:
        print('INFO: sent to '+ip+':'+port + ':' + message)
    data = sock.recv(1024)
    if DEBUG:
        print('INFO: answer: ', data.decode())
    sock.close()
    return data.decode()

def get_singlefile_data(vbsname):
    # TODO: Thread/IF selection in vmux step
    disk2fileout = scriptdir+"/checkdata.vdif"
    vmuxedfile = disk2fileout +".vmuxed"
    ss = fbcmd("scan_set="+vbsname+":+1.0s:+"+extractiontime)
    if " does not exist" in ss:
        return [False, -1, 0, -1] # No single file data found
    sc = fbcmd("scan_check?")
    nbbcs = int(int(sc.split(":")[4])/2)
    fbcmd("disk2file=" + disk2fileout + ":::w")
    nwait = 0
    time.sleep(0.25) # Wait for disk2file
    while True:
        stat = fbcmd("disk2file?")
        if "inactive" in stat:
            break
        if nwait>5:
            print("ERROR: Waited more than 5 sec for disk2file! Something is wrong, exiting...")
            sys.exit(1)
        time.sleep(1) # Wait for disk2file
        nwait+=1
    vmuxcmd = "vmux -v {0} 8224 15625 0,1,2,3,4,5,6,7 {1}".format(disk2fileout, vmuxedfile)
    os.system(vmuxcmd)
    time.sleep(5) # Wait for vmux
    # Read file
    fh = vdif.open(vmuxedfile, 'rs', sample_rate=sample_rate*u.MHz) # Need to specify sample rate, too short to autodetect.
    start_time = fh.info()['start_time']
    # Ensure file pointer is at beginning of file
    fh.seek(0)
    # Read all data until end
    ifdata = fh.read()
    # Close infile
    fh.close()
    return [True, nbbcs, ifdata, start_time]

def get_multifile_data(vbs, nif):
    vbsname = vbs+"_"+str(nif)
    disk2fileout = scriptdir+"/checkdata.vdif"
    ss = fbcmd("scan_set="+vbsname+":+2.0s:+"+extractiontime)
    if " does not exist" in ss:
        return [-1, 0, -1]
    sc = fbcmd("scan_check?")
    nbbcs = int(int(sc.split(":")[4])/2)
    fbcmd("disk2file=" + disk2fileout + ":::w")
    nwait = 0
    time.sleep(0.25) # Wait for disk2file
    while True:
        stat = fbcmd("disk2file?")
        if "inactive" in stat:
            break
        if nwait>5:
            print("ERROR: Waited more than 5 sec for disk2file! Something is wrong, exiting...")
            sys.exit(1)
        time.sleep(1) # Wait for disk2file
        nwait+=1
    # Read file
    fh = vdif.open(disk2fileout, 'rs', sample_rate=sample_rate*u.MHz) # Need to specify sample rate, too short to autodetect.
    start_time = fh.info()['start_time']
    # Ensure file pointer is at beginning of file
    fh.seek(0)
    # Read all data until end
    ifdata = fh.read()
    # Close infile
    fh.close()
    return [nbbcs, ifdata, start_time]

def plot_bbc(bbcdata, bbc, nif):
    row=(nrows-1)-nif
    col=bbc-nif*bbcsperIF # Assume nbbcs always the same
    nfft = bbcdata.size
    states = np.unique(bbcdata, return_counts=True)
    sampler_stats = states[1]/nfft
    
    ps = np.abs(np.fft.fft(bbcdata))**2
    time_step = 1.0/sample_rate
    freqs = np.fft.fftfreq(nfft, time_step)
    idx = np.argsort(freqs)
    
    # Spectrum is conjugate from - to +, only plot half...
    nplot = int(nfft/2) 
    ps2plot = ps[idx][nplot:]
    
    # Decimate signal to 128 points
    down = int(nplot/nspec)
    ps2plot_dec = resample_poly(ps2plot, 1, down)
    fr2plot = np.linspace(0,bbcw, nspec)
    
    # Plot
    if nif%2==0:
        color = "black"
    else:
        color= "red"
    ax = axs[row][col]
    ax.plot(fr2plot, ps2plot_dec, color=color)
    if col==0:
        ax.set_ylabel("IF "+ str(iflabels[nif]) + "\n"+str(start_time)[:-5].replace("T","\n"), rotation=0, ha='right', va="center")
    ax.text(0.5, 0.35, "BBC{0:03d}".format(bbc+1), transform=ax.transAxes, ha="center")
    #print("BBC{0:03d} sampler stats: {1} %".format(bbc+1, np.round(100*sampler_stats,1)))
    start=0
    for i,stat in enumerate(sampler_stats):
        #if i%2==0:
        if i in [0,3]:
            scol = "blue"
        else:
            scol = "green"
        ax.add_patch(patches.Rectangle( (start,0), width=stat, height=0.25, edgecolor="black", facecolor = scol, fill=True, transform=ax.transAxes))
        start +=stat
    itot = 0
    for i in [0.18,0.33,0.33]: # last 0.18 not necessary
        itot+=i
        ax.axvline(x=itot*bbcw)
    ax.set_xlim([0,bbcw])

ip = sys.argv[1] #ip = "localhost"
port = sys.argv[2] #port = "2621" # jive5ab control port
bbcw = int(sys.argv[3]) #bbcw = 32 # MHz, width of BBC
nspec = int(sys.argv[4]) #nspec = 256 # number of points in final spectrum
bbcsperIF = int(sys.argv[5]) #bbcsperIF = 8

DEBUG=False# Print jive5ab return messages, which are parsed for results

ifs2plot = [0,1,2,3,4,5,6,7] # List IFs to plot, starting from 0. 
#Plot design
nrows = 8
ncols = bbcsperIF
extractiontime = "0.01s" # At least 0.01s
iflabels = ["A", "B", "C", "D", "E", "F", "G", "H"]

plt.rcParams.update({'font.size': 8})
sample_rate = 2*bbcw # MHz
#scriptdir=os.path.dirname(os.path.realpath(__file__))
scriptdir = "/data/check_data/"

scres = fbcmd("scan_check?")
if "does not exist" in scres:
    vbsfile = scres.split(":")[1].split("'")[1].strip()
else:
    vbsfile = scres.split(":")[2].strip() # ignore spaces around filename
if vbsfile[-2]=="_":
    # Multi-file name, ignore the suffix for the initial pattern
    vbsfile = vbsfile[:-2]
print("Processing VBS name " + vbsfile)

#vbsname = "testrec_freja_210526_161523"
# Prepare plot
f,axs = plt.subplots(nrows, ncols, sharex=True, figsize=(8,4), dpi=300)
for a in axs:
    for b in a:
        b.set_yscale("log")
        b.yaxis.set_major_locator(plt.NullLocator())
        b.yaxis.set_minor_locator(plt.NullLocator())
        b.xaxis.set_major_locator(plt.NullLocator())
        b.xaxis.set_minor_locator(plt.NullLocator())
        # Remove top double line except from top row
        if not b in axs[0]:
            b.spines["top"].set_visible(False)
plt.subplots_adjust(left=0.125, right=0.975, top=0.925, bottom=0.05, hspace=0, wspace=0)

# Check if dealing with single-file. If so, vmux, then read all data sequentially and split
singlefile, nbbcs, data, start_time = get_singlefile_data(vbsfile)
if not singlefile:
    recmode = "multifile"
    # Failed single-file, try multi-file:
    for nif in ifs2plot:
        nbbcs, data, start_time = get_multifile_data(vbsfile, nif)
        if nbbcs>0: #Check if data was found
            for i in range(nbbcs):
                bbc = nbbcs*nif + i
                # Slice out bbc from all data
                bbcdata = data[:, i].astype(int)  # bbc, converted to 4 integer states (2-bit): -3, -1, +1, +3
                plot_bbc(bbcdata, bbc, nif)
else:
    # Singlefile, so step through all BBCs, assuming bbcperif BBCs for each IF
    recmode = "vmuxed"
    for bbc in range(nbbcs):
        nif = int(bbc/bbcsperIF)
        # Slice out bbc from all data
        bbcdata = data[:, bbc].astype(int)  # bbc, converted to 4 integer states (2-bit): -3, -1, +1, +3
        plot_bbc(bbcdata, bbc, nif)

f.suptitle(vbsfile+": " + recmode + ", "+extractiontime + ". log10 spectra: {} points per {} MHz. Blue/green = sampler stats.".format(nspec,bbcw))
f.savefig(scriptdir+"/bandpass.pdf",dpi=300)
