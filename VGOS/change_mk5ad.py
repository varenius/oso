#!/usr/bin/env python 
import sys

inf = "/usr2/control/mk5ad.ctl"
dest = sys.argv[1].strip().lower() # gyller, skirner, kare

# First make sure all lines are commented out:
lines = []
for l in open(inf):
    if not l.startswith("*"):
        l = "*"+l
    lines.append(l)

# Then find a line containing the desired destination name
# The next line (i+1) will be the one to uncomment
# For example, we find 
#* gyller
#*    129.16.208.73 32626 500
# and we change to 
#* gyller
#    129.16.208.73 32626 500
for i,l in enumerate(lines):
    if dest in l:
        lines[i+1] = lines[i+1].strip("*")
        break

# Write modified lines to file
of = open(inf,"w")
for l in lines:
    of.write(l)
of.close()
