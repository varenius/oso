import os, sys
from astropy.io import fits
from AIPS import AIPS
from AIPSTask import AIPSTask as task
from AIPSData import AIPSUVData as UV
from Wizardry.AIPSData import AIPSImage as WIM
from Wizardry.AIPSData import AIPSUVData as WUV
from AIPSData import AIPSImage as IM
import time
import numpy as np
import matplotlib.pyplot as plt

infits = sys.argv[1] # input fitsfile with data

whattodo = {'load_data': False,
            'listr': False,
            'pcflag': False,
            'antflag': False,
            'rflag1': False,
            'fring' :False,
            'bpass' :False,
            'rflag2': True,
            'ion_corr': False, # ->CL2
            'par_ang_cor': False, # ->CL3
            'apriori_ampcal': False,  # SN1,2, CL4
            'bpass_pcal': False, # BP 1.
            'export_results': False,
            }
AIPS.userno = 888

#fitld
#flag pcal
#flag ishioka
#rflag RFI?
#fring
#apply fring
#read antab
#apply antab, apcal
#split (and average to one point per IF?)
#fittp

if whattodo['load_data']:
    fitld = task('fitld')
    fitld.default()
    outdata = UV('TMP', 'TMP', 1, 1)
    fitld.datain = infits
    fitld.outdata = outdata
    fitld.ncount = 1 # one file
    fitld.digicor = 1 # Do corrections for digitization loss
    fitld.clint = 1.0/60 # Every second
    # If outdata exists, remove it (it is TMP file after all)
    if outdata.exists():
        outdata.zap()
    fitld.go()

if whattodo['listr']:
    listrfile = 'listr.tmp'
    if os.path.exists(listrfile):
        os.remove(listrfile)
    data = UV('TMP', 'TMP', 1, 1)
    listr = task('listr')
    listr.default()
    listr.indata=data
    listr.optype='SCAN'
    listr.outprint=listrfile
    listr.docrt=-1
    listr.go()

def getIFs(data):
    ifs = np.array([
    # IF LOWEREDGE[GHz]  WIDTH[kHz]   CHANNELWIDTH[kHz]
    [ 1, 3.00040000,32000.0020,100.0000],
    [ 2, 3.03240000,32000.0020,100.0000],
    [ 3, 3.06440000,32000.0020,100.0000],
    [ 4, 3.19240000,32000.0020,100.0000],
    [ 5, 3.28840000,32000.0020,100.0000],
    [ 6, 3.35240000,32000.0020,100.0000],
    [ 7, 3.41640000,32000.0020,100.0000],
    [ 8, 3.44840000,32000.0020,100.0000],
    [ 9, 5.24040000,32000.0020,100.0000],
    [10, 5.27240000,32000.0020,100.0000],
    [11, 5.30440000,32000.0020,100.0000],
    [12, 5.43240000,32000.0020,100.0000],
    [13, 5.52840000,32000.0020,100.0000],
    [14, 5.59240000,32000.0020,100.0000],
    [15, 5.65640000,32000.0020,100.0000],
    [16, 5.68840000,32000.0020,100.0000],
    [17, 6.36040000,32000.0020,100.0000],
    [18, 6.39240000,32000.0020,100.0000],
    [19, 6.42440000,32000.0020,100.0000],
    [20, 6.55240000,32000.0020,100.0000],
    [21, 6.64840000,32000.0020,100.0000],
    [22, 6.71240000,32000.0020,100.0000],
    [23, 6.77640000,32000.0020,100.0000],
    [24, 6.80840000,32000.0020,100.0000],
    [25,10.20040000,32000.0020,100.0000],
    [26,10.23240000,32000.0020,100.0000],
    [27,10.26440000,32000.0020,100.0000],
    [28,10.39240000,32000.0020,100.0000],
    [29,10.48840000,32000.0020,100.0000],
    [30,10.55240000,32000.0020,100.0000],
    [31,10.61640000,32000.0020,100.0000],
    [32,10.64840000,32000.0020,100.0000]])
    return ifs

def getPCALchans(IF):
    PCALchans = []
    fmin = IF[1]*1e3 # to MHz
    fmax = fmin + IF[2]*1e-3 # MHz
    chres = IF[3]*1e-3 # MHz
    nchan = int((fmax-fmin) / chres)
    pcf = 5.0 # MHz, pcal separation
    for n in range(1,nchan+1): # AIPS starts counting at 1
        f = fmin + n*chres
        if f % pcf < 2*chres: 
            # Close enough to flag!
            PCALchans.append(n)
            # Also flag other regular suspicious peaks
            if n-10>0:
                PCALchans.append(n-10)
    return PCALchans

