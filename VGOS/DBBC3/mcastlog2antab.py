import sys
import datetime

def bbcinfo(bbc):
#BBC IF POL CENTERFREQ
    bbcs = {}
    bbcs['001l']=[1,'X',  3464.40 ]
    bbcs['002l']=[1,'X',  3432.40 ]
    bbcs['003l']=[1,'X',  3368.40 ]
    bbcs['004l']=[1,'X',  3304.40 ]
    bbcs['005l']=[1,'X',  3208.40 ]
    bbcs['006l']=[1,'X',  3080.40 ]
    bbcs['007l']=[1,'X',  3048.40 ]
    bbcs['008l']=[1,'X',  3016.40 ]
    bbcs['009l']=[2,'Y',  3464.40 ]
    bbcs['010l']=[2,'Y',  3432.40 ]
    bbcs['011l']=[2,'Y',  3368.40 ]
    bbcs['012l']=[2,'Y',  3304.40 ]
    bbcs['013l']=[2,'Y',  3208.40 ]
    bbcs['014l']=[2,'Y',  3080.40 ]
    bbcs['015l']=[2,'Y',  3048.40 ]
    bbcs['016l']=[2,'Y',  3016.40 ]
    bbcs['017l']=[3,'X',  5736.40 ]
    bbcs['018l']=[3,'X',  5704.40 ]
    bbcs['019l']=[3,'X',  5640.40 ]
    bbcs['020l']=[3,'X',  5576.40 ]
    bbcs['021l']=[3,'X',  5480.40 ]
    bbcs['022l']=[3,'X',  5352.40 ]
    bbcs['023l']=[3,'X',  5320.40 ]
    bbcs['024l']=[3,'X',  5288.40 ]
    bbcs['025l']=[4,'Y',  5736.40 ]
    bbcs['026l']=[4,'Y',  5704.40 ]
    bbcs['027l']=[4,'Y',  5640.40 ]
    bbcs['028l']=[4,'Y',  5576.40 ]
    bbcs['029l']=[4,'Y',  5480.40 ]
    bbcs['030l']=[4,'Y',  5352.40 ]
    bbcs['031l']=[4,'Y',  5320.40 ]
    bbcs['032l']=[4,'Y',  5288.40 ]
    bbcs['033l']=[5,'X',  6856.40 ]
    bbcs['034l']=[5,'X',  6824.40 ]
    bbcs['035l']=[5,'X',  6760.40 ]
    bbcs['036l']=[5,'X',  6696.40 ]
    bbcs['037l']=[5,'X',  6600.40 ]
    bbcs['038l']=[5,'X',  6472.40 ]
    bbcs['039l']=[5,'X',  6440.40 ]
    bbcs['040l']=[5,'X',  6408.40 ]
    bbcs['041l']=[6,'Y',  6856.40 ]
    bbcs['042l']=[6,'Y',  6824.40 ]
    bbcs['043l']=[6,'Y',  6760.40 ]
    bbcs['044l']=[6,'Y',  6696.40 ]
    bbcs['045l']=[6,'Y',  6600.40 ]
    bbcs['046l']=[6,'Y',  6472.40 ]
    bbcs['047l']=[6,'Y',  6440.40 ]
    bbcs['048l']=[6,'Y',  6408.40 ]
    bbcs['049l']=[7,'X', 10696.40 ]
    bbcs['050l']=[7,'X', 10664.40 ]
    bbcs['051l']=[7,'X', 10600.40 ]
    bbcs['052l']=[7,'X', 10536.40 ]
    bbcs['053l']=[7,'X', 10440.40 ]
    bbcs['054l']=[7,'X', 10312.40 ]
    bbcs['055l']=[7,'X', 10280.40 ]
    bbcs['056l']=[7,'X', 10248.40 ]
    bbcs['057l']=[8,'Y', 10696.40 ]
    bbcs['058l']=[8,'Y', 10664.40 ]
    bbcs['059l']=[8,'Y', 10600.40 ]
    bbcs['060l']=[8,'Y', 10536.40 ]
    bbcs['061l']=[8,'Y', 10440.40 ]
    bbcs['062l']=[8,'Y', 10312.40 ]
    bbcs['063l']=[8,'Y', 10280.40 ]
    bbcs['064l']=[8,'Y', 10248.40 ]
    bbcs['001u']=[1,'X',  3496.40 ]
    bbcs['002u']=[1,'X',  3464.40 ]
    bbcs['003u']=[1,'X',  3400.40 ]
    bbcs['004u']=[1,'X',  3336.40 ]
    bbcs['005u']=[1,'X',  3240.40 ]
    bbcs['006u']=[1,'X',  3112.40 ]
    bbcs['007u']=[1,'X',  3080.40 ]
    bbcs['008u']=[1,'X',  3048.40 ]
    bbcs['009u']=[2,'Y',  3496.40 ]
    bbcs['010u']=[2,'Y',  3464.40 ]
    bbcs['011u']=[2,'Y',  3400.40 ]
    bbcs['012u']=[2,'Y',  3336.40 ]
    bbcs['013u']=[2,'Y',  3240.40 ]
    bbcs['014u']=[2,'Y',  3112.40 ]
    bbcs['015u']=[2,'Y',  3080.40 ]
    bbcs['016u']=[2,'Y',  3048.40 ]
    bbcs['017u']=[3,'X',  5704.40 ]
    bbcs['018u']=[3,'X',  5672.40 ]
    bbcs['019u']=[3,'X',  5608.40 ]
    bbcs['020u']=[3,'X',  5544.40 ]
    bbcs['021u']=[3,'X',  5448.40 ]
    bbcs['022u']=[3,'X',  5320.40 ]
    bbcs['023u']=[3,'X',  5288.40 ]
    bbcs['024u']=[3,'X',  5256.40 ]
    bbcs['025u']=[4,'Y',  5704.40 ]
    bbcs['026u']=[4,'Y',  5672.40 ]
    bbcs['027u']=[4,'Y',  5608.40 ]
    bbcs['028u']=[4,'Y',  5544.40 ]
    bbcs['029u']=[4,'Y',  5448.40 ]
    bbcs['030u']=[4,'Y',  5320.40 ]
    bbcs['031u']=[4,'Y',  5288.40 ]
    bbcs['032u']=[4,'Y',  5256.40 ]
    bbcs['033u']=[5,'X',  6824.40 ]
    bbcs['034u']=[5,'X',  6792.40 ]
    bbcs['035u']=[5,'X',  6728.40 ]
    bbcs['036u']=[5,'X',  6664.40 ]
    bbcs['037u']=[5,'X',  6568.40 ]
    bbcs['038u']=[5,'X',  6440.40 ]
    bbcs['039u']=[5,'X',  6408.40 ]
    bbcs['040u']=[5,'X',  6376.40 ]
    bbcs['041u']=[6,'Y',  6824.40 ]
    bbcs['042u']=[6,'Y',  6792.40 ]
    bbcs['043u']=[6,'Y',  6728.40 ]
    bbcs['044u']=[6,'Y',  6664.40 ]
    bbcs['045u']=[6,'Y',  6568.40 ]
    bbcs['046u']=[6,'Y',  6440.40 ]
    bbcs['047u']=[6,'Y',  6408.40 ]
    bbcs['048u']=[6,'Y',  6376.40 ]
    bbcs['049u']=[7,'X', 10664.40 ]
    bbcs['050u']=[7,'X', 10632.40 ]
    bbcs['051u']=[7,'X', 10568.40 ]
    bbcs['052u']=[7,'X', 10504.40 ]
    bbcs['053u']=[7,'X', 10408.40 ]
    bbcs['054u']=[7,'X', 10280.40 ]
    bbcs['055u']=[7,'X', 10248.40 ]
    bbcs['056u']=[7,'X', 10216.40 ]
    bbcs['057u']=[8,'Y', 10664.40 ]
    bbcs['058u']=[8,'Y', 10632.40 ]
    bbcs['059u']=[8,'Y', 10568.40 ]
    bbcs['060u']=[8,'Y', 10504.40 ]
    bbcs['061u']=[8,'Y', 10408.40 ]
    bbcs['062u']=[8,'Y', 10280.40 ]
    bbcs['063u']=[8,'Y', 10248.40 ]
    bbcs['064u']=[8,'Y', 10216.40 ]
    freq = bbcs[bbc][-1]
    pol = bbcs[bbc][-2]
    return pol, freq

