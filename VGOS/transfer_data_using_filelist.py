import sys
import os

filelist = sys.argv[1]

def get_next_path(filelist):
    path = ""
    for line in open(filelist):
        if not line.startswith("#"):
            path = line.split()[-1]
            break
    print("Got next path: " + path)
    return path

def transfer(path):
    m5cmd = "m5copy vbs://:2621/"+path+ " file://159.226.233.197:2620/vgos/vg02/VO1047/Oe/ -udt -p 2681 --resume"
    # once more, to ensure resume finished
    m5cmd = m5cmd + " && " + m5cmd
    print("Running " + m5cmd)
    return os.system(m5cmd)

def comment_path(filelist, path):
    lines = []
    for line in open(filelist):
        lines.append(line)
    with open(filelist,"w") as outfile:
        for line in lines:
            if path in line:
                outfile.write("#" + line)
                print("Commented line "+line)
            else:
                outfile.write(line)
try:
    while True:
        path = get_next_path(filelist)
        if path == "":
            break
        res = transfer(path)
        if res==0:
            comment_path(filelist, path)
        else:
            print("Problem with path " + path + ". Trying again...")
except KeyboardInterrupt:
    print('interrupted!')
    sys.exit(1)

