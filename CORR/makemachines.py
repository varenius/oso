import glob, os

# This script will create one .machines and one.threads file for each .input
# file that exists in the current working directory. This is useful for setting
# up DiFX correlation job on a small flexbuff cluster.
# 
# The structure of the .machines files is like this:
# ---
# Machine controlling the job
# Machine feeding data stream 1
# Machine feeding data stream 2
# Computing machine 1
# Computing machine 2
# ...
# ---
# where the machines must be called a viable network ID, i.e. an IP-address
# or DNS name. if using 3 machines called "gyller", "skirner" and "oldbogar", 
# as DNS names where "gyller" act as head node, serving 2 datastreams, 
# and doing computation, and "skirner" and "oldbogar" are only doing i
# computation, then the machines file can look like
# ---
# gyller
# gyller
# gyller
# gyller
# skirner
# oldbogar
# ---

# The structure of the .threads file is like this:
# ---
# NUMBER OF CORES:    N
# Number of threads to run on Computing machine 1
# Number of threads to run on Computing machine 2
# ...
# ---
# where N is the number of machines (NOT the number of CPU cores, despite saying CORES).
# So, if using 3 machines with 10,10,16 processes respectively, where the order of the
# machine IDs are given as the last 3 lines in the .machines file, then we can have the
# example .threads file as
# ---
# NUMBER OF CORES:    3
# 10
# 10
# 16
# ---
# We can run each DiFX job with the same config, meaning we need identical copies of the 
# threads and machines file for each job. This script assumes you have edited the ex.machines
# and ex.threads, and will copy them to your working dir

ins = glob.glob("*.input")

scriptdir = os.path.dirname(os.path.realpath(__file__))

for i in ins:
    b = i.split(".")[0]
    os.system("cp {0}/ex.machines {1}.machines".format(scriptdir,b))
    os.system("cp {0}/ex.threads {1}.threads".format(scriptdir,b))
