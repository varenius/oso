import sys

inf = sys.argv[1]

# Make summary of the hours observed for each baseline (one or more antennas)
# Will ignore lines with antenna code surrounded by ~~ indicating cancelled
summary = {}
for line in open(inf):
    ls = line.split("|")
    tels = ""
    if ls[4].strip()=="On":
        tels += "On"
    if ls[5].strip()=="Oe":
        tels += "Oe"
    if ls[6].strip()=="Ow":
        tels += "Ow"
    if not tels in summary.keys():
        summary[tels] = 0.0
    if not tels == "":
        summary[tels]+=float(ls[2])
# Print the number of hours per baseline
print(summary)
