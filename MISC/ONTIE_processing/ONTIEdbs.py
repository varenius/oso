import sys
import os
import glob

exp = sys.argv[1]
if exp == "all":
    exps = glob.glob("/data2/eskil/CORRELATED/on*")
else:
    exps = ["/data2/eskil/CORRELATED/"+exp+"/",]

def getDbName():
    for line in open(crep):
        if "DATABASE" in line:
            dbname = line.split()[-1]
            return dbname

for e in exps:
    datapath = e + "/1234/"
    outpath = "/data2/eskil/vgosdb_ONTIE/"
    eshort = e.split("/")[-2]
    crep = e + eshort + ".corr"
    
    db2make = getDbName()
    year = "20"+db2make[0:2]
    makec = "LC_ALL=C vgosDbMake -d {0} -t {1} -r OSO -o {2} {3}".format(db2make, crep, outpath, datapath)
    calcc = "vgosDbCalc {0}/{1}/{2}/{2}_V001_iOSO_kall.wrp".format(outpath, year, db2make)
    procc = "vgosDbProcLogs -k log {0}/{1}/{2}/{2}_V002_iOSO_kall.wrp".format(outpath, year, db2make)

    ans = raw_input("Process: '" + db2make + "' ? [y/n]")
    if ans =="y":
        os.system(makec)
        os.system(calcc)
        os.system(procc)
