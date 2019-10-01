import sys
logfile = sys.argv[1]

for line in open(logfile):
    if ("evlbi?" in line) and (not "loss : 0" in line):
        print(line)
