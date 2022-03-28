Guid to correlate NY2080 and other similar experiments
Eskil Varenius
Onsala Space Observatory
2022-03-28



Edit .v2d file, example attached.

fusermount -u /mnt/vbsmnt ; vbs_fs /mnt/vbsmnt/ -I "ny2080*"

m5bsum -s /mnt/vbsmnt/ny2080_ny* > ny.files
vsum -s /mnt/vbsmnt/ny2080_ns* > ns.files

eskil@grotte:~/NYTIE/VEX_for_corr$ sked ../SKD_new/ny2075.skd 
...
End of listing.
? VEC ny20780.vex
...
SKED output file ./ny2080.vex finished.
quit


EDIT VEX file to comment out this line:
*    ref $TRACKS = Mk341_1f_2b-SX02:Ns;
Can also change correlator line to something sensible now, e.g:
target_correlator = OSO;


oper@gyller:/mnt/raidz0/NYTIE/ny2080$ python3 /home/oper/eskil/eskil.oso.git/CORR/fs_log_rate.py -l ny2080ns.log 
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
oper@gyller:/mnt/raidz0/NYTIE/ny2080$ python3 /home/oper/eskil/eskil.oso.git/CORR/fs_log_rate.py -l ny2080ny.log 
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



$CLOCK;
*                  valid from           clock_early    clock_early_epoch        rate
def Ns;  clock_early = 2022y080d00h00m00s : 25.493 usec : 2022y080d00h00m00s : 0.232e-12; enddef;
def Ny;  clock_early = 2022y080d00h00m00s : -86.804 usec : 2022y080d00h00m00s : -0.184e-12; enddef;

Run geteop.pl with date 2 days before exp start and 5 days in total
EMAIL_ADDR=eskil.varenius@chalmers.se geteop.pl 2022-078 5
--> EOP.txt
append EOP file to vex file


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




