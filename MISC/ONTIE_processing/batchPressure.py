import glob
import os

fns = glob.glob("RAW/*/*/k*.log")
print fns

for fn in fns:
    inf = fn
    outf = fn[4:]
    cmd = "python updateLogPressureData.py -i " + inf + " -o " + outf
    print "Excecuting CMD: " + cmd
    os.system(cmd)
