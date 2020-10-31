#list VBS-experiments on disk
import os
os.system("vbs_ls -lrth > tmp.dat")
infile = "tmp.dat"
exps = []
for line in open(infile):
    if line.startswith("d"):
        sp = line.split()[7].split("_")
        if len(sp)==3:
            exp=sp[0] + "_" + sp[1]  # Exp and antenna
        else:
            exp=sp
        if not exp in exps:
            exps.append(exp)
print("Found these VBS-experiments on disk:")
for exp in exps:
    print(exp)
