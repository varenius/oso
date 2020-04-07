# Script to plot correlated amplitudes for VGOS data in AIPS
# as function of time
from AIPS import AIPS
from Wizardry.AIPSData import AIPSUVData
import numpy as np
import sys
import matplotlib.pyplot as plt
 
AIPS.userno = 666
 
uvdata = AIPSUVData('VO0051', 'UVDATA', 1, 1)


# Get number of IFs
nif=uvdata.header['naxis'][uvdata.header['ctype'].index('IF')]

# Get lower-edge frequencies for these IFS
freq0=uvdata.header['crval'][uvdata.header['ctype'].index('FREQ')]
FQ=uvdata.table('FQ', 1)
freqs = (np.array(FQ[0]['if_freq']) + freq0 )/1e6 # Mhz
#print freqs

# Calculate the channels with pcal signal (need to be removed)
pcalch0 = 5- (freqs % 5) - 1
#print pcalch0
pcalch0 = np.round(pcalch0).astype(np.int)
#print pcalch0

print "START"
ts = []
for row in uvdata:
    adata = []
    if not (row.baseline[0]==row.baseline[1]): # Ignore autocorrs
        for j in range(nif): # loop through IFs
            #print("IF", j)
            # Get XX, YY amps (as function of freq, i.e. for 32 freq point amp_XX has length 32)
            amp_XX=np.sqrt(row.visibility[j][:,0][:,0]**2 + row.visibility[j][:,0][:,1]**2)
            amp_YY=np.sqrt(row.visibility[j][:,1][:,0]**2 + row.visibility[j][:,1][:,1]**2)
            toflag = range(pcalch0[j],32,5) + range(pcalch0[j]+1,32,5)
            amp = amp_YY
            a_filt = np.delete(amp,toflag)
            adata.append(np.average(a_filt))
            #plt.plot(amp_XX)
            #plt.plot(aXX_filt)
            #plt.show()
        ts.append(adata)
        #print(len(ts))

ts = np.array(ts)
banda = np.average(ts[:,0:8], axis=1)
bandb = np.average(ts[:,8:16], axis=1)
bandc = np.average(ts[:,16:24], axis=1)
bandd = np.average(ts[:,24:32], axis=1)
print(bandc)
print(np.average(bandc))

plt.plot(banda*1e3, label='Band A')
plt.plot(bandb*1e3, label='Band B')
plt.plot(bandc*1e3, label='Band C')
plt.plot(bandd*1e3, label='Band D')
plt.title('Oe-Ow observing 0059+581')
plt.ylabel('Correlated YY amplitude [arbitrary units]')
plt.xlabel("Time from 2020y051d18h20m22s UTC [seconds]")
plt.legend(loc="center right")
plt.savefig('oe-ow_0059+581.pdf')
plt.show()
