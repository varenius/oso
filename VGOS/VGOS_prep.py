#!/usr/bin/env python3
import sys, os
import datetime

print("Welcome to the OTT VGOS_prep script. Please answer the following questions:")
###########################
exp = input("QUESTION: Experiment, e.g. b22082 ? ").strip().lower()
print("INFO: OK, try to process experiment "+exp)
print()
###########################
dlans = input("QUESTION: Download schedule from IVS (yes/no) ? ").strip().lower()
if dlans =="yes" or dlans =="y":
    print("INFO: Will download schedule from IVS")
    dl = True
else:
    if os.path.exists("/usr2/sched/"+exp+".skd") or os.path.exists("/usr2/sched/"+exp+".vex"):
        print("INFO: Will using already existing file in /usr2/sched/")
        dl = False
    else:
        print("ERROR: Download not requested, but no matching skd/vex file found in /usr2/sched/. Did you forget to put it here?")
        print("ABORTING!")
        sys.exit(1)
print()
###########################
prcs = {"1":"vo-default", 
        "2": "vt2077-alternative", 
        "3": "on1323", 
        "4": "on1324", 
        "5": "on1325", 
        "6": "X-band from S/X R11091 (8x8 MHz overlap)",
        "7": "X-band from S/X RV157 (4x16 MHz overlap)",
        "8": "X-band from S/X T2 (8x4 MHz overlap)"
}
prcks = " ".join(["\n" + i+")"+prcs[i] for i in sorted(prcs.keys())])
print("INFO: Available frequency setup default PRC files are:\n{}\n".format(prcks))
prc = input("QUESTION: Please select setup using digit 1, 2, ...: ").strip().lower()
selprc = prcs[prc]
print("INFO: OK, selected setup is "+selprc)
print()
###########################
# get hostname of this FS machine, fulla or freja
host = os.uname()[1]
# Translate hostname to telescope 2 letter code for drudg
tels = {"fulla":"oe", "freja":"ow"}
tel = tels[host]
ant = input("QUESTION: This is machine " + host + " so I assume you will use antenna " + tel + " (yes/no) ? ")
if not (ant =="yes" or ant =="y"):
    tel = input("QUESTION: Then which antenna (oe/ow)? ").strip().lower()
print("INFO: OK, using " + tel)
print("")
###########################
recs = {"fulla":"gyller","freja":"skirner"}
rec = recs[host]
ans = input("QUESTION: This is machine " + host + " so I assume you will use recorder " + rec + " (yes/no) ? ")
if not (ans =="yes" or ans =="y"):
    rec = input("QUESTION: Then which recorder (gyller/skirner/kare)?").strip().lower()
print("INFO: OK, using " + rec)
print("")
###########################
mirrorans = input("QUESTION: Mirror other station snap file - useful to tag-along Oe/Ow with a On S/X experiment - (yes/no) ? ")
mirror = False
if (mirrorans =="yes" or mirrorans =="y"):
    mirror = True
    tagtel = input("QUESTION: Then which antenna to mirror (normally On)? ").strip().lower()
    print("INFO: OK, will mirror SNP file for " + tagtel)
print("")
###########################
print("QUESTION: Which experiment to start after this one?")
nextexp = input("          Type experiment name (e.g. b22087 without oe/ow), else leave blank: ").lower().strip()
print("")
###########################
a_stowans = input("QUESTION: Do you want to add a antenna=stow after prepant (yes/no) ? ").lower().strip()
a_stow = False
if (a_stowans =="yes" or a_stowans =="y"):
    a_stow = True
print("")
###########################
a_offans = input("QUESTION: Do you want to add a antenna=off after prepant (yes/no) ? ").lower().strip()
a_off = False
if (a_offans =="yes" or a_offans =="y"):
    a_off = True
print("")
###########################
a_calsour = input("QUESTION: Do you want 120 seconds observation on 3c286 at the end of the experiment?").lower().strip()
a_cals = False
if (a_calsour =="yes" or a_calsour =="y"):
    a_cals = True
print("")
###########################
a_sendlogans = input("QUESTION: Do you want to send the log file to IVS after the experiment?").lower().strip()
a_sendlog = False
if (a_sendlogans =="yes" or a_sendlogans =="y"):
    a_sendlog = True
