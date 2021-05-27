#!/usr/bin/python
import socket, os, datetime, time, re, sys
import numpy as np
import matplotlib.pyplot as plt
from baseband import vdif
import astropy.units as u
from scipy.signal import resample_poly

# jive5ab info
#ip = "129.16.208.51" # kare
ip = "localhost"
port = "2621" # jive5ab control port
me = socket.gethostname()
DEBUG=False# Print jive5ab return messages, which are parsed for results

nifs = 8 # number of IFs
bbcw = 32 # MHz, width of BBC
nspec = 128 # number of points in final spectrum
#Plot design
nrows = 32
ncols = 2
sample_rate = 2*bbcw # MHz

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

scriptdir=os.path.dirname(os.path.realpath(__file__))
def get_ifdata(nif):
    vbsname = "testrec_fulla_210526_162154_"+str(nif)
    disk2fileout = scriptdir+"/checkdata.vdif"
    fbcmd("scan_set="+vbsname+":+3.0s:+0.01s")
    fbcmd("scan_set?")
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
    # Ensure file pointer is at beginning of file
    fh.seek(0)
    # Read all data until end
    ifdata = fh.read()
    # Close infile
    fh.close()
    return [nbbcs, ifdata]

#vbsname = "testrec_freja_210526_161523"
# Prepare plot
plt.rcParams.update({'font.size': 3})
f,axs = plt.subplots(nrows, ncols, sharex=True, figsize=(4,8), dpi=300)
plt.subplots_adjust(left=0.075, right=0.95, top=0.95, bottom=0.05, hspace=0)

#Else if multifile
bbc = 0
for nif in range(nifs):
    nbbcs, data = get_ifdata(nif)
    for i in range(nbbcs):
        # Slice out bbc i from all data
        bbcdata = data[:, i].astype(int)  # bbc, converted to 4 integer states (2-bit): -3, -1, +1, +3
        nfft = bbcdata.size
        states = np.unique(bbcdata, return_counts=True)
        sampler_stats = 100*states[1]/nfft
        
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
        col = int(bbc/nrows)
        row = (nrows-1)-int((col*bbc+bbc)/(col+1))
        axs[row][col].plot(fr2plot, ps2plot_dec, color=color)
        axs[row][col].set_yscale("log")
        axs[row][col].set_ylabel("BBC{0:03d}".format(bbc+1), rotation=0, ha='right', va="center")
        axs[row][col].yaxis.set_major_locator(plt.NullLocator())
        axs[row][col].yaxis.set_minor_locator(plt.NullLocator())
        axs[row][col].spines["top"].set_visible(False)
        print("BBC{0:03d} sampler stats: {1} %".format(bbc+1, np.round(sampler_stats,1)))
        bbc+=1
plt.show()
