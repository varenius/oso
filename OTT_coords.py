import glob

#fns = ['./Reports/19NOV19X0.SFF',]
fns = glob.glob("./Reports/*SFF")

# ONSALA60, ITRF2014, ref 2010, from http://itrf.ensg.ign.fr/ITRF_solutions/2014/doc/ITRF2014_VLBI.SSC.txt
ONSALA60 = {'X':3370605.8407, 'Y':711917.6739, 'Z':5349830.8703} # meters

def print_res(t, r):
    X = round(r['X'],4)
    Y = round(r['Y'],4)
    Z = round(r['Z'],4)
    print(t+ " {:.4f} {:.4f} {:.4f}".format(X, Y, Z))

def get_coords(rfile):
    rf = open(rfile)
    ONSA13NE = {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
    ONSA13SW = {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
    for line in rf:
        if ("ONSA13NE-ONSALA60" in line) and ("Comp" in line):
            ls = line.split()
            c = ls[2] # X, Y, or Z
            p = float(ls[4]) # value relative to ONSALA60, in mm.
            ONSA13NE[c]=ONSALA60[c]-p/1000.0
        if ("ONSALA60-ONSA13SW" in line) and ("Comp" in line):
            ls = line.split()
            c = ls[2] # X, Y, or Z
            p = float(ls[4]) # value relative to ONSALA60, in mm.
            ONSA13SW[c]=ONSALA60[c]+p/1000.0
    rf.close()
    print(rfile)
    print_res("ONSA13SW", ONSA13SW)
    print_res("ONSA13NE", ONSA13NE)

for f in fns:
    get_coords(f)
