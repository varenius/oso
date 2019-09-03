import sys, os

# Get path of script
scriptpath = os.path.dirname(os.path.abspath(__file__))

# take schedule name as input, e.g. vt9248
exp = sys.argv[1]

if exp[2]=="9":
    year = "2019"
else:
    year = "202"+exp[2]

ftpaddr = "ftp://ivs.bkg.bund.de/pub/vlbi/ivsdata/aux/" + year + "/" + exp + "/" + exp + ".skd"

check = raw_input("Ready to fetch, drudg, and modify (SNP/PRC) experiment " + exp + ". NOTE: this will overwrite any existing files with this experiment name. Type go and hit enter to continue: " )
if check.strip() == "go":
    # Get schedule via wget, saving it in /usr2/sched/, e.g. /usr2/sched/vt9248.skd
    print("INFO: Downloading sked file...")
    wgetcmd = "wget --user anonymous " + ftpaddr + " -O /usr2/sched/" + exp + ".skd"
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
    print("INFO: Changing setupsx to setupbb in snp file...")
    sedcmd = "sed -i 's/setupsx/setupbb/g' /usr2/sched/"+exp+tel+".snp"
    os.system(sedcmd)
    print("INFO: ...done.")
    
    # copy template PRC file to /usr2/proc/expST.prc where ST is oe or ow
    print("INFO: Instead of drudging for PRC, copy template PRC...")
    cpcmd = "cp " + scriptpath + "/VGOS_default_prc." + tel + " /usr2/proc/" + exp + tel + ".prc"
    os.system(cpcmd)

    # change VT9248 to actual experiment name in PRC header
    print("INFO: ... and edit the PRC header to use actual experiment namt...")
    sedcmd = "sed -i 's/VT9248/" + exp.upper() + "/g' /usr2/proc/"+exp+tel+".prc"
    os.system(sedcmd)
    print("INFO: ...done.")
else: 
    print("Did not get go as answer so not doing anything.")
