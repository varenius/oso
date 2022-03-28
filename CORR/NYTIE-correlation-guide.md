# Guide to correlate and fringe-fit NY2080
Eskil Varenius, Onsala Space Observatory, 2022-03-28

# Table of contents
1. [Required software](#software)
2. [Mounting and indexing the data ](#mount)
    1. [Sub paragraph](#subparagraph1)
3. [Another paragraph](#paragraph2)

## Required software <a name="software"></a>
This guide assumes you have the following software installed, preferably the same or higher version numbers:
* difx (2.6.3 https://www.atnf.csiro.au/vlbi/dokuwiki/doku.php/difx/installation)
* HOPS (3.23 from https://www.haystack.mit.edu/haystack-observatory-postprocessing-system-hops/)
* nuSolve (0.7.4 from https://sourceforge.net/projects/nusolve/) 
* sked (2022-03-28 from https://ivscc.gsfc.nasa.gov/IVS_AC/sked_cat/)

## Mounting and indexing the data <a name="mount"></a>
To correlate we need VLBI raw data, usually recorded in VDIF (new) or m5b (old) format. If the data are recorded on a flexbuff, they are spread in multiple segments striped across many disks (VBS data format). To virtually assemble them so that we can read each file properly, we can use the "vbs_fs" command to mount the files to some folder on the machine. In this example, I pick the location "/mnt/vbsmnt" to mount my data. To do this, I first need to create the folder with `mkdir /mnt/vbsmnt`. Assuming this folder exists, I want to make sure to unmount any previously mounted data with `fusermount -u /mnt/vbsmnt`. Finally we mount all files matching "ny2080*" with the command `vbs_fs /mnt/vbsmnt/ -I "ny2080*"`.

Once the data are accessible, either directly or via the vbs_fs mounted file-system, we need to index the files to let DiFX know what data is available. If the data are in "m5b" format, e.g. antenna Ny, then we run the tool m5bsum which comes with difx like `m5bsum -s /mnt/vbsmnt/ny2080_ny* > ny.files`. This produces a file with paths to all datafiles and their respective start and end timestamps. Similarly, for VDIF, e.g. antenna Ns, we run `vsum -s /mnt/vbsmnt/ny2080_ns* > ns.files`. 

## Preparing the vex and v2d files  <a name="vex+v2d"></a>
The main control file used to tell DiFX what to do is called a .v2d file. The software also reads a .vex file. There is some partial overlap and choice where to put some settings, it can be either in v2d or vex. But both files are fundamentally required.

### Preparing the v2d file  <a name="v2d"></a>
Usually we start from a previous template v2d file and change the required fields. In this case, the final v2d will look like this:
```
vex = ny2080.vex 
antennas = Ns, Ny
singleScan = True
tweakIntTime = True
mjdStart = 2022y080d08h43m00s
#mjdStop = 2022y075d20h20m00s
SETUP geo 
{
  tInt = 0.8192 
  doPolar = False
  nChan = 64 
}
ANTENNA NS
{
  filelist = ns.files
  toneSelection = all
  phaseCalInt = 5
}
ANTENNA NY
{
  filelist = ny.files
  toneSelection = all
}
```
Here we made sure to change the `vex=` line to the current experiment vex file (see below), adjust any date fields (here used to skip first part which did not have good data), and possibly tInt and/or nChan for time and frequency resolution respectively of the output visibilities. Note that we are using the "ns.files" "ny.files" that we prepared above.

### Preparing the vex file  <a name="vex"></a>
The vex file will contain information about scan times, sources, clock corrections and Earth Orientation Parameters (EOPs). If you schedule with VieSched++ software, you may have a VEX file already. Here we assume you have skeduled with the sked software, which by default writes .skd files. However, sked can also output vex files. To convert an existing skd file to vex, we
1. Open the file in sked with `sked ../SKD_new/ny2080.skd`
2. At the prompt we use the command `VEC ny2080.vex` to save it to a vex file
3. quit the sked software

### Manually modify vex equipment setup
In theory, the vex file should be correct with all equipment and antenna settings. However, because of errors in the station catalogs, and in some cases limitations in the catalog and .skd formats, we need to manually edit the vex file. For S/X NYTIE observations, there is only one required change and this is to comment one line of code: `*    ref $TRACKS = Mk341_1f_2b-SX02:Ns;` where the `*` character indicates a commented line. If you want, you can optionally also change the correlator name to something sensible; in this case I set `target_correlator = OSO;`.


### Add clock information

For correlation we need information about the respective clocks for all stations involved. The "proper" way to do this is to use the tool "fmout.py" which can be found in https://github.com/whi-llc/fmout. However, long before I was aware of this tool, I wrote my own (less fancy) version at https://github.com/varenius/oso/blob/master/CORR/fs_log_rate.py. This second script has the minor advantage of writing not only a clock value (offset and rate) fitted from the Field-System log file, but it also adds the so called "peculiar offset" values for a few stations, and writes the results as a line which can be directly copied and pasted in the vex file. (The most recent peculiar offset values can be obtained from adjust.py from https://github.com/whi-llc/adjust and would have to be added manually to the fs_log_rate.py code. However, if nothing major happens to the RF setup, the offsets should be constant.)

To generate the desired clock information, we run the script once for each station; first for Ns:
```
$ python3 fs_log_rate.py -l ny2080ns.log 
Running with arguments: Namespace(etime=None, logfile=['ny2080ns.log'], outfile=None, stime=None)
----------------------
*RESULT IN VEX FORMAT:
*NOTE: Using peculiar offset 1.68 us from reference. Make sure this is correct!
*                  valid from           clock_early    clock_early_epoch        rate
def Ns;  clock_early = 2022y080d00h00m00s : 25.493 usec : 2022y080d00h00m00s : 0.232e-12; enddef;
*NOTE: You may want to adjust 'valid from' to before the exp start to cover all scans.
----------------------
*RESULT IN CORRELATOR REPORT FORMAT:
Station     fmout-gps      Used      rate     Comments
             [usec]       [usec]   [sec/sec]
Ns           23.81        25.49     0.232e-12 Reftime 2022y080d00h00m00s
```
and then for Ny
```
$ python3 fs_log_rate.py -l ny2080ny.log 
Running with arguments: Namespace(etime=None, logfile=['ny2080ny.log'], outfile=None, stime=None)
----------------------
*RESULT IN VEX FORMAT:
*NOTE: Using peculiar offset 2.308 us from reference. Make sure this is correct!
*                  valid from           clock_early    clock_early_epoch        rate
def Ny;  clock_early = 2022y080d00h00m00s : -86.804 usec : 2022y080d00h00m00s : -0.184e-12; enddef;
*NOTE: You may want to adjust 'valid from' to before the exp start to cover all scans.
----------------------
*RESULT IN CORRELATOR REPORT FORMAT:
Station     fmout-gps      Used      rate     Comments
             [usec]       [usec]   [sec/sec]
Ny          -89.11       -86.80    -0.184e-12 Reftime 2022y080d00h00m00s
```
This gives a fitted linear trend for the clock data from the FS log file, with the reference epoch given as
midnight on the day the observation started. Please note: It is good to save this output in full, 
as you may need it later. 

We now append the following lines to the vex file:
```
$CLOCK;
*                  valid from           clock_early    clock_early_epoch        rate
def Ns;  clock_early = 2022y080d00h00m00s : 25.493 usec : 2022y080d00h00m00s : 0.232e-12; enddef;
def Ny;  clock_early = 2022y080d00h00m00s : -86.804 usec : 2022y080d00h00m00s : -0.184e-12; enddef;
```

### Add Earth Orientation Parameters (EOPs)
By default, IVS experiments are 24 hours. Difx wants 2 days before and 2 days after i.e. 5 days in total of EOP values in the correct format. This can be obtained by running the tool "geteop.pl" which comes with difx. Because of recent security restrictions for anonymous downloads, we need to give an email address as an environment variable when running the script. To do so and download 5 days of data starting 2 days before: `EMAIL_ADDR=your.email@example.com geteop.pl 2022-078 5` where "your.email..." should be your valid email. This will produce a file called EOP.txt which can be copied verbatim and appended as a section to the VEX file.


vex2difx -v -v -v -d *.v2d
calcif2 -f *.calc (if failure, run startCalcServer)

python3 /home/oper/eskil/eskil.oso.git/CORR/makemachines.py 

startdifx -n -f -v *.input

Complains about
"[ -1] WARNING Baseline 0 frequency 0 points at two different frequencies that are apparently identical - this is not wrong, but very strange.  Check the input file
"
But no problem.
Check that you get progress, e.g. by running "errormon2"



difx2mark4 -v  -s ../station_code_file.txt  *.difx

cp cf_ny2075 cf_ny2080

Remove "pc_phases" line

FIND PC_PHASES using " fourfit -pt -c cf_ny2080 -b wN -m 1 1234/BRIGHT_SCAN"
Select "080-1307" which is OJ287
Then "fourfit -c cf_ny2080 -b wN 1234/*"