def get_scans(fslog):
    #2020.132.18:00:01.04:data_valid=on
    #2020.132.18:00:30.00:data_valid=off
    scans = []
    for l in open(fslog):
        if "data_valid=on" in l:
            time = l.split(":d")[0]
            beg = datetime.datetime.strptime(time, "%Y.%j.%H:%M:%S.%f")
            #beg = beg.replace(tzinfo=timezone.utc)
        if "data_valid=off" in l:
            time = l.split(":d")[0]
            end = datetime.datetime.strptime(time, "%Y.%j.%H:%M:%S.%f")
            #end = end.replace(tzinfo=timezone.utc)
            scans.append([beg, end])
    return scans

def get_tsys(mcastlog, tcaldata):
    tpidata = []
    sid = 0 # scan id
    # margin of data to include before and after scan
    dt = datetime.timedelta(seconds = 1)
    for l in open(mcastlog):
        if "BBC001" in l: # Use timestame of first BBC, no big difference anyway and only one time for all BBCs in antab
            ls = l.split()
            tr = ls[0] # 2020-11-24T19:32:15.365789
            t = datetime.datetime.strptime(tr,'%Y-%m-%dT%H:%M:%S.%f')
            bbcdata = []
        if "BBC0" in l:
            ls = l.split()
            bbc = ls[2][3:6] # 001, 002...
            tpid = ls[3].split(",")
            # NOTE: SHOULD BE THIS; BUT SIGN IS FLIPPED, so OFF is ON n v124 data
            #BBC001 Total Power USB On
            #BBC001 Total Power LSB On
            #BBC001 Total Power USB Off
            #BBC001 Total Power LSB Off
            uon = int(tpid[5])
            lon = int(tpid[6])
            uoff = int(tpid[7])
            loff = int(tpid[8])
            if int(bbc)<=16:
                # Use LSB
                tpi_on = lon
                tpi_off = loff
                pol, freq = bbcinfo(bbc+'l')
            else:
                # Use USB
                tpi_on = uon
                tpi_off = uoff
                pol, freq = bbcinfo(bbc+'u')
            tcal = tcaldata[pol][str(freq)] # Jy
            try:
                tpicont = tcal * 0.5 *(tpi_on + tpi_off)/(tpi_on - tpi_off) # Account for noise diode being on 50% of the time
            except ZeroDivisionError:
                tpicont = -1
            ## FIX CONT_CAL DISP SIGN BUG
            tpicont = -1*tpicont
            bbcdata.append(tpicont)
        if "BBC064" in l:
            tpidata.append([t, bbcdata])
    return tpidata

