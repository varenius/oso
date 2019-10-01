#list VBS-experiments on disk
import os
os.system("vbs_ls -lrth > tmp.dat")
infile = "tmp.dat"
exps = []
for line in open(infile):
    if line.startswith("d"):
        exp=line.split()[7].split("_")[0]
        if not exp in exps:
            exps.append(exp)
print("Found these VBS-experiments on disk:")
for exp in exps:
    print(exp)
