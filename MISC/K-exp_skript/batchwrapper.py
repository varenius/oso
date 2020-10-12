import glob
import os

indir = "/home/eskil/vgosdb/NewAnalysisOctober2020/"

infiles = glob.glob(indir + "*/*/*003*")

for f in infiles:
    cmd = "nuSolve -t batch.js " + f + " /home/eskil/nuSolve/Reports/batch/ PH no"
    print("Running CMD=", cmd)
    os.system(cmd)
