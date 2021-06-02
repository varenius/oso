#!/usr/bin/env python3
import sys, os, glob
import datetime, time
import numpy as np
import matplotlib.dates as mdates
from subprocess import run, PIPE
import socket

def filltracks(of):
    of.write("$TRACKS;\n")
    of.write("  def OTT;\n")
    of.write("    track_frame_format = VDIF;\n")
    of.write("  enddef;\n")

def fillmode(of):
    of.write("$MODE;\n")
    of.write("  def VGEO-X8.XX;\n")
    of.write("    ref $FREQ = OTT:Oe:Ow;\n")
    of.write("    ref $BBC = OTT:Oe:Ow;\n")
    of.write("    ref $IF = OTT:Oe:Ow;\n")
    of.write("    ref $TRACKS = OTT:Oe:Ow;\n")
    of.write("    ref $PHASE_CAL_DETECT = OTT:Oe:Ow;\n")
    of.write("  enddef;\n")

def fillbbc(of):
    of.write("$BBC;\n")
    of.write("  def OTT;\n")
    of.write("    BBC_assign = &BBC01 : 01 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC02 : 02 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC03 : 03 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC04 : 04 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC05 : 05 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC06 : 06 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC07 : 07 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC08 : 08 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC09 : 09 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC10 : 10 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC11 : 11 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC12 : 12 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC13 : 13 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC14 : 14 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC15 : 15 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC16 : 16 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC17 : 17 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC18 : 18 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC19 : 19 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC20 : 20 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC21 : 21 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC22 : 22 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC23 : 23 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC24 : 24 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC25 : 25 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC26 : 26 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC27 : 27 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC28 : 28 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC29 : 29 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC30 : 30 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC31 : 31 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC32 : 32 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC33 : 33 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC34 : 34 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC35 : 35 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC36 : 36 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC37 : 37 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC38 : 38 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC39 : 39 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC40 : 40 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC41 : 41 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC42 : 42 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC43 : 43 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC44 : 44 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC45 : 45 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC46 : 46 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC47 : 47 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC48 : 48 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC49 : 49 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC50 : 50 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC51 : 51 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC52 : 52 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC53 : 53 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC54 : 54 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC55 : 55 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC56 : 56 : &IF_1N;\n")
    of.write("    BBC_assign = &BBC57 : 57 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC58 : 58 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC59 : 59 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC60 : 60 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC61 : 61 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC62 : 62 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC63 : 63 : &IF_3N;\n")
    of.write("    BBC_assign = &BBC64 : 64 : &IF_3N;\n")
    of.write("  enddef;\n")

