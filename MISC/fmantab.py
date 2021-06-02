#!/usr/bin/env python3
import sys, os
import datetime
from subprocess import PIPE, run

def get_timerange(f, comp):
    print("Checking " + f + "...")
    fstart = f.split("/")[-1].split("_")[2].split(".")[0]
    stime = datetime.datetime.strptime(fstart,"%Y-%m-%d--%H-%M-%S")
    cmd = ["ssh", comp, "tail -n 1 "+f]
    rc = run(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    end = rc.stdout.split(" ")[0]
    etime = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%f')
    return stime, etime

#Find start/end times of observation
vex = sys.argv[1]
start = ""
end = ""
for line in open(vex):
    if not line.startswith("*"):
        if "exper_name =" in line:
            exp = line.split("=")[1].strip()[:-1].lower()
        if "start = " in line:
            stime = datetime.datetime.strptime(line[12:-2],"%Yy%jd%Hh%Mm%Ss")
            if start == "":
                start = stime
        if "station = Ow" in line:
            scan = float(line.split(":")[2].split()[0])
            stop = stime + datetime.timedelta(seconds = scan)
print("VEX file {0} found to cover timerange {1} to {2} for experiment {3}.".format(vex, start, stop, exp))

print("Checking all available TPI log files for a matching one...")
print("Checking for OW...")
#get list of possible logfiles
command = ["ssh", "freja", "ls /usr2/oper/eskil/eskil.oso.git/VGOS/DBBC3/MULTICAST_DBBC3*"]
rc = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
files = rc.stdout.split("\n")
match = ""
for f in files[:-1]:
    fstart, fstop = get_timerange(f, "freja")
    if (start > fstart) and (stop < fstop):
        match = f
        fn = f.split("/")[-1]
        print("Matching TPI file found: " + f)
        mcdata = "OW_"+fn
        os.system("scp freja:"+f+ " "+mcdata)
        fslog = exp+"ow.log"
        print("Assuming we want to create antab file using FS log " + fslog)
        if start > datetime.datetime(2021,1,19):
            tcal = "/home/oper/eskil/eskil.oso.git/VGOS/DBBC3/OW_post_2021-01-19.tcal.jansky.txt"
        else:
            tcal = "/home/oper/eskil/eskil.oso.git/VGOS/DBBC3/OW_pre_2021-01-19.tcal.jansky.txt"
        cmd = "python /home/oper/eskil/eskil.oso.git/VGOS/DBBC3/mcastlog2antab.py {0} {1} {2} {3}ow.antab".format(fslog, mcdata, tcal, exp)
        print("Creating antab using command "+ cmd)
        os.system(cmd)
        break
print("Checking for OE...")
#get list of possible logfiles
command = ["ssh", "fulla", "ls /usr2/oper/eskil/eskil.oso.git/VGOS/DBBC3/MULTICAST_DBBC3*"]
rc = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
files = rc.stdout.split("\n")
match = ""
for f in files[:-1]:
    fstart, fstop = get_timerange(f, "fulla")
    if (start > fstart) and (stop < fstop):
        match = f
        fn = f.split("/")[-1]
        print("Matching TPI file found: " + f)
        mcdata = "OE_"+fn
        os.system("scp fulla:"+f+ " "+mcdata)
        fslog = exp+"oe.log"
        print("Assuming we want to create antab file using FS log " + fslog)
        if start > datetime.datetime(2020,12,2):
            tcal = "/home/oper/eskil/eskil.oso.git/VGOS/DBBC3/OE_post_2020-12-02.tcal.jansky.txt"
        else:
            tcal = "/home/oper/eskil/eskil.oso.git/VGOS/DBBC3/OE_post_2020-12-02.tcal.jansky.txt"
        cmd = "python /home/oper/eskil/eskil.oso.git/VGOS/DBBC3/mcastlog2antab.py {0} {1} {2} {3}oe.antab".format(fslog, mcdata, tcal, exp)
        print("Creating antab using command "+ cmd)
        os.system(cmd)
        break
combantab = exp+"oe+ow.antab"
os.system("cat *antab > "+combantab)
print("...DONE! File " + combantab + " should now contain antab data for both OE and OW for exp " + exp+ ". Enjoy!")
