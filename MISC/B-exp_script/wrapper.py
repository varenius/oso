import glob
import os

indir = "/home/eskil/bexp_vgosDb/"

indirs = glob.glob(indir + "*/*")

out = "/home/eskil/nuSolve/Reports/bexp_res/20210121"
os.system("rm -rf " + out)
for d in indirs:
    print(d)
    dbname = d.split("/")[-1]
    f = d + "/"+dbname + "_V004_iOSO_kall.wrp" 
    if not os.path.exists(f):
        f = f.replace("V004", "V003")
    #cmd = "nuSolve -t batch.js " + f + " " + out + " no"
    cmd = "nuSolve -t batch.js " + f + " " + out + " save"
    print("Running CMD=", cmd)
    os.system(cmd)
