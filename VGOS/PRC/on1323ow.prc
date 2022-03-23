define  proc_library  21323073850x
"ONTIE on1323 obs library
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
setupxx
enddef
define  setupxx       21323073856
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
bbc049=2603.01,g,32,1
bbc050=2643.01,g,32,1
bbc051=2683.01,g,32,1
bbc052=2803.01,g,32,1
bbc053=3023.01,g,32,1
bbc054=3183.01,g,32,1
bbc055=3428.01,g,32,1
bbc056=3468.01,g,32,1
bbc057=2603.01,h,32,1
bbc058=2643.01,h,32,1
bbc059=2683.01,h,32,1
bbc060=2803.01,h,32,1
bbc061=3023.01,h,32,1
bbc062=3183.01,h,32,1
bbc063=3428.01,h,32,1
bbc064=3468.01,h,32,1
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
