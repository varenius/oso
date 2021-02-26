import sys
import os

vmuxfile = sys.argv[1]

def get_next_vmcmd(vmuxfile):
    vmcmd = ""
    for line in open(vmuxfile):
        if not line.startswith("#"):
            vmcmd = line
            break
    print("Got next vmcmd: " + vmcmd)
    return vmcmd

def vmux_and_transfer(vmcmd):
    vmfile = vmcmd.split()[6]
    exp = vmfile[0:9]
    cwd = os.getcwd()
    m5cmd = "m5copy file://:2621"+cwd+"/"+vmfile+ " file://192.52.62.236:2650/mnt/raid4/data/"+exp+"/ -udt -p 2652 --resume"
    if os.path.exists(vmfile):
        #File already on disk, transfer existing file (assuming it's complete)
        cmd = m5cmd
    else:
        #No file on disk, so vmux and transfer
        cmd = vmcmd + " " + m5cmd
    # Extre m5copy to ensure we got all data transferred
    cmd = cmd + " && " + m5cmd  
    print("Running " + cmd)
    return os.system(cmd)

def comment_vmcmd(vmuxfile, vmcmd):
    lines = []
    for line in open(vmuxfile):
        lines.append(line)
    with open(vmuxfile,"w") as outfile:
        for line in lines:
            if vmcmd in line:
                outfile.write("#" + line)
                print("Commented line "+line)
            else:
                outfile.write(line)

def remove_vmfile(vmcmd):
    vmfile = vmcmd.split()[6]
    os.system("rm "+vmfile)
try:
    while True:
        vmcmd = get_next_vmcmd(vmuxfile)
        if vmcmd == "":
            break
        res = vmux_and_transfer(vmcmd)
        if res==0:
            comment_vmcmd(vmuxfile, vmcmd)
            remove_vmfile(vmcmd)
        else:
            print("Problem with vmcmd" + vmcmd)
            sys.exit(1)
except KeyboardInterrupt:
    print('interrupted!')

