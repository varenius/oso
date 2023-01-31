# Guide to correlate and fringe-fit NY2080
Eskil Varenius, Onsala Space Observatory

## Table of contents
- [Introduction](#introduction)
  * [Required software](#required-software)
  * [Mounting and indexing the data](#mounting-and-indexing-the-data)
  * [Preparing the vex and v2d files](#preparing-the-vex-and-v2d-files)
    + [Preparing the v2d file](#preparing-the-v2d-file)
    + [Preparing the vex file](#preparing-the-vex-file)
    + [Manually modify vex equipment setup](#manually-modify-vex-equipment-setup)
    + [Add clock information](#add-clock-information)
    + [Add Earth Orientation Parameters](#add-earth-orientation-parameters)
  * [Prepare the input files needed for difx](#prepare-the-input-files-needed-for-difx)
- [Running DiFX](#running-difx)
  * [Convert the difx output to MK4-format](#convert-the-difx-output-to-mk4-format)
- [Fringe-fitting](#fringe-fitting)
  * [Determine pc-phases using a bright scan](#determine-pc-phases-using-a-bright-scan)
  * [Running the actual fringe-fitting](#running-the-actual-fringe-fitting)
  * [Creating a correlator report](#creating-a-correlator-report)
- [Creating a vgosDb](#creating-a-vgosdb)
  * [Appending Calc information](#appending-calc-information)
  * [Appending FS-log information](#appending-fs-log-information)
- [Creating a version 4 wrapper with editing and ambiguity resolution using nuSolve](#creating-a-version-4-wrapper-with-editing-and-ambiguity-resolution-using-nusolve)
# Introduction
This is a guide to correlate and post-process data from experiment ny2080. The output will be a vgosDb database which can be analysed by your favourite VLBI analysis software package. I assume you have the recorded VDIF/MARK5B data and the VLBI Field-System (FS) log files. In addition, you need the following:

## Required software 
This guide assumes you have the following software installed, preferably the same or higher version numbers:
* difx (2.6.3 https://www.atnf.csiro.au/vlbi/dokuwiki/doku.php/difx/installation)
* HOPS (3.23 from https://www.haystack.mit.edu/haystack-observatory-postprocessing-system-hops/)
* nuSolve (0.7.4 from https://sourceforge.net/projects/nusolve/) 
* sked (2022-03-28 from https://ivscc.gsfc.nasa.gov/IVS_AC/sked_cat/)

## Mounting and indexing the data
To correlate we need VLBI raw data, usually recorded in VDIF (new) or m5b (old) format. If the data are recorded on a flexbuff, they are spread in multiple segments striped across many disks (VBS data format). To virtually assemble them so that we can read each file properly, we can use the "vbs_fs" command to mount the files to some folder on the machine. In this example, I pick the location "/mnt/vbsmnt" to mount my data. To do this, I first need to create the folder with `mkdir /mnt/vbsmnt`. Assuming this folder exists, I want to make sure to unmount any previously mounted data with `fusermount -u /mnt/vbsmnt`. Finally we mount all files matching "ny2080*" with the command `vbs_fs /mnt/vbsmnt/ -I "ny2080*"`.

Once the data are accessible, either directly or via the vbs_fs mounted file-system, we need to index the files to let DiFX know what data is available. If the data are in "m5b" format, e.g. antenna Ny, then we run the tool m5bsum which comes with difx like `m5bsum -s /mnt/vbsmnt/ny2080_ny* > ny.files`. This produces a file with paths to all datafiles and their respective start and end timestamps. Similarly, for VDIF, e.g. antenna Ns, we run `vsum -s /mnt/vbsmnt/ny2080_ns* > ns.files`. 

## Preparing the vex and v2d files
The main control file used to tell DiFX what to do is called a .v2d file. The software also reads a .vex file. There is some partial overlap and choice where to put some settings, it can be either in v2d or vex. But both files are fundamentally required.

### Preparing the v2d file
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

### Preparing the vex file
The vex file will contain information about scan times, sources, clock corrections and Earth Orientation Parameters (EOPs). If you schedule with VieSched++ software, you may have a VEX file already. Here we assume you have skeduled with the sked software, which by default writes .skd files. However, sked can also output vex files. To convert an existing skd file to vex, we
1. Open the file in sked with `sked ../SKD_new/ny2080.skd`
2. At the prompt we use the command `VEC ny2080.vex` to save it to a vex file
3. quit the sked software

### Manually modify vex equipment setup
In theory, the vex file should be correct with all equipment and antenna settings. However, because of errors in the station catalogs, and in some cases limitations in the catalog and .skd formats, we need to manually edit the vex file. For S/X NYTIE observations, there is only one required change and this is to comment one line of code: `*    ref $TRACKS = Mk341_1f_2b-SX02:Ns;` where the `*` character indicates a commented line. If you want, you can optionally also change the correlator name to something sensible; in this case I set `target_correlator = OSO;`.

Notes if including a VGOS antenna with linear broad-band DBBC3 setup:
* This relatively limited need for modifications only applies for S/X observing. If you want to include a VGOS antenna, for example Nn, the story is a bit more complicated. Then you need to add the VGOS frequencies to the vex file. An example vex file for correlation can be seen at e.g. https://ivscc.gsfc.nasa.gov/sessions/2020/on0223/. 
* You also probably need to use "zoom windows" to override the frequency selection in difx (not only because you likely observe with different bandwidths, but also to avoid a "feature" with mixed USB/LSB correlation where some baselines are omitted.
* Finally If including a VGOS antenna, you also need to force "override" for "vex2difx" further down, since circular-linear mixed basis is not officially supported (but worked for ONTIE so far). 
* More details may be needed. The ONTIE sessions are all uploaded to IVS, also the correlator input and output (SWIN) files, so you can inspect the details if you are curious. 

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

### Add Earth Orientation Parameters
By default, IVS experiments are 24 hours. Difx wants 2 days before and 2 days after i.e. 5 days in total of EOP values in the correct format. This can be obtained by running the tool "geteop.pl" which comes with difx. Because of recent security restrictions for anonymous downloads, we need to give an email address as an environment variable when running the script. To do so and download 5 days of data starting 2 days before: `EMAIL_ADDR=your.email@example.com geteop.pl 2022-078 5` where "your.email..." should be your valid email. This will produce a file called EOP.txt which can be copied verbatim and appended as a section to the VEX file.

## Prepare the input files needed for difx
When you have the v2d and vex files, and the ny/ns.files which the v2d points to, you can translate these to the actual input files used by difx. This is done by running the command `vex2difx -v -v -v -d *.v2d`. This will, using the example v2d file above, generate one set of input file for every scan. In this case we have 800 scans, so we generate a large number of files. 

Assuming this works without errors (otherwise try to figure out why, perhaps some stray character in the v2d or vex files when you did the modifications above) the next step is to generate the delay model files. The new way to do this is to run the command `difxcalc -f *.calc` using the difxcalc program which comes with difx.
(OLD WAY, using calcif2 instead of difxcalc: If this is the first time you do this operation since booting the machine, you likely first have to run `startCalcServer`. The command to generate the model files is `calcif2 -f *.calc`.)

To start difx you also need to specify the computing setup used, i.e. number of machines, their names/IPs, and the processes to run on each machine. There are multiple ways to do this, but I have settled on my own little convenience script at https://github.com/varenius/oso/blob/master/CORR/makemachines.py. I run this in the directory with all the .input files as `python3 makemachines.py` and it will generate .machines and .threads files for all of the input files. Please see the comments inside the makemachines.py script for details on how to adapt the setup for your needs. The minimum setup for running this job (with 2 antennas, with one filelist-file per antenna) on a single machine with 4 CPU cores would be:
```
ex.threads:
NUMBER OF CORES:    1
4
ex.machines:
gyller
gyller
gyller
gyller
```
Note that in this case, "gyller" is the hostname of the machine we use. (I tried "localhost" in a previous example, and that did not work.)

# Running DiFX
To run DiFX, and not overwrite any threads or machines files based on erroneous assumptions, we use the command `startdifx -n -f -v *.input`. Note: This may take many hours if you have only a few CPU cores (and possibly I/O limitations) so it is good practice to 
* first try to correlate only a few scans, perhaps on known bright sources, to see that everything works as expected, and
* run this job in a "screen" or similar so that you can go and do other stuff while it runs
Please note that, as DiFX output will tell you, you can use e.g. the tool "errormon2" to check the progress while it's running. (This will create a log-file also in the directory where you are, which is redundant since there will be a .difxlog file for each job as well.)
The output from the correlation job will be one ".difx" folder per scan, if using the above v2d setup.

Notes:
When you run difx with the above setup, you will probably see warnings like
```
[ -1] WARNING Baseline 0 frequency 0 points at two different frequencies that are apparently identical - this is not wrong, but very strange.  Check the input file
```
This is not a problem, it will run fine anyway.

## Convert the difx output to MK4-format
For fringe-fitting we use the HOPS fourfit software. This cannot read the .difx files, but wants the old "mark4"-format. To convert, we run the tool "difx2mark4" which comes with difx. To convert all .difx folders at once we run `difx2mark4 -v  -s station_code_file.txt  *.difx`. The "-s" argument is optional but good practice, since this will force the Mark4 station labels (one single letter) to use the data in the given txt file. It is nice to use the same letters as other correlators, if possible, to simplify comparisons and questions later on. For Ny/Ns data I use a file "station_code_file.txt" with these contents:
```
w Ns
N Ny
```
By default, this creates a folder called "1234" which contains one folder per scan.

# Fringe-fitting
Fringe-fitting using fourfit is the most common way to process geodetic VLBI-data (PIMA and possibly CASA are other options). Fourfit needs a "control file" to set various parameters. Usually, we start from a previously existing control file and modify as needed. Such a control file can usually be found in the "correlator report" (see below), often included in the mk4-history in the vgosDb. For convenience, I have included the final cf_2080 control file at https://github.com/varenius/oso/blob/master/CORR/cf_ny2080. 

## Determine pc-phases using a bright scan
Assuming you have a previous control file for Ny-Ns baseline, we:
1. Make a copy that we can edit for this experiment
2. Remove any "pc_phases" lines in this file
3. Find, e.g. from vex file, one or more scan names for bright sources (good signal-to-noise). Here I picked scan "080-1307" which is bright source OJ287.

Now we want to find the instrumental "pc_phases" for the antennas. We pick one antenna as reference, which can in principle be at random. In this case, we pick station N as reference, because it's convenient (see below). We now find the pc_phases of antenna "w" by running the command `fourfit -pt -c cf_ny2080 -b wN -m 1 1234/080-1307`. This will produce a plot on screen, and output in the terminal. We note this important line:
```
pc_phases ghijklmn   32.3 -292.6  -83.6  -59.3 -234.1 -209.3 -214.6 -176.5 
```
This line contains the phase values needed to align all BBCs for a common group-delay fitting. To use these static offsets (assuming the instruments are stable) during the complete experiment, we put this line in the control file. Note: Strictly speaking these values are the "baseline difference" and not "station difference", which means we could put them either on antenna w or antenna N. However, since the baseline is given in the mark4 format as "wN" it is simplest to given them for the first antenna "w" by adding, in the control file, the lines
```
if station w
 * Determined by first commenting out, then using "-m 1" flag on bright scan
 * in this case OJ287 in scan 080-1307
 pc_phases ghijklmn   32.3 -292.6  -83.6  -59.3 -234.1 -209.3 -214.6 -176.5 
```
where any line starting with `*` is a comment. If we instead want to use these offsets for station "N", we would have to change the sign for all of the values since the baseline would be the other way around. 

Notes:
* It is now good practice to check the values by running the same command as before, but on a few different scans - ideally spread in time over the experiment. In general, you should see a well aligned phase vs time for all BBCs during the experiment. 
* If you for some reason need to use "Manual phase-cal", you modify the cf_file to say "pc_mode manual" for the antenna where this is needed, and then you do the procedure above as usual.

## Running the actual fringe-fitting
The fourfit command above with the "-pt" option will actually not write any results to disk, just show you the figure and print values in terminal. To actually fringe-fit and save the results, we run `fourfit -c cf_ny2080 -b wN 1234/*"` to fringe-fitt this baseline using our control file for all scans. this may take a while, so again it may be a good idea to run this in a screen. 

## Creating a correlator report
Technically this is an optional step, i.e. not required for analysis, but it is very good practice to do this as properly as you can. Most correlators process many data sets and soon get tired of doing this by hand. Therefore, they have various scripts to generate the correlator reports more or less automatically. So far I have not spent enough time to warrant a fully automatic tool, but I have made a short script to summarise the basic baseline statistics from fourfit which is needed for the correlator report. Note: The current correlator report format (may change soon) is described in the IVS memo https://ivscc.gsfc.nasa.gov/publications/memos/ivs-2017-001v02.pdf (which unfortunately is somewhat inconsistent, but generally a good explanation of the content). In my case, I start from an existing correlator report and manually edit the required sections. An example of a correlator report for NY2080 can be found at XXX. To genrate the text in the "SUMMARY" and "CODES" sections, one can use the script at https://github.com/varenius/oso/blob/master/CORR/crep.py. This first need you to produce an "alist" summary file from the fringe-fitted data, which can be done as 
```
alist 1234/
```
which will create the file alist.out. Then, we create the summary by running
```
python crep.py alist.out ny2080.vex station_code_file.txt 
```
For the "CLOCKS" section in the correlator report, please note that the "fs_log_rate.py" script example above also generates lines which are suitable to paste into the correlator report clocks table. For an example correlator report file, called ny2080.corr, see https://github.com/varenius/oso/blob/master/CORR/ny2080.corr.

# Creating a vgosDb
To create a vgosDb and fill it with the usual (calc, logs) content, we use the tools vgosDbMake, vgosDbCalc and vgosDbProcLogs which are bundled with the nuSolve software. Before you can process data you first need to run each tool with the "-w" option to set up paths etc. Here it is important to have current a priori files (for Calc) and a well defined directory for fs log fiels (for ProcLogs). Assuming this is all set up, we firs create the database (version 1 wrapper) by
```
LC_ALL=C vgosDbMake -d DBCODE -r OSO  -o /output_vgosDb_folder/ -t ny2080.corr /1234/
```
where `DBCODE` is constructed from the session start date and code as specified in https://cddis.nasa.gov/archive/vlbi/ivsformats/master-format.txt. In this case, it would be 22MAR21VN (agreed with IVS 2022-03-30 per email). For the other options, see "vgosDbMake --help". 
Notes:
* I usually add the `LC_ALL=C` before the command to avoid some weird issues I had a couple of years ago. Not sure this is needed anymore, but I still include it.

## Appending Calc information
We now have a wrapper version 1, and we can use it to construct a version 2 which contains Calc information
```
vgosDbCalc /path/to/database/22MAR21VN_V001_iOSO_kall.wrp 
```
## Appending FS-log information
Similarly to append FS-log info (weather, cable-cal etc.)
```
vgosDbProcLogs -k log /path/to/database/22MAR21VN_V002_iOSO_kall.wrp
```
This will create a "version 3" wrapper.

# Creating a version 4 wrapper with editing and ambiguity resolution using nuSolve 

We now open the V003-wrapper with nuSolve. After opening the wrapper and checking that the loading log output looks sensible (no big errors or important warnings), I usually click "Options--> Clocks: PWL, Baseline vector: LCL, Outliers Action: Elimination, Reweighting Action: Evaluate weight correction". then I switch to "Bands" and select "Y: Res GR delay, ns". Then I press "Process" 5 times or so to converge, then remove outliers either automatically with "Outlr" button or manually by selecting the points in the display using the mouse and then pressing "CTRL-X" on the keyboard. Then press "process" some more times until converge. You may have to hit the "Ambig" button to resolve ambiguities. Once you have converted and the residuals look reasonable Gaussian, and you may be done. In this case, press "Save" to save the results to a new (automatically the highest + 1) wrapper version. 

If you also want to process phase-delays, you can select "Y: Res PH delay, ns" and repeat the outlier-removal and ambiguity resolution procedure. You may have to do this interatively a few times, including dosens of "Process" clicks before you converge. Then, if you save again, you will get the phase delay editing and amibguity multipliers stored in another (by defauly now version 5) database wrapper.  
