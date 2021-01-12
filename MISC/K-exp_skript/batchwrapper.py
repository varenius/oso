import glob
import os

#indir = "/mnt/raidz0/K-analysis_Onames/vgosdbs/"
indir = "/mnt/raidz0/K-analysis_Onames/vgosDb_new/"

#infiles = glob.glob(indir + "*/*/*003*")
infiles = glob.glob(indir + "*/*/20AUG10*003*")

out = "/home/eskil/nuSolve/Reports/batch_20210112/"
os.system("rm -rf " + out)
for f in infiles:
    cmd = "nuSolve -t batch.js " + f + " " + out + "/ GR save"
    #cmd = "nuSolve -t batch.js " + f + " " + out + "/ GR no"
    print("Running CMD=", cmd)
    #os.system(cmd)
    #cmd = "nuSolve -t batch.js " + f + " " + out + "/ PH no"
    #print("Running CMD=", cmd)
    #os.system(cmd)
