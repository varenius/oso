#!/usr/bin/env python 
import sys, os
import datetime

# Get path of script
scriptpath = os.path.dirname(os.path.realpath(__file__))

# take schedule name and year as input, e.g. vt9248 2019
exp = sys.argv[1]
year = sys.argv[2]
# Check if we should download schedule, or assume it already exists locally
dl=False
if (len(sys.argv)==4) and (sys.argv[3]=="dl"):
    dl=True


#if exp[2]=="9":
#    year = "2019"
#else:
#    year = "202"+exp[2]

ftpaddr = "ftp://ivs.bkg.bund.de/pub/vlbi/ivsdata/aux/" + year + "/" + exp + "/" + exp + ".skd"

check = raw_input("Ready to fetch, drudg, and modify (SNP/PRC) experiment " + exp + ". NOTE: this will overwrite any existing files with this experiment name. Type go and hit enter to continue: " )
if check.strip() == "go":
    if dl:
        # Get schedule via wget, saving it in /usr2/sched/, e.g. /usr2/sched/vt9248.skd
        print("INFO: Downloading sked file...")
        #wgetcmd = "wget --user anonymous " + ftpaddr + " -O /usr2/sched/" + exp + ".skd"
        wgetcmd = "fesh -f " + exp
        os.system(wgetcmd)
        print("INFO: ...done.")
    
    # get hostname of this FS machine, fulla or freja
    host = os.uname()[1]
    # Translate hostname to telescope 2 letter code for drudg
    tels = {"fulla":"oe", "freja":"ow"}
    tel = tels[host]
    # TODO: Could also read location.ctl if setup properly
    
    # drudg sked file for SNP. 
    print("INFO: host is " + host + " so running drudg for telescope " + tel + " ...")
    drudgcmd = "drudg /usr2/sched/" + exp + ".skd " + tel + " 3 0" 
    os.system(drudgcmd)
    print("INFO: ...done.")
    
    # change setupsx to setupbb in SNP file
    print("INFO: Changing setupsx to setupbb and commenting in snp file...")
    sedcmd = "sed -i 's/setupsx/\"setupbb/g' /usr2/sched/"+exp+tel+".snp"
    os.system(sedcmd)
    print("INFO: Commenting out setupxx in snp file...")
    sedcmd = "sed -i 's/setupxx/\"setupxx/g' /usr2/sched/"+exp+tel+".snp"
    os.system(sedcmd)
    #print("INFO: ... and comment out disk_pos and ready_disk and checkmk5...")
    #sedcmd = "sed -i 's/^disk_pos/\"disk_pos/g' /usr2/sched/"+exp+tel+".snp"
    #os.system(sedcmd)
    #sedcmd = "sed -i 's/^ready_disk/\"ready_disk/g' /usr2/sched/"+exp+tel+".snp"
    #os.system(sedcmd)
    #sedcmd = "sed -i 's/^checkmk5/\"checkmk5/g' /usr2/sched/"+exp+tel+".snp"
    #os.system(sedcmd)
    print("INFO: ...done.")
    
    # copy template PRC file to /usr2/proc/expST.prc where ST is oe or ow
    print("INFO: Instead of drudging for PRC, copy template PRC...")
    cpcmd = "cp " + scriptpath + "/VGOS_default_prc." + tel + " /usr2/proc/" + exp + tel + ".prc"
    os.system(cpcmd)

    snpf = "/usr2/sched/"+exp+tel+".snp"
    # Store lines in array
    lines = []
    for line in open(snpf):
        lines.append(line)
    # Find first timetag
    for line in lines:
        if line.startswith("!"+year+"."):
            starttime = datetime.datetime.strptime(line.strip()[1:], "%Y.%j.%H:%M:%S")
            break
    preptime = (starttime+datetime.timedelta(minutes=-10)).strftime("%Y.%j.%H:%M:%S")
    #print("starttime=", starttime, "preptime=", preptime)
    wf = open(snpf, "w")
    for line in lines:
        wf.write(line)
        if "Rack=DBBC" in line:
            #wf.write("mk5=datastream=clear\n")
            #wf.write("mk5=datastream=add:{thread}:*\n")
            wf.write("prepant\n")
            wf.write("!"+preptime + "\n")
    wf.close()
    print("All done.")
else: 
    print("Did not get go as answer so not doing anything.")
