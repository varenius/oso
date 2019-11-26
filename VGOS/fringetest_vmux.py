import sys, os

datafile = sys.argv[1]
outdir = sys.argv[2]
fn = datafile.split("/")[-1]

cmds = []
cmds.append("vmux -v " + datafile + " 8224 15625 0,1 " + outdir + "/" + fn + "_band-A")
cmds.append("vmux -v " + datafile + " 8224 15625 2,3 " + outdir + "/" + fn + "_band-B")
cmds.append("vmux -v " + datafile + " 8224 15625 4,5 " + outdir + "/" + fn + "_band-C")
cmds.append("vmux -v " + datafile + " 8224 15625 6,7 " + outdir + "/" + fn + "_band-D")

print cmds

ans = raw_input("Press y to run the above commands!")

if ans == "y":
    for cmd in cmds:
        os.system(cmd)
