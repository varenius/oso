#Simple script to do an az/el plot of a source for a given location using the skyfield API
from skyfield.api import Star, Topos, load
from matplotlib import pyplot as plt

# Load basic data
planets = load('de421.bsp')
ts = load.timescale()

# Define targets
targets = {}
targets['cyga'] = Star(ra_hours=(19, 59, 28), dec_degrees=(40,44,2)) # Cygnus A
targets['casa'] = Star(ra_hours=(23, 23, 24), dec_degrees=(58,48.9,0)) # Cas A

# Define location of observer
o8 = planets['earth'] + Topos("57.393118 N", "11.917756 E") # Onsala 25m antenna, approximate
# Define time(s) to observe
times = ts.utc(2019, 9, 20,range(0,24)) # 24h from start time

# Create figure objects
azfig, azax = plt.subplots()
altfig, altax = plt.subplots()

# Make plot
for target in targets:
    astro = o8.at(times).observe(targets[target])
    app = astro.apparent()
    
    alt, az, distance = app.altaz()
    azax.plot_date(times.utc_datetime(), az.degrees, label=target)
    azax.set_xlabel("Datetime")
    azax.set_ylabel("Azimuth")
    azax.set_title("At Onsala 25m")
    azax.legend()

    altax.plot_date(times.utc_datetime(), alt.degrees, label=target)
    altax.set_xlabel("Datetime")
    altax.set_ylabel("Altitude")
    altax.set_title("At Onsala 25m")
    altax.legend()

plt.show()
