#!/usr/local/bin/python3.9
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
import time
import os
from skyfield.api import Topos, load
import warnings
warnings.filterwarnings("ignore")

# The list of links with TLE data
#GPS https://celestrak.com/NORAD/elements/gps-ops.txt
#GALILEO https://celestrak.com/NORAD/elements/galileo.txt
#GLONASS https://celestrak.com/NORAD/elements/glo-ops.txt
#BEIDOU https://celestrak.com/NORAD/elements/beidou.txt
#stations 'http://celestrak.com/NORAD/elements/stations.txt'

# Notes:
#https://rhodesmill.org/skyfield/earth-satellites.html

class SatLive:
    def __init__(self):
        self.gps = load.tle_file("https://celestrak.com/NORAD/elements/gps-ops.txt")
        self.galileo = load.tle_file("https://celestrak.com/NORAD/elements/galileo.txt")
        self.glonass = load.tle_file("https://celestrak.com/NORAD/elements/glo-ops.txt")
        self.beidou = load.tle_file("https://celestrak.com/NORAD/elements/beidou.txt")
        self.allsat = self.gps+self.galileo+self.glonass+self.beidou
        print('Loaded', len(self.allsat), 'satellites')
        # create dict where we can fetch a satellite using its name as key
        self.sats_by_name = {sat.name: sat for sat in self.allsat}
        # Define observatory for az,el calculation
        self.obs = Topos('57.393109 N', '11.917798 E') # OSO25m
        # Define timerange, https://rhodesmill.org/skyfield/time.html
        self.ts = load.timescale()
        self.tgps = False
        self.tgalileo = False
        self.tglonass = False
        self.tbeidou = False
        #self.sat2plot = self.gps+self.galileo
        self.sat2plot = []
        # Plot the data, awaiting key-press events
        self.plot()

    def track(self,targ):
        try:
            while True:
                # Calculate difference, used to get alt/az further down
                difference = targ - self.obs
                topocentric = difference.at(self.ts.now())
                alt, az, distance = topocentric.altaz()
                ra, dec, distance = topocentric.radec()
                a_r = ra.hms()
                b_r = dec.dms()
                a = [np.abs(i) for i in a_r]
                b = [np.abs(i) for i in b_r]
                asign = ""
                bsign = ""
                if a_r[0] <0:
                    asign = "-"
                if b_r[0] <0:
                    bsign = "-"
                sname = targ.name.split()[0]+"_"+targ.name.split()[-1][1:-1]
                cmd = "source={},{}{:02d}{:02d}{:05.2f},{}{:02d}{:02d}{:05.2f},2000.0".format(sname,asign, int(a[0]), int(a[1]), a[2], bsign, int(b[0]), int(b[1]), b[2])
                print("Sending command to FS: "+ cmd)
                os.system("inject_snap "+cmd)
                print("... then waiting 5 seconds before recalculating position.")
                print("Press CTRL-C to abort tracking and return to plot.")
                time.sleep(5)
        except KeyboardInterrupt:
            self.plot()

    def togglesat(self):
        sl = []
        if self.tgps:
            sl = sl+self.gps
        if self.tgalileo:
            sl = sl+self.galileo
        if self.tbeidou:
            sl = sl+self.beidou
        if self.tglonass:
            sl = sl+self.glonass
        self.sat2plot = sl
    
    def on_click(self,event):
        caz = event.xdata*180/np.pi % 360
        calt = event.ydata % 90
        print("Clicked at (az,alt)=({0},{1})".format(caz, calt))
        if len(self.sat2plot)>0:
            self.findSat(caz, calt)
        else:
            print("Nothing shown... returning to plot.")
            plt.close("all")
            self.plot()

    def findSat(self,caz,calt):
        t = self.ts.now()
        dist = 9999
        targ = self.sat2plot[0]
        for sat in self.sat2plot:
            # Calculate difference, used to get alt/az further down
            difference = sat - self.obs
            topocentric = difference.at(t)
            alt, az, distance = topocentric.altaz()
            sdist = np.sqrt((float(alt.degrees)-calt)**2 + (float(az.degrees)-caz)**2)
            #print(sat.name, float(alt.degrees)-calt, float(az.degrees)-caz, sdist)
            if sdist < dist:
                targ = sat
                dist = sdist
        plt.close("all")
        print("Closest sat = ", targ.name)
        if input("Track {} every 5 seconds? [Y/N]".format(targ.name)).lower() == "y":
            self.track(targ)
        else:
            self.plot()
    
    def on_press(self,event):
        sys.stdout.flush()
        plt.close("all")
        if event.key == 'r':
            self.plot()
        elif event.key in ['a', 'b','c','d']:
            if event.key=="a":
                self.tgps = not self.tgps
            elif event.key=="b":
                self.tbeidou = not self.tbeidou
            elif event.key=="c":
                self.tgalileo = not self.tgalileo
            elif event.key=="d":
                self.tglonass = not self.tglonass
            self.togglesat()
            self.plot()
        elif event.key == 'q':
            sys.exit(0)
        else:
            pass
    
    def plot(self):
        minalt=20 # degrees
        fig = plt.figure(figsize=(10,10))
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        fig.canvas.mpl_connect('button_press_event', self.on_click)
        ax = fig.add_subplot(1,1,1,projection='polar')
        ax.set_theta_zero_location("N")  # theta=0 at the top
        ax.set_theta_direction(-1)  # theta increasing clockwise
        ax.set_rlim(bottom=90, top=minalt)
        #ax.set_rlim(bottom=minalt, top=80)
        t = self.ts.now()
        for sat in self.sat2plot:
            # Calculate difference, used to get alt/az further down
            difference = sat - self.obs
            topocentric = difference.at(t)
            alt, az, distance = topocentric.altaz()
            if alt.degrees> minalt:
                ax.scatter(az.radians, alt.degrees) # Azimuth in radians!!!
                ax.annotate(sat.name, (az.radians, alt.degrees))
        ax.set_title("Az/el plot OSO 25m made " + t.utc_strftime() + "\n Press r to replot, click close to satellite to track it. \n Toggle constallations with a=GPS, b=BEIDOU, c=GALILEO, d=GLONASS.\nPress q to quit.")
        plt.draw()
        plt.pause(0.001)
        move_figure(fig, 200, 200)
        plt.show()

def move_figure(f, x, y):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)

if __name__ == '__main__':
    satlive = SatLive()    