def get_tcaldata(tcalfile):
    tcaldata = {}
    tcaldata['X'] = {}
    tcaldata['Y'] = {}
    for line in open(tcalfile):
        if not line.startswith('#'):
            ls = line.split()
            pol = ls[0]
            freq = ls[1]
            tcal = ls[2]
            tcaldata[pol][freq]=float(tcal)
    return tcaldata

def write_antab(tpidata, scans, outfile, ant, exp):
    of = open(outfile,"w")
    of.write("!\n")
    of.write("!INFO: Amplitude calibration data for antenna {} in experiment {}.\n".format(ant, exp))
    of.write("!INFO: For use with AIPS task ANTAB. \n".format(ant, exp))
    of.write("!\n")
    of.write("!\n")
   #HEADER
    #  i) CONTROL group:     specifies default input format for Tsys or
    #                        Tant entries.
    #cstr = "CONTROL INDEX = " 
    #cstr += "'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', "  
    #cstr += "'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', "
    #cstr += "'X9', 'X10', 'X11', 'X12', 'X13', 'X14', 'X15', 'X16', "
    #cstr += "'Y9', 'Y10', 'Y11', 'Y12', 'Y13', 'Y14', 'Y15', 'Y16', " 
    #cstr += "'X17', 'X18', 'X19', 'X20', 'X21', 'X22', 'X23', 'X24', " 
    #cstr += "'Y17', 'Y18', 'Y19', 'Y20', 'Y21', 'Y22', 'Y23', 'Y24', " 
    #cstr += "'X25', 'X26', 'X27', 'X28', 'X29', 'X30', 'X31', 'X32', "
    #cstr += "'Y25', 'Y26', 'Y27', 'Y28', 'Y29', 'Y30', 'Y31', 'Y32' "
    #cstr += "/"
    #cstr = "CONTROL INDEX = " 
    #cstr += "'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', "  
    #cstr += "'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', "
    #cstr += "'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', "
    #cstr += "'L9', 'L10', 'L11', 'L12', 'L13', 'L14', 'L15', 'L16', " 
    #cstr += "'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'R23', 'R24', " 
    #cstr += "'L17', 'L18', 'L19', 'L20', 'L21', 'L22', 'L23', 'L24', " 
    #cstr += "'R25', 'R26', 'R27', 'R28', 'R29', 'R30', 'R31', 'R32', "
    #cstr += "'L25', 'L26', 'L27', 'L28', 'L29', 'L30', 'L31', 'L32' "
    #cstr += "/"
    #of.write(cstr+"\n")

    # WRITE GAIN
    of.write("!\n")
    of.write("!INFO: Flat GAIN curve\n")
    of.write("!INFO: Polarisations are Horizontal (H) and Vertical (V). However,\n")
    of.write("!      below R and L are used instead, because software assume RCP/LCP\n")
    of.write("!      as the possible polarisations number 1/2 in data. But R=H, L=V.\n")
    of.write("!\n")
    if ant == "OW":
        dpfu = 0.035
        gain = "GAIN OW ELEV DPFU = "+str(dpfu)+" POLY = 1.0 /"
    elif ant == "OE":
        dpfu = 0.025
        gain = "GAIN OE ELEV DPFU = "+str(dpfu)+" POLY = 1.0 /"
    of.write(gain+"\n")

    # WRITE TSYS
    #Day_no  hh:mm:ss.ss  col1 col2 ... etc
    #Example:
    # TSYS SC FT = 1.05 INDEX = 'R1:8', 'L1:8' /
    # 321 20:32.78  32.6 33.4 ! Values for RCP, LCP
    # 321 20:34:01  31.6 35.8
    of.write("!\n")
    of.write("!INFO: FT=Factor by which to multiply all values.\n")
    of.write("!\n")
    cstr = "TSYS {} FT = 1.0 INDEX ".format(ant)
    cstr += "'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', "  
    cstr += "'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', "
    cstr += "'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16', "
    cstr += "'L9', 'L10', 'L11', 'L12', 'L13', 'L14', 'L15', 'L16', " 
    cstr += "'R17', 'R18', 'R19', 'R20', 'R21', 'R22', 'R23', 'R24', " 
    cstr += "'L17', 'L18', 'L19', 'L20', 'L21', 'L22', 'L23', 'L24', " 
    cstr += "'R25', 'R26', 'R27', 'R28', 'R29', 'R30', 'R31', 'R32', "
    cstr += "'L25', 'L26', 'L27', 'L28', 'L29', 'L30', 'L31', 'L32' "
    cstr += "/"
    of.write(cstr+"\n")
    # Loop through TSYS data
    # margin of data to include before and after scan
    dt = datetime.timedelta(seconds = 1)
    sid = 0 # scan id, start at 0
    of.write("!\n")
    of.write("!INFO: Negative values or values of 999.9 are assumed indefinite.\n")
    of.write("!INFO: DOY HH:MM:SS.ss TSYS...\n")
    of.write("!\n")
    for tpid in tpidata:
        d = tpid[0]
        while (d > scans[sid][1]+dt): # if we are past the end of the scan, shift scan index
            if sid < len(scans)-1:
                sid +=1
                of.write("!SCAN\n")
            else:
                break
        if (d > scans[sid][0]-dt) and (d < scans[sid][1]+dt): # we are inside scan
            doy = d.timetuple().tm_yday
            ts = d.strftime("%H:%M:%S.%f")[:-4]
            res = "{0} {1}".format(doy, ts)
            for t in tpid[1]:
                tent = " {:.2f}".format(t*dpfu) # Convert from Jansky to Kelvin
                res += tent
            of.write(res+"\n")
    # Write finish line
    of.write("/\n")
    of.close()

fslog = sys.argv[1]
mcastlog = sys.argv[2]
tcalfile = sys.argv[3]
outfile = sys.argv[4]

if "oe." in fslog:
    ant="OE"
elif "ow." in fslog:
    ant="OW"
exp = fslog.split("/")[-1][0:6]
tcaldata = get_tcaldata(tcalfile)
tsysdata = get_tsys(mcastlog, tcaldata)
scans = get_scans(fslog)
write_antab(tsysdata, scans, outfile, ant, exp)
