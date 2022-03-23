define  proc_library  21267213741x
" ONSA13NE default VGOS obs library
" Manually constructed outside DRUDG
"< DBBC3_DDC            rack >< FlexBuff recorder 1>
enddef
define  exper_initi   21267213741
proc_library
sched_initi
onoff=2,2,,,,,049u,050u,051u,052u,053u,054u,055u,056u,057u,058u,059u,060u,061u,062u,063u,064u
mk5=dts_id?
mk5=os_rev?
mk5_status
setupbb
enddef
define  setupbb       21267213747
pcalon
tpicd=stop
core3hbb=$
fb_mode=vdif,,,64
fb_mode
jive5ab_cnfg
dbbcbb32
ifdbb
cont_cal=on,2
tpicd=no,100
tpicd
enddef
define  dbbcbb32      21267213758x9x
bbc049=2603.01,g,32,1
bbc050=2643.01,g,32,1
bbc051=2683.01,g,32,1
bbc052=2803.01,g,32,1
bbc053=3023.01,g,32,1
bbc054=3183.01,g,32,1
bbc055=3283.01,g,32,1
bbc056=3323.01,g,32,1
bbc057=2603.01,h,32,1
bbc058=2643.01,h,32,1
bbc059=2683.01,h,32,1
bbc060=2803.01,h,32,1
bbc061=3023.01,h,32,1
bbc062=3183.01,h,32,1
bbc063=3283.01,h,32,1
bbc064=3323.01,h,32,1
enddef
define  ifdbb       2121267213759x
ifg=2,agc,32000
ifh=2,agc,32000
lo=
lo=log,11600,lsb,lcp
lo=loh,11600,lsb,rcp
enddef
define  core3hbb      21267214623x
core3h_mode0=begin,force
core3h_mode7=,0x33333333,,64.0,
core3h_mode8=,0x33333333,,64.0,
core3h_mode0=end,force
enddef
