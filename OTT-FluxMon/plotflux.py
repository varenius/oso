#!/usr/bin/python3
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import glob
# Use TEX rendering for nice fonts
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})
# for Palatino and other serif fonts use:
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"],
})
plt.rcParams.update({'font.size': 18})

inpath = sys.argv[1]

if inpath.endswith(".flux"):
    infs = [inpath,]
else:
    infs = glob.glob(inpath+"*.flux")

for inf in infs:
    data = np.loadtxt(inf)
    source = os.path.basename(inf).split(".flux")[0]
    if len(data)>0:
        f, ax = plt.subplots(figsize = (7,7))
        
        ax.plot(data[:,1]*1e-9, data[:,2],"ko", label="Stokes I")
        ax.set_xlabel('Frequency [GHz]')
        ax.set_xscale("log")
        #ax.set_yscale("log")
        xticks = ([3,4,5,6,7,8,9,10,11])
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticks)
        ax.set_ylabel('Flux density [Jy]')
        #ax.set_ylim([0.1,15])
        ax.set_title(source)
        
        # define points to plot Perley-Butler models
        x=np.linspace(3,11.5, 500) # in GHz
        if "3C286" in inf:
            def spec(x):
                """Spectrum for 3c286, Perley and Butler (2017) """
                return 10**(1.2481-0.4507*np.log10(x)-0.1798*(np.log10(x))**2+0.0357*(np.log10(x))**3)
        elif "3C147" in inf:
            def spec(x):
                """Spectrum for 3c147, Perley and Butler (2017) """
                return 10**(1.4516-0.6961*np.log10(x)-0.2007*(np.log10(x))**2+0.0640*(np.log10(x))**3-0.0464*(np.log10(x))**4+0.0289*(np.log10(x))**5)
        elif "3C295" in inf:
            def spec(x):
                """Spectrum for 3c295, Perley and Butler (2017) """
                return 10**(1.4701-0.7658*np.log10(x)-0.2780*(np.log10(x))**2+0.0347*(np.log10(x))**3-0.0399*(np.log10(x))**4)
        if ("3C286" in inf) or ("3C147" in inf) or ("3C295" in inf):
            ax.plot(x, spec(x), label="Perley-Butler (2017)")
        
        ax.legend()
        f.savefig(inf+".pdf", dpi=300, bbox_inches='tight' )
        #plt.show()
