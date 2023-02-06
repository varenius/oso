#!/usr/bin/env python3
import sys, os
import datetime

print("Welcome to the OTT VGOS_prep script. Please answer the following questions:")
###########################
exp = input("QUESTION: Experiment, e.g. b22082 ? ").strip().lower()
print("INFO: OK, try to process experiment "+exp)
print()
###########################
dl = input("QUESTION: Download schedule from IVS (yes/no) ? ").strip().lower()
if dl =="yes" or dl =="y":
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
prcs = {"1":"vo-default", "2": "vt2077-alternative", "3": "on1323", "4": "on1324", "5": "on1325", "6": "X-band of S/X R1"}
prcks = " ".join([i+") "+prcs[i] for i in sorted(prcs.keys())])
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
print("QUESTION: Do you want to automatically start another experiment after this?")
nextexp = input("          If so, typ experiment name (e.g. b22087 without oe/ow). Else leave blank: ").lower().strip()
print("")
###########################
ans = input("QUESTION: Do you want to add a antenna=off after prepant (yes/no) ? ").lower().strip()
a_off = 0
if (ans =="yes" or ans =="y"):
    a_off = 1
print("")
###########################
check = input("FINAL QUESTION: Ready to prepare, and possibly overwrite, experiment files for " + exp + ". Proceed (yes/no) ? " ).strip().lower()
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
print("INFO: Running DRUDG for telescope " + tel + " ...")
drudgcmd = "drudg /usr2/sched/" + exp  + " " + tel + " 3 0" 
os.system(drudgcmd)

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
wf = open(snpf, "w")
for line in lines:
    wf.write(line)
    if "Rack=DBBC" in line:
        wf.write("init_{0}\n".format(rec))
        wf.write("prepant\n")
        if a_off==1:
            wf.write("antenna=off\n")
        wf.write("!"+preptime + "\n")
        wf.write("antenna=run\n")
if exp.startswith("b2") or exp.startswith("c2"):
    #VGOSB/C session, include auto-transfer to ishioka
    print("INFO: This is a VGOSB or VGOSC experiment, so adding automatic data transfer to GSI after exp finish.")
    wf.write("sy=etransfer.py {0} gsi {1} {2}\n".format(rec, exp, tel))
if not nextexp=="":
    print("INFO: Adding schedule={0}{1},#1 as last line of SNP file.".format(nextexp, tel))
    wf.write("schedule={0}{1},#1\n".format(nextexp, tel))
else:
    wf.write("antenna=off\n")
wf.close()
print("INFO: All done. You may want to check the resulting /usr2/sched/{0}{1}.snp and /usr2/proc/{0}{1}.prc files.".format(exp,tel))