def fillfreq(of):
    of.write("$FREQ;\n")
    of.write("  def OTT;\n")
    of.write("    chan_def = &X : 3480.40 MHz : L : 32.000 MHz : &Ch01 : &BBC01 : &L_cal;\n")
    of.write("    chan_def = &X : 3448.40 MHz : L : 32.000 MHz : &Ch02 : &BBC02 : &L_cal;\n")
    of.write("    chan_def = &X : 3384.40 MHz : L : 32.000 MHz : &Ch03 : &BBC03 : &L_cal;\n")
    of.write("    chan_def = &X : 3320.40 MHz : L : 32.000 MHz : &Ch04 : &BBC04 : &L_cal;\n")
    of.write("    chan_def = &X : 3224.40 MHz : L : 32.000 MHz : &Ch05 : &BBC05 : &L_cal;\n")
    of.write("    chan_def = &X : 3096.40 MHz : L : 32.000 MHz : &Ch06 : &BBC06 : &L_cal;\n")
    of.write("    chan_def = &X : 3064.40 MHz : L : 32.000 MHz : &Ch07 : &BBC07 : &L_cal;\n")
    of.write("    chan_def = &X : 3032.40 MHz : L : 32.000 MHz : &Ch08 : &BBC08 : &L_cal;\n")
    of.write("    chan_def = &X : 3480.40 MHz : L : 32.000 MHz : &Ch09 : &BBC09 : &L_cal;\n")
    of.write("    chan_def = &X : 3448.40 MHz : L : 32.000 MHz : &Ch10 : &BBC10 : &L_cal;\n")
    of.write("    chan_def = &X : 3384.40 MHz : L : 32.000 MHz : &Ch11 : &BBC11 : &L_cal;\n")
    of.write("    chan_def = &X : 3320.40 MHz : L : 32.000 MHz : &Ch12 : &BBC12 : &L_cal;\n")
    of.write("    chan_def = &X : 3224.40 MHz : L : 32.000 MHz : &Ch13 : &BBC13 : &L_cal;\n")
    of.write("    chan_def = &X : 3096.40 MHz : L : 32.000 MHz : &Ch14 : &BBC14 : &L_cal;\n")
    of.write("    chan_def = &X : 3064.40 MHz : L : 32.000 MHz : &Ch15 : &BBC15 : &L_cal;\n")
    of.write("    chan_def = &X : 3032.40 MHz : L : 32.000 MHz : &Ch16 : &BBC16 : &L_cal;\n")
    of.write("    chan_def = &X : 5720.40 MHz : L : 32.000 MHz : &Ch17 : &BBC17 : &L_cal;\n")
    of.write("    chan_def = &X : 5688.40 MHz : L : 32.000 MHz : &Ch18 : &BBC18 : &L_cal;\n")
    of.write("    chan_def = &X : 5624.40 MHz : L : 32.000 MHz : &Ch19 : &BBC19 : &L_cal;\n")
    of.write("    chan_def = &X : 5560.40 MHz : L : 32.000 MHz : &Ch20 : &BBC20 : &L_cal;\n")
    of.write("    chan_def = &X : 5464.40 MHz : L : 32.000 MHz : &Ch21 : &BBC21 : &L_cal;\n")
    of.write("    chan_def = &X : 5336.40 MHz : L : 32.000 MHz : &Ch22 : &BBC22 : &L_cal;\n")
    of.write("    chan_def = &X : 5304.40 MHz : L : 32.000 MHz : &Ch23 : &BBC23 : &L_cal;\n")
    of.write("    chan_def = &X : 5272.40 MHz : L : 32.000 MHz : &Ch24 : &BBC24 : &L_cal;\n")
    of.write("    chan_def = &X : 5720.40 MHz : L : 32.000 MHz : &Ch25 : &BBC25 : &L_cal;\n")
    of.write("    chan_def = &X : 5688.40 MHz : L : 32.000 MHz : &Ch26 : &BBC26 : &L_cal;\n")
    of.write("    chan_def = &X : 5624.40 MHz : L : 32.000 MHz : &Ch27 : &BBC27 : &L_cal;\n")
    of.write("    chan_def = &X : 5560.40 MHz : L : 32.000 MHz : &Ch28 : &BBC28 : &L_cal;\n")
    of.write("    chan_def = &X : 5464.40 MHz : L : 32.000 MHz : &Ch29 : &BBC29 : &L_cal;\n")
    of.write("    chan_def = &X : 5336.40 MHz : L : 32.000 MHz : &Ch30 : &BBC30 : &L_cal;\n")
    of.write("    chan_def = &X : 5304.40 MHz : L : 32.000 MHz : &Ch31 : &BBC31 : &L_cal;\n")
    of.write("    chan_def = &X : 5272.40 MHz : L : 32.000 MHz : &Ch32 : &BBC32 : &L_cal;\n")
    of.write("    chan_def = &X : 6840.40 MHz : L : 32.000 MHz : &Ch33 : &BBC33 : &L_cal;\n")
    of.write("    chan_def = &X : 6808.40 MHz : L : 32.000 MHz : &Ch34 : &BBC34 : &L_cal;\n")
    of.write("    chan_def = &X : 6744.40 MHz : L : 32.000 MHz : &Ch35 : &BBC35 : &L_cal;\n")
    of.write("    chan_def = &X : 6680.40 MHz : L : 32.000 MHz : &Ch36 : &BBC36 : &L_cal;\n")
    of.write("    chan_def = &X : 6584.40 MHz : L : 32.000 MHz : &Ch37 : &BBC37 : &L_cal;\n")
    of.write("    chan_def = &X : 6456.40 MHz : L : 32.000 MHz : &Ch38 : &BBC38 : &L_cal;\n")
    of.write("    chan_def = &X : 6424.40 MHz : L : 32.000 MHz : &Ch39 : &BBC39 : &L_cal;\n")
    of.write("    chan_def = &X : 6392.40 MHz : L : 32.000 MHz : &Ch40 : &BBC40 : &L_cal;\n")
    of.write("    chan_def = &X : 6840.40 MHz : L : 32.000 MHz : &Ch41 : &BBC41 : &L_cal;\n")
    of.write("    chan_def = &X : 6808.40 MHz : L : 32.000 MHz : &Ch42 : &BBC42 : &L_cal;\n")
    of.write("    chan_def = &X : 6744.40 MHz : L : 32.000 MHz : &Ch43 : &BBC43 : &L_cal;\n")
    of.write("    chan_def = &X : 6680.40 MHz : L : 32.000 MHz : &Ch44 : &BBC44 : &L_cal;\n")
    of.write("    chan_def = &X : 6584.40 MHz : L : 32.000 MHz : &Ch45 : &BBC45 : &L_cal;\n")
    of.write("    chan_def = &X : 6456.40 MHz : L : 32.000 MHz : &Ch46 : &BBC46 : &L_cal;\n")
    of.write("    chan_def = &X : 6424.40 MHz : L : 32.000 MHz : &Ch47 : &BBC47 : &L_cal;\n")
    of.write("    chan_def = &X : 6392.40 MHz : L : 32.000 MHz : &Ch48 : &BBC48 : &L_cal;\n")
    of.write("    chan_def = &X : 10680.40 MHz : L : 32.000 MHz : &Ch49 : &BBC49 : &L_cal;\n")
    of.write("    chan_def = &X : 10648.40 MHz : L : 32.000 MHz : &Ch50 : &BBC50 : &L_cal;\n")
    of.write("    chan_def = &X : 10584.40 MHz : L : 32.000 MHz : &Ch51 : &BBC51 : &L_cal;\n")
    of.write("    chan_def = &X : 10520.40 MHz : L : 32.000 MHz : &Ch52 : &BBC52 : &L_cal;\n")
    of.write("    chan_def = &X : 10424.40 MHz : L : 32.000 MHz : &Ch53 : &BBC53 : &L_cal;\n")
    of.write("    chan_def = &X : 10296.40 MHz : L : 32.000 MHz : &Ch54 : &BBC54 : &L_cal;\n")
    of.write("    chan_def = &X : 10264.40 MHz : L : 32.000 MHz : &Ch55 : &BBC55 : &L_cal;\n")
    of.write("    chan_def = &X : 10232.40 MHz : L : 32.000 MHz : &Ch56 : &BBC56 : &L_cal;\n")
    of.write("    chan_def = &X : 10680.40 MHz : L : 32.000 MHz : &Ch57 : &BBC57 : &L_cal;\n")
    of.write("    chan_def = &X : 10648.40 MHz : L : 32.000 MHz : &Ch58 : &BBC58 : &L_cal;\n")
    of.write("    chan_def = &X : 10584.40 MHz : L : 32.000 MHz : &Ch59 : &BBC59 : &L_cal;\n")
    of.write("    chan_def = &X : 10520.40 MHz : L : 32.000 MHz : &Ch60 : &BBC60 : &L_cal;\n")
    of.write("    chan_def = &X : 10424.40 MHz : L : 32.000 MHz : &Ch61 : &BBC61 : &L_cal;\n")
    of.write("    chan_def = &X : 10296.40 MHz : L : 32.000 MHz : &Ch62 : &BBC62 : &L_cal;\n")
    of.write("    chan_def = &X : 10264.40 MHz : L : 32.000 MHz : &Ch63 : &BBC63 : &L_cal;\n")
    of.write("    chan_def = &X : 10232.40 MHz : L : 32.000 MHz : &Ch64 : &BBC64 : &L_cal;\n")
    of.write("    sample_rate = 64.0 Ms/sec;\n")
    of.write("  enddef;\n")

