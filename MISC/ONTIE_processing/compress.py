# Script to compress vgosDbs to tar gz files with the right name
import glob
import os

for path in glob.glob("20*/*"):
    fn = os.path.basename(path)
    d = os.path.dirname(path)
    #print("tar -C " + d + " -cvzf "+fn+".tgz "+fn)
    os.system("tar -C " + d + " -cvzf "+fn+".tgz "+fn)

os.system("mv *tgz IVS-upload")
