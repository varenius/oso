import glob
import os

indir = "/mnt/raidz0/K-analysis_Onames/vgosdbs/"

infiles = glob.glob(indir + "*/*/*003*")
#infiles = glob.glob(indir + "*/*/20AUG14*003*")

out = "/home/eskil/nuSolve/Reports/batch_20210115/"
os.system("rm -rf " + out)
for f in infiles:
    cmd = "nuSolve -t batch.js " + f + " " + out + "/ GR save"
    print("Running CMD=", cmd)
    os.system(cmd)
    #cmd = "nuSolve -t batch.js " + f + " " + out + "/ PH no"
    #print("Running CMD=", cmd)
    #os.system(cmd)
