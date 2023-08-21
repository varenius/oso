import glob, os

ins = glob.glob("*.input")

exp = ins[0].split(".")[0].split("_")[0]
nodata = {}

for line in open(exp+".nodata"):
    ls = line.split(":")
    job = ls[0].split()[-1]
    nodata[job] = ls[1].split()

for i in ins:
    b = i.split(".")[0]
    jobid = int(b.split("_")[-1])
    try:
        misants = nodata[str(jobid)]
    except KeyError :
        misants = []
    numstream= 4 - len(misants)
    # write machines file
    with open(b + ".machines","w") as f:
        f.write("gyller\n")
        for i in range(numstream):
            f.write("kare\n")
        f.write("oldbogar\n")
        f.write("hjuke\n")
    f.close()
    # Write threads file
    with open(b + ".threads","w") as f:
        f.write("NUMBER OF CORES:    2\n")
        f.write("16\n")
        f.write("32\n")
    f.close()
