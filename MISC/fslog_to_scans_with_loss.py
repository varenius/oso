import sys

inf = sys.argv[1]
losslist = []
postob = False
for l in open(inf):
    if "scan_name=" in l:
        ls = l.split(",")
        sname = ls[0].split("=")[-1]
        postob = False

    if "postob" in l:
        postob = True
    if postob and ": loss : " in l:
        loss = l.split(":")[-5].split()[-1].strip("(").strip(")")
        if not "0.00%" in loss:
            losslist.append(sname + " (" + loss + ")")

print(",".join(losslist))
print(len(losslist))
