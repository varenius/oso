import sys
import glob
import os

# Make a file with bash commands to "vmux" vdif data from 8ch8thread to 64ch1thread
# for Haystack correleator. Note that each line ends with && to only continue next command
# if the first one finished OK. However, the last line must not have && when running.
# So you need to edit the file to ensure the last command does not end with &&, else you will get error.

vbsdir = "/mnt/vbsmnt/"
if not len(sys.argv)==3:
    print("USAGE: script.py exp outfile, for example: script.py vt9259 vmux.vt9259.sh")
    print("NOTE: select antenna by e.g.: script.py vt9259_oe vmux.vt9259.oe.sh")
    sys.exit(1)

exp = sys.argv[1]
ofname = sys.argv[2]

vdifs = glob.glob(vbsdir + exp + "*")

of = open(ofname,"w")
for vin in vdifs:
    vout = os.path.basename(vin) + "_all"
    vmuxcmd = "vmux -v {0} 8224 15625 0,1,2,3,4,5,6,7 {1} &&\n".format(vin, vout)
    of.write(vmuxcmd)
of.close()