def fillif(of):
    of.write("$IF;\n")
    of.write("  def OTT;\n")
    of.write("    if_def = &IF_1N : 1N : X :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
    of.write("    if_def = &IF_3N : 3N : Y :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
    of.write("  enddef;\n")

def getskd(exp):
    run(['scp','fulla:/usr2/sched/'+exp+'.skd', '.'])

def getfslogs(exp):
    run(['scp','fulla:/usr2/log/'+exp+'oe.log', '.'])
    run(['scp','freja:/usr2/log/'+exp+'ow.log', '.'])

def fillclock(of, fslog):
    peculiaroff = {"Ow": [6.183,"from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
                   "Oe": [6.211,"from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
                   "On": [1.350,"from multiple exp from Bonn"],
                   "Is": [1.268,"from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
                   "Yj": [-0.108, "from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
                   "O8": [5.18, "From Bob C, EVN: O8 = +5.78,  On = +1.95 --> O8 = 5.78-(1.95-1.350)=5.18"]
                   }
    vals = []
    times = []
    for l in open(fslog):
        if ("/gps-fmout/" in l ) or ("/gps-maser/" in l) or ("/gps-dbbcout2/" in l):
            ls = l.split("/")
            time = datetime.datetime.strptime(ls[0], "%Y.%j.%H:%M:%S.%f")
            val = -float(ls[2]) # negative, as fmout-gps is the "clock early" convention
            vals.append(val) # Seconds
            times.append(time)
        elif ("/fmout-gps/" in l ):
            ls = l.split("/")
            time = datetime.datetime.strptime(ls[0], "%Y.%j.%H:%M:%S.%f")
            val = float(ls[2]) # pos, as fmout-gps is the "clock early" convention
            vals.append(val) # Seconds
            times.append(time)
        elif ("!dbe_gps_offset?" in l ):
            ls = re.split(r"/|[?]0:|;",l.strip())
            time = datetime.datetime.strptime(ls[0], "%Y.%j.%H:%M:%S.%f")
            val = float(ls[3])
            vals.append(val) # Seconds
            times.append(time)
    vals = np.array(vals)
    times = np.array(times)
    
    # Filter outliers
    avg = np.average(vals)
    std = np.std(vals)
    diff = np.abs(vals-avg)
    cut = 10*std
    # Filtering should really be done first fitting once without filters, removing linear trend, then filter outliers. 
    # But this works well enough for Onsala big jumps as is.
    bad = np.where(diff>cut)
    vals = np.delete(vals, bad)
    times = np.delete(times,bad)
    
    x = mdates.date2num(times) # decimal days
    pf = np.polyfit(x, vals, 1)
    p = np.poly1d(pf)
    
    xx = np.linspace(x.min(), x.max(), 100)
    dd = mdates.num2date(xx)
    
    fn = os.path.basename(fslog)
    station = fn[-6:-5].upper()+fn[-5:-4].lower()
    
    valtime = (dd[0]+datetime.timedelta(minutes=-30)).strftime("%Yy%jd%Hh%Mm%Ss") # Make valid range 30 min before first ref point, just in case first point is after first scan
    reftime = (dd[0]).strftime("%Yy%jd%Hh%Mm%Ss") # Integer seconds; we don't need more precision
    
    # Get fitted clock, add peculiar offset
    pecoff = peculiaroff[station]
    refclock = p(xx.min()) + pecoff[0]*1e-6
    rate = pf[0]/(24*3600) # convert to s/s
    of.write("*"+station+": Clock without peculiar offset: {0} us\n".format(p(xx.min())*1e6))
    of.write("*                  valid from           clock_early    clock_early_epoch        rate\n")
    of.write("def {:s};  clock_early = {:s} : {:.3f} usec : {:s} : {:.3f}e-12; enddef;\n".format(station,valtime,refclock*1e6,reftime,rate*1e12))
    
def fillEOP(of, start):
    os.system('EMAIL_ADDR=eskil.varenius@chalmers.se geteop.pl ' + start + ' 5')
    for el in open("EOP.txt"):
        of.write(el)

def skd2vex(exp):
    outvex = exp+".vex"
    if os.path.exists(outvex):
        os.remove(outvex)
    # Convert SKD to VEX
    p = run(['/opt/sked/sked', exp+".skd"], stdout=PIPE, input='VEC '+outvex+'\rq\r', encoding='ascii')

def makev2d(exp):
    vf = open(exp+".v2d",'w')
    vf.write("vex = {0}.vex\n".format(exp))
    vf.write("antennas = Oe, Ow\n")
    vf.write("nCore=12\n")
    vf.write("nThread=1\n")
    vf.write("# Ensure we get cross-auto corrs, just in case (i.e. Oe X-pol correlated with Oe Y-pol)\n")
    vf.write("exhaustiveAutocorrs = true\n")
    vf.write("SETUP default\n")
    vf.write("{\n")
    vf.write(" tInt=1\n")
    vf.write(" # High res to be able to notch-filter RFI on Oe-Ow baseline\n")
    vf.write(" fftSpecRes=0.1 \n")
    vf.write(" specRes=0.1\n")
    vf.write("}\n")
    vf.write("DATASTREAM oe0\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = oe0.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM oe1\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = oe1.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM oe2\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = oe2.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM oe3\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = oe3.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM oe4\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = oe4.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM oe5\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = oe5.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM oe6\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = oe6.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM oe7\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = oe7.files\n")
    vf.write("}\n")
    vf.write("\n")
    vf.write("DATASTREAM ow0\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = ow0.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM ow1\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = ow1.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM ow2\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = ow2.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM ow3\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = ow3.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM ow4\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = ow4.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM ow5\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = ow5.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM ow6\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = ow6.files\n")
    vf.write("}\n")
    vf.write("DATASTREAM ow7\n")
    vf.write("{\n")
    vf.write("  format = VDIF/8224/2\n")
    vf.write("  filelist = ow7.files\n")
    vf.write("}\n")
    vf.write("\n")
    vf.write("ANTENNA Ow\n")
    vf.write("{\n")
    vf.write(" datastreams = ow0, ow1, ow2, ow3, ow4, ow5, ow6, ow7\n")
    vf.write(" sampling = REAL\n")
    vf.write(" toneSelection = all\n")
    vf.write(" phaseCalInt = 5\n")
    vf.write(" }\n")
    vf.write("\n")
    vf.write("ANTENNA Oe\n")
    vf.write("{\n")
    vf.write(" datastreams = oe0, oe1, oe2, oe3, oe4, oe5, oe6, oe7\n")
    vf.write(" sampling = REAL\n")
    vf.write(" toneSelection = all\n")
    vf.write(" phaseCalInt = 5\n")
    vf.write(" }\n")

def makemachines():
    ins = glob.glob("*.input")
    for i in ins:
        b = i.split(".")[0]
        mf = open(b + ".machines","w")
        for k in range(24):
            mf.write(socket.gethostname()+"\n")
        mf.close()

def mountfiles(exp):
    umount = "fusermount -u /mnt/fmdata"
    mount = "vbs_fs /mnt/fmdata -I '{0}*'".format(exp)
    gumount = "ssh oper@gyller " + umount
    gmount = "ssh oper@gyller " + mount
    usshfs = "fusermount -u /mnt/gyller-fmdata"
    sshfs = "sshfs oper@10.100.0.15:/mnt/fmdata /mnt/gyller-fmdata"
    for c in [umount, mount, gumount, gmount, usshfs, sshfs]:
        print("Running command " + c)
        os.system(c)
        time.sleep(1)

def listfiles(exp):
    print("NOTE: Will index all data with vsum. May take 10 minutes or so...")
    for mf in range(8):
        cmd = "vsum -s /mnt/fmdata/{0}_ow*_{1} > ow{1}.files".format(exp, mf)
        print("Running command "+cmd)
        os.system(cmd)
    for mf in range(8):
        cmd = "vsum -s /mnt/gyller-fmdata/{0}_oe*_{1} > oe{1}.files".format(exp, mf)
        print("Running command "+cmd)
        os.system(cmd)
    print("...done indexing data!")


## SCRIPT STARTS HERE

exp = sys.argv[1]
ans = input("Will run preparation actions for experiment " + exp + ". NOTE: This may unmount file-systems causing loss of paths and I/O limits. So, NEVER DO THIS WHEN RECORDING OR CORRELATING unless you know what you are doing! Type 'yes' to proceed:")
if not ans.lower()=="yes":
    print("Did not get yes, aborting")
    sys.exit(1)

getfslogs(exp)
getskd(exp)
skd2vex(exp)

# Read all lines of VEX file
vex = [l for l in open(exp+".vex")]
keep = True
of = open(exp+".vex","w")
start = ""
for line in vex:
    if "begin $MODE" in line:
        keep=False
        fillmode(of)
    if "end $MODE" in line:
        keep=True
    if "begin $BBC" in line:
        keep=False
        fillbbc(of)
    if "end $BBC" in line:
        keep=True
    if "begin $FREQ" in line:
        keep=False
        fillfreq(of)
    if "end $FREQ" in line:
        keep=True
    if "begin $IF" in line:
        keep=False
        fillif(of)
    if "end $IF" in line:
        keep=True
    if "begin $TRACKS" in line:
        keep=False
        filltracks(of)
    if "end $TRACKS" in line:
        of.write(line)
        of.write("$CLOCK;\n")
        fillclock(of, exp+"oe.log")
        fillclock(of, exp+"ow.log")
        fillEOP(of, start)
    if keep:
        of.write(line)
    if "start = " in line and start=="":
        year = line.split()[2][0:4]
        doy = str(int(line.split()[2][5:8])-2)
        start = year+"-"+doy
of.close()

makev2d(exp)
mountfiles(exp)
listfiles(exp)
os.system("vex2difx -v -v -v -d "+exp+".v2d")
# Ensure that the CalcServer is running: will restart if already exists
os.system("startCalcServer")
os.system("calcif2 *.calc")
makemachines()

print("SCRIPT FINISHED. Check the output. If all seems OK, start correlation (in a screen!) by running 'startdifx -n -f *.input -v'")
