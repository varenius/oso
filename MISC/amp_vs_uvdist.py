import astropy.io.fits as fits
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.stats import binned_statistic
from scipy.constants import c
from scipy.optimize import curve_fit

ndist= 10 # Number of ranges for sked flux catalog line
    
# Open file given as first argument to script
infile = sys.argv[1]
d = fits.open(infile)

# Read FITS Metadata
target = d[0].header["OBJECT"]
freq = d[2].header["FREQ"]
dateobs = d[0].header["DATE-OBS"]
nif = d[1].header["NO_IF"]

# Calculate UV distances from U and V coordinates
us = d[0].data['UU'] # in light-seconds, according to http://parac.eu/AIPSMEM117.pdf Table 4
vs = d[0].data['VV'] # in light-seconds, according to http://parac.eu/AIPSMEM117.pdf Table 4
lam = c/freq # Observing wavelength
ls_to_m = 1.0*c# Convert from light-seconds to meters
m_to_mlambda = 1.0/(1e6*lam)# Convert from meters to Mlambda
dist = np.sqrt(us**2+vs**2)*ls_to_m*m_to_mlambda # Now distances are in Mega-wavelength

# Calculate visibility amplitudes from real, imaginary data
# First get UV data (not the Us and Vs, but the complex numbers (real, imag) for each UV point)
uvdata = d[0].data['DATA']
# Read all amplitudes, and add the respective distance for each (ignoring the baseline length differences between IFs)
amps = []
dists = []
sigmas = []
for (i,d) in enumerate(uvdata):
    for m in range(nif):
        # Extract values from nested arrays
        # Assume nstokes, nfreq = 1 for now
        [real, imag, weight] = d[0][0][m].flatten()
        # Negative weights means data should be excluded
        if weight>0:
            # Calculate amplitude from real, imaginary
            amps.append(np.sqrt(real**2+imag**2))
            dists.append(dist[i])
            sigmas.append(1.0/np.sqrt(weight))

# Convert from python lists to numpy arrays to allow nice numpy features
amps = np.array(amps)
dists = np.array(dists)
sigmas = np.array(sigmas)

# Bin data to reduce scatter
nbins = 50 # Define number of bins to use
# Bin amplitude values based on distances
avg_amps, edge_amps, bin_amps = binned_statistic(dists, amps, statistic='mean', bins=nbins)
# Bin distances, based on themselves
avg_dist, edge_dist, bin_dist = binned_statistic(dists, dists, statistic='mean', bins=nbins)

# Define 1D-gaussian
def gauss(x,a,sigma):
    x0=0 # Fixed, we assume everything is centered
    return a*np.exp(-(x-x0)**2/(2*sigma**2))
# Fit model to data
popt,pcov = curve_fit(gauss,dists,amps,p0=[0.5, 50], sigma=sigmas)
# Determine UV-ranges for plotting
if lam>0.1:
    band = "S"
    dmax = 100 # Mlambda
else:
    band = "X"
    dmax = 340 # Mlambda

# Render model at fixed UV-range
mdists = np.linspace(0,dmax,100)
mamps = gauss(mdists, *popt)

# Format string for SKED source catalog
# First prepare start of string
skedl = "{0} {1} {2} {3}".format(target, band, "B", 0.0)
# Extract model flux densities for sked catalog at specific points
catpoints = np.linspace(0,dmax,ndist)[1:] # Ndist points from 0 to dmax in Mlambda, omitting 0.0 as it's already covered
catflux = gauss(catpoints, *popt)
# Now add the flux for the distances (in km) to the string
for i in range(len(catpoints)):
    pflux = catflux[i]
    pdist =  catpoints[i] * 1e-3 / m_to_mlambda # Convert from Mlambda to kilometers
    skedl += " {0:.2f} {1:.1f}".format(pflux, pdist)
print("SKEDFLUXCAT: " + skedl)

# Create figure and axis object for plotting
fig, ax = plt.subplots(1)
# Plot result as correlated amplitude vs UV distance
ax.errorbar(avg_dist, avg_amps, fmt="o", label="binned data")
# Plot fitted model
ax.plot(mdists, mamps, label='Gaussian fit')
# Plot SKED cat values
ax.errorbar(catpoints, catflux, fmt= "*", label="For SKED")
ax.legend()
# Set lables and limits
ax.set_ylabel("Correlated amplitude [Jy]")
ax.set_xlabel("Projected baseline length [Mlambda]")
ax.set_ylim(bottom=0.0)
# Set title
fig.suptitle(dateobs + "    " + target + "    " + "Freq: {0} GHz".format(freq/1.0e9))
# Save figure as PDF file
fig.savefig(infile + ".pdf", dpi=300)

# Show plot on screen
plt.show()
