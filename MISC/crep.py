import numpy as np
import sys

class CorrelatorReport:
    def __init__(self, a, v, s):
        self.readStations(s)
        self.readAlist(a)
        self.readVEX(v)

    def readStations(self,f):
        self.s2ts1={}
        self.s1ts2={}
        for l in open (f):
            if not l.startswith("*"):
                [s1,s2]=l.split()
                # Lookup dict for 2 letter code --> 1 letter code
                self.s2ts1[s2.strip()]=s1.strip()
                # Lookup dict for 1 letter code --> 2 letter code
                self.s1ts2[s1.strip()]=s2.strip()

    def readAlist(self,f):
        d = []
        for l in open (f):
            if not l.startswith("*"):
                d.append(l.split())
        self.alist = np.array(d)

    def readVEX(self,f):
        d = {}
        st_in_scan = []
        for l in open (f):
            if "station =" in l:
                st = l.split(":")[0].split("=")[1].strip()
                st_in_scan.append(self.s2ts1[st])
            if "endscan;" in l:
                nstat = len(st_in_scan)
                for i in range(nstat):
                    for j in range(i+1,nstat):
                        bl = st_in_scan[i]+st_in_scan[j]
                        if not bl in d.keys():
                            d[bl]=0
                        d[bl]+=1 # Increment scan counter by one
                st_in_scan = []
        self.nscans = d

    def getSummary(self):
        # Correlated scans
        corr_qcodes = self.alist[:,15]
        corr_nscan = float(len(corr_qcodes))
        corr_5t9 = [q for q in corr_qcodes if q in ['5','6','7','8','9']]
        corr_0 = [q for q in corr_qcodes if q in ['0']]
        # Add together both 1 char codes like "3" and 2 char codes like "5G"
        corr_4t1_AH_N = [q for q in corr_qcodes if q in ['4','3','2','1','N','A','B','C','D','E','F','G','H']] + [q for q in corr_qcodes if (len(q)==2) and (q[1] in ['4','3','2','1','N','A','B','C','D','E','F','G','H'])]
        # All scans, also non-correlated
        tot_nscan = sum([self.nscans[i] for i in self.nscans.keys()])
        # Prepare summary text
        h = "+SUMMARY\n"
        h += " Qcode  % of Total   % of Correlated\n" 
        h += "             scans        scans\n" 
        msg =" 5-9           -          {:5.2f}%\n".format(100.0*len(corr_5t9)/corr_nscan)
        msg +=" 0             -          {:5.2f}%\n".format(100.0*len(corr_0)/corr_nscan)
        msg +=" 4-1,A-H,N     -          {:5.2f}%\n".format(100.0*len(corr_4t1_AH_N)/corr_nscan)
        msg +=" REMOVED       -           -\n".format()
        # Ignore "total scans" since this is not well defined. Do we mean number of scans/number of baseline products, scheduled/correlated?
        #msg =" 5-9           {:2d}%            {:2d}%\n".format(int(round(100.0*len(corr_5t9)/tot_nscan)), int(round(100.0*len(corr_5t9)/corr_nscan)))
        #msg +=" 0             {:2d}%            {:2d}%\n".format(int(round(100.0*len(corr_0)/tot_nscan)), int(round(100.0*len(corr_0)/corr_nscan)))
        #msg +=" 4-1,A-H,N     {:2d}%            {:2d}%\n".format(int(round(100.0*len(corr_4t1_AH_N)/tot_nscan)), int(round(100.0*len(corr_4t1_AH_N)/corr_nscan)))
        #msg +=" REMOVED       {:2d}%             -\n".format(int(round(100.0*(1-corr_nscan/tot_nscan))))
        print(h + msg)

    def getQcodes(self):
        #codes = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","N","-"]
        codes = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","N"]
        # Correlated scans
        corr_bs_q = self.alist[:,14:16]
        bs = np.unique(corr_bs_q[:,0])
        qtab = []
        for b in bs:
            # Get all Qcodes for this baseline
            vs = corr_bs_q[:,1][corr_bs_q[:,0]==b]
            vals = []
            for v in vs:
                if len(v)==1:
                    vals.append(v)
                elif len(v)==2:
                # Trim 2 letter codes, e.g. 5G, to one letter, i.e. "G"
                    vals.append(v[1])
            vals = np.array(vals)
            qc = []
            for c in codes:
                qc.append((len(vals[vals==c])))
            # Get total for this bl. Depends on how to interpret the memo.
            ### ALTERNATIVE 1
            qc.append(sum(qc)) #Total scans with existing codes for this baseline
            ### ALTERNATIVE 2
            # If instead we want the total scans scheduled (not correlated) then we do
            #if not bs in self.nscans.keys():
            #    totkey = bs[::-1]
            #else:
            #    totkey= bs
            #qc.append(self.nscans[totkey]) #Total scans scheduled
            ###
            qtab.append(qc)
        qtab.append(np.sum(np.array(qtab),axis=0))
        qtab = np.array(qtab).astype(str)
        cws = [len(max(qtab[:,i], key=len)) for i in range(len(codes)+1)] # Include Total column
        h = "+QCODES"
        print(h)
        h = "Qcod"
        for i,a in enumerate(codes):
            h+= a.rjust(cws[i]+1)
        h+= "Tot".rjust(cws[-1]+1)
        sep = "-"*len(h.strip())
        print(h)
        print(sep)
        for k,b in enumerate(bs):
            m = b + ":X"
            for i,c in enumerate(qtab[k,:]):
                m+= c.rjust(cws[i]+1)
            print(m)
        print(sep)
        f= "Tot "
        for l,c in enumerate(qtab[-1,:]):
            f+= c.rjust(cws[l]+1)
        f+= "\n"
        print(f)
        l = "Legend:\n"
        l += "QC = 0   Fringes not detected.\n"
        l += "   = 1-9 Fringes detected, no error condition. Higher #, better quality.\n"
        l += "   = B   Interpolation error in fourfit.\n"
        l += "   = D   No data in one or more frequency channels.\n"
        l += "   = E   Maximum fringe amplitude at edge of SBD, MBD, or rate window.\n"
        l += "   = F   Fork problem in processing.\n"
        l += "   = G   Fringe amp in a channel is <.5 times mean amp (only if SNR>20).\n"
        l += "   = H   Low Phase-cal amplitude in one or more channels.\n"
        l += "   = N   No valid correlator data.\n"
        #l += "   = -   Scans in original schedule file for which correlation was not\n"
        #l += "         attempted, usually because of known station problems.\n"
        #l += "   = Tot Total number of scans in schedule.\n" 
        l += "   = Tot Total number of Qcodes in row/column.\n" 
        print(l)

    def getSNR(self):
        print("")

cr = CorrelatorReport(sys.argv[1], sys.argv[2], sys.argv[3]) # args= alist, vex
cr.getSummary()
cr.getQcodes()
