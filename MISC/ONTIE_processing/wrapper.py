import glob
import os

indir = "/home/eskil/vgosdbs/ONTIE/"

infiles = glob.glob(indir + "*/*/*004*")
#infiles = glob.glob(indir + "*/*/20JAN11*004*")

out = "/home/eskil/nuSolve/Reports/batch_20210225/"
os.system("rm -rf " + out)
for f in infiles:
    #cmd = "nuSolve -t batch.js " + f + " " + out + "/ GR no"
    #print("Running CMD=", cmd)
    #os.system(cmd)
    cmd = "nuSolve -t batch.js " + f + " " + out + "/ PH save"
    print("Running CMD=", cmd)
    os.system(cmd)
