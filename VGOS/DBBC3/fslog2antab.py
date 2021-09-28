import sys
import datetime
import numpy as np

def get_tsys(fslog):
#2021.266.12:20:01.38#dbtcn#tsys/ 001l, 71.0, 002l, 78.6, 003l, 77.8, 004l, 63.7, 005l, 74.3, 006l, 89.0, 007l, 76.2, 008l, 87.0, ia,155.2
#2021.266.12:20:01.38#dbtcn#tsys/ 009l, 51.7, 010l, 54.8, 011l, 55.8, 012l, 46.7, 013l, 66.3, 014l, 69.8, 015l, 65.2, 016l, 64.5, ib, 68.6
#2021.266.12:20:01.38#dbtcn#tsys/ 017u, 54.4, 018u, 54.2, 019u, 57.7, 020u, 47.9, 021u, 40.2, 022u, 50.0, 023u, 49.3, 024u, 47.2, ic, 74.7
#2021.266.12:20:01.38#dbtcn#tsys/ 025u, 34.4, 026u, 35.5, 027u, 38.1, 028u, 32.2, 029u, 36.1, 030u, 48.8, 031u, 50.9, 032u, 47.0, id, 59.5
#2021.266.12:20:01.38#dbtcn#tsys/ 033u, 49.8, 034u, 51.7, 035u, 51.2, 036u, 45.2, 037u, 53.4, 038u, 50.1, 039u, 47.1, 040u, 44.3, ie, 80.8
#2021.266.12:20:01.38#dbtcn#tsys/ 041u, 49.7, 042u, 50.5, 043u, 51.8, 044u, 49.9, 045u, 53.9, 046u, 49.2, 047u, 47.7, 048u, 44.3, if, 59.8
#2021.266.12:20:01.38#dbtcn#tsys/ 049u, 88.2, 050u, 91.4, 051u,106.2, 052u,108.1, 053u, 83.6, 054u, 80.1, 055u, 79.8, 056u, 89.6, ig, 49.3
#2021.266.12:20:01.38#dbtcn#tsys/ 057u, 90.6, 058u, 89.3, 059u, 89.9, 060u, 87.3, 061u, 86.4, 062u, 78.6, 063u, 78.4, 064u, 78.3, ih, 61.3
    tsdata = []
    for l in open(fslog):
        if "#dbtcn#tsys/" in l:
            if "001l" in l:
                tr = l.split("#")[0]
                t = datetime.datetime.strptime(tr, "%Y.%j.%H:%M:%S.%f")
                # Clear memory since we have new timerange
                valsnow = []
                valsnow.append(t)
            ts = l.strip().split("/")[1].split(",")
            vals = ts[1::2][0:-1] # Ignore last if value
            for vr in vals:
                if "$$$" in vr:
                    v = -1
                else:
                    v = float(vr)
                valsnow.append(v)
            if "064u" in l:
                tsdata.append(valsnow)
                # Done with this time
    return tsdata

def write_antab(tsysdata, outfile, ant, exp):
    # HEADER
    of = open(outfile,"w")
    of.write("!\n")
    of.write("!INFO: Amplitude calibration data for antenna {} in experiment {}.\n".format(ant, exp))
    of.write("!INFO: For use with AIPS task ANTAB. \n".format(ant, exp))
    of.write("!\n")
    of.write("!\n")

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
    of.write("!\n")
    of.write("!INFO: Negative values or values of 999.9 are assumed indefinite.\n")
    of.write("!INFO: DOY HH:MM:SS.ss TSYS...\n")
    of.write("!\n")
    for td in tsysdata:
        d = td[0]
        doy = d.timetuple().tm_yday
        ts = d.strftime("%H:%M:%S.%f")[:-4]
        res = "{0} {1}".format(doy, ts)
        for t in td[1:]:
            res += " {:.2f}".format(t) 
        of.write(res+"\n")
    # Write finish line
    of.write("/\n")
    of.close()

fslog = sys.argv[1]
outfile = sys.argv[2]

if "oe." in fslog:
    ant="OE"
elif "ow." in fslog:
    ant="OW"
exp = fslog.split("/")[-1][0:6]
tsysdata = get_tsys(fslog)
write_antab(tsysdata, outfile, ant, exp)