print("")
###########################
# PRINT SUMMARY
print("")
print("###########################")
print("")
print("YOU HAVE MADE THE FOLLOWING CHOICES:")
print("Experiment: "+exp)
print("Download from IVS: "+dlans)
print("Frequency setup: "+selprc)
print("Telescope: " + tel)
print("Mirror other station snap file: " + mirrorans)
if mirror:
    print("     ... will mirror SNP file for " + tagtel)
print("Recorder: " + rec)
print("Next exp after sched_end:" + nextexp)
print("Put 'antenna=stow' after prepant: " + a_stowans)
print("Put 'antenna=off' after prepant: " + a_offans)
print("Observe 3c286 at the end of experiment: " + a_calsour)
print("Send the log file to IVS: "+a_sendlogans)
print("")
print("###########################")
print("")
check = input("FINAL QUESTION: Ready to prepare, and possibly overwrite, experiment files for exp " + exp + ". Proceed (yes/no) ? " ).strip().lower()
if not (check == "yes" or check == "y"):
    print("ABORTING!")
    sys.exit(0)
###########################
# START ACTUAL SCRIPT!
# Get path of script
scriptpath = os.path.dirname(os.path.realpath(__file__))
if dl:
    # Get schedule via wget, saving it in /usr2/sched/, e.g. /usr2/sched/vt9248.skd
    print("INFO: Downloading sked file...")
    wgetcmd = "fesh -f " + exp
    os.system(wgetcmd)

# drudg skd/vex file for SNP. 
if mirror:
    print("Mirroring, so will run DRUGG for antenna " + tagtel + " and then replace with actual antenna " + tel + " ...")
    drudgtel = tagtel
else:
    drudgtel = tel
print("INFO: Running DRUDG for telescope " + drudgtel + " ...")
drudgcmd = "drudg /usr2/sched/" + exp  + " " + drudgtel + " 3 0" 
os.system(drudgcmd)
if mirror:
    movecmd = "mv /usr2/sched/" + exp + drudgtel + ".snp /usr2/sched/" + exp + tel + ".snp"  
    os.system(movecmd)
    replacecmd = "sed -i 's/"+exp+","+tagtel+",/"+exp+","+tel+",/g' /usr2/sched/" + exp + tel + ".snp"  
    os.system(replacecmd)

# change setupsx to setupbb in SNP file
#print("INFO: Changing setupsx to setupbb and commenting out in snp file...")
sedcmd = "sed -i 's/setupsx/\"setupbb/g' /usr2/sched/"+exp+tel+".snp"
os.system(sedcmd)
#print("INFO: Commenting out any setupxx-calls in snp file...")
sedcmd = "sed -i 's/setupxx/\"setupxx/g' /usr2/sched/"+exp+tel+".snp"
os.system(sedcmd)
#print("INFO: Commenting out any setup01-calls in snp file...")
sedcmd = "sed -i 's/setup01/\"setup01/g' /usr2/sched/"+exp+tel+".snp"
os.system(sedcmd)

# copy template PRC file to /usr2/proc/expST.prc where ST is oe or ow
print("INFO: Instead of drudging for PRC, copy template PRC for "+ selprc)
if selprc=="vo-default":
    cpcmd = "cp " + scriptpath + "/PRC/VGOS_default_prc." + tel + " /usr2/proc/" + exp + tel + ".prc"
# Templates below are for Ow, but Oe is identical since differences are absorbed in station.prc
elif selprc=="vt2077-alternative":
    cpcmd = "cp " + scriptpath + "/PRC/vt2077ow.prc /usr2/proc/" + exp + tel + ".prc"
elif selprc=="on1323":
    cpcmd = "cp " + scriptpath + "/PRC/on1323ow.prc /usr2/proc/" + exp + tel + ".prc"
elif selprc=="on1324":
    cpcmd = "cp " + scriptpath + "/PRC/on1324ow.prc /usr2/proc/" + exp + tel + ".prc"
elif selprc=="on1325":
    cpcmd = "cp " + scriptpath + "/PRC/on1325ow.prc /usr2/proc/" + exp + tel + ".prc"
elif selprc=="X-band from S/X R11091 (8x8 MHz overlap)":
    cpcmd = "cp " + scriptpath + "/PRC/r11091_8x8MHz_xband_centered_32MHz_ow.prc /usr2/proc/" + exp + tel + ".prc"