if whattodo['pcflag']:
    data = UV('TMP', 'TMP', 1, 1)
    # Remove all FG tables
    data.zap_table('FG', -1)
    ifs2flag = getIFs(data)
    for if2flag in ifs2flag:
        chns = getPCALchans(if2flag)
        for ch2flag in chns:
            uvflg = task('uvflg')
            uvflg.default()
            uvflg.indata = data
            uvflg.outfgver = 1
            uvflg.reason = 'PCAL'
            uvflg.opcode = 'FLAG'
            uvflg.bchan=ch2flag
            uvflg.echan=ch2flag
            uvflg.bif=int(if2flag[0])
            uvflg.eif=int(if2flag[0])
            uvflg.go()

if whattodo['antflag']:
    fgver = 1
    data = UV('TMP', 'TMP', 1, 1)
    antab = data.table('AN', 1)
    ants2keep = ['OE', 'OW']
    for row in antab:
        antnum = row['nosta']
        antname = row['anname'].strip()
        if not antname in ants2keep:
            uvflg = task('uvflg')
            uvflg.default()
            uvflg.indata = data
            uvflg.outfgver = fgver
            uvflg.opcode = 'FLAG'
            uvflg.antenna = [None, antnum]
            uvflg.go()

if whattodo['rflag1']:
    fgver = 1
    data = UV('TMP', 'TMP', 1, 1)
    rflag = task('rflag')
    rflag.default()
    rflag.indata = data
    rflag.outfgver = fgver
    rflag.stokes = "XYYX"
    rflag.fparm[1] = 5
    rflag.fparm[2] = 1
    rflag.fparm[4] = -1
    rflag.fparm[6] = 2 # Adjacent chans
    rflag.fparm[7] = 0.85
    rflag.fparm[8] = 2
    rflag.fparm[9] = 3
    rflag.fparm[10] = 3 # Clip level
    rflag.doplot=1 # Calculate SCUTOFF adverbs
    rflag.avgchan=19
    rflag.go()
    rflag.doplot=-12 # Apply SCUTOFF, get new values
    rflag.go()
    rflag.doplot=0 # Apply SCUTOFF
    rflag.go()

if whattodo['fring']:
    fgver = 1
    snoutver = 1
    clinver = 1
    cloutver = 2
    data = UV('TMP', 'TMP', 1, 1)
    data.zap_table('SN', -1)
    ## Remove all SN tables >= snver
    #for i in range(data.table_highver('SN'), snver-1, -1):
    #    data.zap_table('SN', i)
    fring = task('fring')
    fring.default()
    fring.indata = data
    fring.snver = snoutver
    fring.solint = 10 # longer than scan
    fring.flagver = fgver
    fring.go()

    # Apply SN-table
    # Remove all CL tables higher than version cloutver-1.
    for i in range(data.table_highver('CL'), cloutver-1, -1):
        data.zap_table('CL', i)
    # Make CL table
    clcal = task('clcal') 
    clcal.default()
    clcal.indata = data
    clcal.snver = snoutver
    clcal.invers = snoutver
    clcal.sour = [None, ''] # All sources
    clcal.gainver = clinver
    clcal.gainuse = cloutver
    clcal.go()

if whattodo['bpass']:
    fgver = 1
    bpoutver = 1
    clinver = 2
    data = UV('TMP', 'TMP', 1, 1)
    for i in range(data.table_highver('BP'), bpoutver-1, -1):
        data.zap_table('BP', i)
    bpass = task('bpass')
    bpass.default()
    bpass.indata = data
    bpass.bpver = bpoutver
    bpass.solint = -1
    bpass.docal = 1
    bpass.gainuse = clinver
    bpass.flagver = fgver
    bpass.bpassprm[10]=1
    bpass.go()

if whattodo['rflag2']:
    clinver = 2
    bpinver = 1
    fgver = 1
    data = UV('TMP', 'TMP', 1, 1)
    rflag = task('rflag')
    rflag.default()
    rflag.indata = data
    rflag.outfgver = fgver
    rflag.stokes = "XYYX"
    rflag.docal = 1
    rflag.gainuse = clinver
    rflag.doband = 1
    rflag.bpver = bpinver
    rflag.fparm[1] = 5
    rflag.fparm[2] = 1
    rflag.fparm[4] = -1
    rflag.fparm[6] = 2 # Adjacent chans
    rflag.fparm[7] = 0.85
    rflag.fparm[8] = 2
    rflag.fparm[9] = 3
    rflag.fparm[10] = 3 # Clip level
    rflag.doplot=1 # Calculate SCUTOFF adverbs
    rflag.avgchan=19
    rflag.go()
    rflag.doplot=-12 # Apply SCUTOFF, get new values
    rflag.go()
    rflag.doplot=0 # Apply SCUTOFF
    rflag.go()
