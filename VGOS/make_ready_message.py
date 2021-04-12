import sys

logfile = sys.argv[1]

lines = []
for line in open(logfile):
    lines.append(line)

def get_lines(log,pattern,nlines):
    revlog = list(reversed(log))
    ans = []
    # Loop through logfile backwards to find the latest entry
    for i,d in enumerate(revlog):
        if pattern in d:
            for n in range(0,nlines):
                ans.append(revlog[i-n])
            break
    return ans

def print_lines(ls):
    for l in ls:
        print str(l),

print
print "READY MESSAGE DATA FROM LOGFILE ", logfile
print

print "DBBC3 timing:"
time = get_lines(lines, "#dbbcn#dbbc3/time/",25)
print_lines(time)
print 

print "Pointing:"
point = get_lines(lines, "#fivpt#xoffset",1)
print_lines(point)
print

print "CDMS:"
cdms = get_lines(lines, "/CDMS/",1)
print_lines(cdms)
print 

print "Weather:"
wx = get_lines(lines, "/wx/",1)
print_lines(wx)
print 

print "SEFD:"
header = get_lines(lines, "Center   Comp   Tsys  SEFD ",1)
print_lines(header)
sefda = get_lines(lines, "l   3432.40",1)
print_lines(sefda)
sefdb = get_lines(lines, "r   3432.40",1)
print_lines(sefdb)
sefdc = get_lines(lines, "l   5672.40",1)
print_lines(sefdc)
sefdd = get_lines(lines, "r   5672.40",1)
print_lines(sefdd)
sefde = get_lines(lines, "l   6824.40",1)
print_lines(sefde)
sefdf = get_lines(lines, "r   6824.40",1)
print_lines(sefdf)
sefdg = get_lines(lines, "l  10664.40",1)
print_lines(sefdg)
sefdh = get_lines(lines, "r  10664.40",1)
print_lines(sefdh)
print 

print "First source:"
wx = get_lines(lines, "/source/",1)
print_lines(wx)
print 