elif selprc=="X-band from S/X RV157 (4x16 MHz overlap)":
    cpcmd = "cp " + scriptpath + "/PRC/rv157_4x16MHz_xband_centered_32MHz_ow.prc /usr2/proc/" + exp + tel + ".prc"
elif selprc=="X-band from S/X T2 (8x4 MHz overlap)":
    cpcmd = "cp " + scriptpath + "/PRC/t2_8x4MHz_xband_centered_32MHz_ow.prc /usr2/proc/" + exp + tel + ".prc"
os.system(cpcmd)

snpf = "/usr2/sched/"+exp+tel+".snp"
# Store lines in array
lines = []
for line in open(snpf):
    lines.append(line)
# Find first timetag
for line in lines:
    if line.startswith("!20"):
        starttime = datetime.datetime.strptime(line.strip()[1:], "%Y.%j.%H:%M:%S")
        break
preptime = (starttime+datetime.timedelta(minutes=-10)).strftime("%Y.%j.%H:%M:%S")
#print("starttime=", starttime, "preptime=", preptime)
#find last timetag
for line in reversed(lines):
    if line.startswith("!20"):
        stoptime = datetime.datetime.strptime(line.strip()[1:], "%Y.%j.%H:%M:%S")
        break
#calspreob 15 seconds after last scan,  calscan 15 minutes after preob
calspreob = (stoptime+datetime.timedelta(seconds=+15))
calstime = (calspreob+datetime.timedelta(seconds=+15))
calsend = (calstime+datetime.timedelta(minutes=+2))

wf = open(snpf, "w")
for line in lines:
    if a_cals:
        if "sched_end" in line:
            wf.write("scan_name="+calstime.strftime("%j-%H%M")+",ca"+exp[2:]+","+tel+",120,120\n")
            wf.write("source=3c286,133108.29,303033.0,2000.0,neutral\n")
            wf.write("!"+calspreob.strftime("%Y.%j.%H:%M:%S")+"\npreob\n")
            wf.write("!"+calstime.strftime("%Y.%j.%H:%M:%S")+"\n")
            wf.write("disk_record=on\ndisk_record\ndata_valid=on\nmidob\n")
            wf.write("!"+calsend.strftime("%Y.%j.%H:%M:%S")+"\n")
            wf.write("data_valid=off\ndisk_record=off\npostob\ncheckfb\n")
    wf.write(line)
    if "Rack=DBBC" in line:
        #Do not set recorded here, too late, instead set in PRC, see code later in this script
        wf.write("prepant\n")
        if a_stow:
            a_off = False
            wf.write("antenna=stow\n")
            wf.write("!"+preptime + "\n")
            wf.write("antenna=unstow\n")
            wf.write("antenna=run\n")
        if a_off:
            wf.write("antenna=off\n")
            wf.write("!"+preptime + "\n")
            wf.write("antenna=run\n")
    if starttime.strftime("%Y.%j.%H:%M:%S") in line:
        wf.write("antenna=ivs start\n")
if exp.startswith("b2") or exp.startswith("c2"):
    #VGOSB/C session, include auto-transfer to ishioka
    print("INFO: This is a VGOSB or VGOSC experiment, so adding automatic data transfer to GSI after exp finish.")
    wf.write("sy=etransfer.py {0} gsi {1} {2}\n".format(rec, exp, tel))
if not nextexp=="":
    print("INFO: Adding schedule={0}{1},#1 as last line of SNP file.".format(nextexp, tel))
    wf.write("schedule={0}{1},#1\n".format(nextexp, tel))
else:
    wf.write("antenna=stow\n")
#   wf.write("antenna=off\n")
if a_sendlog:
    wf.write("sendlog\n")
wf.close()

# Also edit PRC file to insert flexbuff_config command at start of exper_initi.
# Previously we had this at start of SNP file, but this is after exper_initi,
# so FS will set the "fb_mode" and similar commands first and THEN change
# recorder, which means the recording would fail to record properly (since no mode set).
prcf = "/usr2/proc/"+exp+tel+".prc"
# Store lines in array
plines = []
for line in open(prcf):
    plines.append(line)
pf = open(prcf, "w")
for line in plines:
    pf.write(line)
    if "define  exper_initi" in line:
        pf.write("init_{0}\n".format(rec))
print("INFO: All done. You may want to check the resulting /usr2/sched/{0}{1}.snp and /usr2/proc/{0}{1}.prc files.".format(exp,tel))
