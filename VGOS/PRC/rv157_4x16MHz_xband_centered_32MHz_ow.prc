define  proc_library  21323073850x
"OW R1 X-band library
" Manually constructed outside DRUDG
"< DBBC3_DDC            rack >< FlexBuff recorder 1>
enddef
define  exper_initi   21323073850
proc_library
sched_initi
onoff=2,2,,,,,049u,050u,051u,052u,053u,054u,055u,056u,057u,058u,059u,060u,061u,062u,063u,064u
fb=dts_id?
fb=os_rev?
fb_status
setup01
enddef
define  setup01       21323073856
pcalon
tpicd=stop
core3hbb=$
fb_mode=vdif,,,64
fb_mode
fb_config
dbbcbb32
ifdbb
cont_cal=on,2
bbc_gain=all,agc
tpicd=no,100
tpicd
enddef
define  dbbcbb32      21323073911x9x
bbc049=2650.25,g,32,1
bbc050=2770.25,g,32,1
bbc051=3130.25,g,32,1
bbc052=3210.25,g,32,1
bbc053=2650.25,g,32,1
bbc054=2770.25,g,32,1
bbc055=3130.25,g,32,1
bbc056=3210.25,g,32,1
bbc057=2650.25,h,32,1
bbc058=2770.25,h,32,1
bbc059=3130.25,h,32,1
bbc060=3210.25,h,32,1
bbc061=2650.25,h,32,1
bbc062=2770.25,h,32,1
bbc063=3130.25,h,32,1
bbc064=3210.25,h,32,1
enddef
define  ifdbb       2121323073912x
ifg=2,agc,32000
ifh=2,agc,32000
lo=
lo=log,11600,lsb,lcp
lo=loh,11600,lsb,rcp
enddef
define  core3hbb      00000000000
core3h_mode=begin,force
core3h_mode=7,,0x33333333,,64.0,$
core3h_mode=8,,0x33333333,,64.0,$
core3h_mode=end,force
enddef
