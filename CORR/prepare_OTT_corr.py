#!/usr/bin/env python3
import sys, os, glob
import datetime, time
import numpy as np
import matplotlib.dates as mdates
from subprocess import run, PIPE
import socket

def fillantenna(of, antennas):
    # Always include all to avoid vex2difx vex-parsing confusion, does not hurt.
    of.write("def ONSA13NE;\n")
    of.write("    antenna_diam = 13.2 m;\n")
    of.write("    axis_type = az : el;\n")
    of.write("    axis_offset = 0 m;\n")
    of.write("    antenna_motion =  az: 720 deg/min:   5 sec;\n")
    of.write("    antenna_motion =  el: 360 deg/min:   4 sec;\n")
    of.write("    pointing_sector = &ccw   :  az :  -65 deg :   65 deg :  el :    5 deg :   90 deg ;\n")
    of.write("    pointing_sector = &n     :  az :   65 deg :  295 deg :  el :    5 deg :   90 deg ;\n")
    of.write("    pointing_sector = &cw    :  az :  295 deg :  425 deg :  el :    5 deg :   90 deg ;\n")
    of.write("enddef;\n")
    of.write("def ONSA13SW;\n")
    of.write("    antenna_diam = 13.2 m;\n")
    of.write("    axis_type = az : el;\n")
    of.write("    axis_offset = 0 m;\n")
    of.write("    antenna_motion =  az: 720 deg/min:   5 sec;\n")
    of.write("    antenna_motion =  el: 360 deg/min:   4 sec;\n")
    of.write("    pointing_sector = &ccw   :  az :  -65 deg :   65 deg :  el :    5 deg :   90 deg ;\n")
    of.write("    pointing_sector = &n     :  az :   65 deg :  295 deg :  el :    5 deg :   90 deg ;\n")
    of.write("    pointing_sector = &cw    :  az :  295 deg :  425 deg :  el :    5 deg :   90 deg ;\n")
    of.write("enddef;\n")
    of.write("def ONSALA60;\n")
    of.write("    antenna_diam = 20 m;\n")
    of.write("    axis_type = az : el;\n")
    of.write("    axis_offset = 0 m;\n")
    of.write("    antenna_motion =  az: 183 deg/min:  20 sec;\n")
    of.write("    antenna_motion =  el:  60 deg/min:  18 sec;\n")
    of.write("    pointing_sector = &ccw   :  az :  340 deg :  380 deg :  el :    5 deg :   85 deg ;\n")
    of.write("    pointing_sector = &n     :  az :  380 deg :  700 deg :  el :    5 deg :   85 deg ;\n")
    of.write("    pointing_sector = &cw    :  az :  700 deg :  740 deg :  el :    5 deg :   85 deg ;\n")
    of.write("enddef;\n")
    of.write("def ISHIOKA;\n")
    of.write("    antenna_diam =  13.20 m;\n")
    of.write("    axis_type = az : el;\n")
    of.write("    axis_offset =    0.00000 m;\n")
    of.write("    antenna_motion = az : 720.0 deg/min :  10.0 sec;\n")
    of.write("    antenna_motion = el : 360.0 deg/min :  10.0 sec;\n")
    of.write("    pointing_sector = &n : az :  290.0 deg :  790.0 deg : el :    5.0 deg :   89.0 deg;\n")
    of.write("enddef;\n")

def fillstation(of, antennas):
    # Always include all to avoid vex2difx vex-parsing confusion, does not hurt.
    of.write("def Oe;\n")
    of.write("    ref $SITE = ONSA13NE;\n")
    of.write("    ref $ANTENNA = ONSA13NE;\n")
    of.write("    ref $DAS = FlexBuff_recorder;\n")
    of.write("    ref $DAS = DBBC3_DDC_rack;\n")
    of.write("    ref $DAS = Oe_Oe;\n")
    of.write("enddef;\n")
    of.write("def Ow;\n")
    of.write("    ref $SITE = ONSA13SW;\n")
    of.write("    ref $ANTENNA = ONSA13SW;\n")
    of.write("    ref $DAS = FlexBuff_recorder;\n")
    of.write("    ref $DAS = DBBC3_DDC_rack;\n")
    of.write("    ref $DAS = Ow_Ow;\n")
    of.write("enddef;\n")
    of.write("def On;\n")
    of.write("    ref $SITE = ONSALA60;\n")
    of.write("    ref $ANTENNA = ONSALA60;\n")
    of.write("    ref $DAS = FlexBuff_recorder;\n")
    of.write("    ref $DAS = DBBC_DDC_rack;\n")
    of.write("    ref $DAS = On_02;\n")
    of.write("enddef;\n")
    of.write("def Is;\n")
    of.write("    ref $SITE = ISHIOKA;\n")
    of.write("    ref $ANTENNA = ISHIOKA;\n")
    of.write("    ref $DAS = K4-2_rack;\n")
    of.write("    ref $DAS = Is_Is;\n")
    of.write("    ref $DAS = K5_recorder;\n")
    of.write("enddef;\n")

def fillsite(of, antennas):
    # Always include all to avoid vex2difx vex-parsing confusion, does not hurt.
    of.write("def ONSA13NE;\n")
    of.write("    site_type = fixed;\n")
    of.write("    site_name = ONSA13NE;\n")
    of.write("    site_ID = Oe;\n")
    of.write("    site_position =  3370889.298 m :   711571.199 m :  5349692.048 m;\n")
    of.write("    site_position_ref = sked_position.cat;\n")
    of.write("    occupation_code = 00000000;\n")
    of.write("enddef;\n")
    of.write("def ONSA13SW;\n")
    of.write("    site_type = fixed;\n")
    of.write("    site_name = ONSA13SW;\n")
    of.write("    site_ID = Ow;\n")
    of.write("    site_position =  3370946.779 m :   711534.507 m :  5349660.925 m;\n")
    of.write("    site_position_ref = sked_position.cat;\n")
    of.write("    occupation_code = 00000000;\n")
    of.write("enddef;\n")
    of.write("def ONSALA60;\n")
    of.write("    site_type = fixed;\n")
    of.write("    site_name = ONSALA60;\n")
    of.write("    site_ID = On;\n")
    of.write("    site_position =  3370605.690 m :   711917.824 m :  5349830.993 m;\n")
    of.write("    site_position_ref = sked_position.cat;\n")
    of.write("    occupation_code = 72137701;\n")
    of.write("enddef;\n")
    of.write("def ISHIOKA;\n")
    of.write("    site_type = fixed;\n")
    of.write("    site_name = ISHIOKA;\n")
    of.write("    site_ID = Is;\n")
    of.write("    site_position = -3959636.203 m :  3296825.448 m :  3747042.571 m;\n")
    of.write("    occupation_code = 00000000;\n")
    of.write("enddef;\n")

def filltracks(of, setup):
    of.write("  def VDIF;\n")
    of.write("    track_frame_format = VDIF;\n")
    of.write("  enddef;\n")

def fillmode(of, setup, antennas):
    if setup=="VGOS":
        if "Is" in antennas:
            of.write("  def VGOS;\n")
            of.write("    ref $FREQ = VGOS:Oe:Ow;\n")
            of.write("    ref $FREQ = VGOS_Is:Is;\n")
            of.write("    ref $BBC = VGOS:Oe:Ow:Is;\n")
            of.write("    ref $IF = VGOS:Oe:Ow:Is;\n")
            of.write("    ref $PHASE_CAL_DETECT = Standard:Oe:Ow:Is;\n")
            of.write("    ref $TRACKS = VDIF:Oe:Ow:Is;\n")
            of.write("  enddef;\n")
        else:
            of.write("  def VGOS;\n")
            of.write("    ref $FREQ = VGOS:Oe:Ow;\n")
            of.write("    ref $BBC = VGOS:Oe:Ow;\n")
            of.write("    ref $IF = VGOS:Oe:Ow;\n")
            of.write("    ref $TRACKS = VDIF:Oe:Ow;\n")
            of.write("    ref $PHASE_CAL_DETECT = OTT:Oe:Ow;\n")
            of.write("  enddef;\n")
    elif setup=="on1323":
        of.write("def on1323;\n")
        of.write("    ref $FREQ = FREQ_20m     : On ;\n")
        of.write("    ref $FREQ = FREQ_OTT     : Oe : Ow ;\n")
        of.write("    ref $BBC = BBC_20m       : On ;\n")
        of.write("    ref $BBC = BBC_OTT       : Oe : Ow ;\n")
        of.write("    ref $IF = IF_20m         : On ;\n")
        of.write("    ref $IF = OTT            : Oe : Ow ;\n")
        of.write("    ref $TRACKS = VDIF       : Oe : Ow : On ;\n")
        of.write("    ref $PHASE_CAL_DETECT = Standard  : Oe : Ow : On ;\n")
        of.write("enddef;\n")
    elif setup=="r11089":
        of.write("def r11089;\n")
        of.write("    ref $FREQ = FREQ_20m     : On ;\n")
        of.write("    ref $FREQ = FREQ_OTT     : Oe : Ow ;\n")
        of.write("    ref $BBC = BBC_20m       : On ;\n")
        of.write("    ref $BBC = BBC_OTT       : Oe : Ow ;\n")
        of.write("    ref $IF = IF_20m         : On ;\n")
        of.write("    ref $IF = OTT            : Oe : Ow ;\n")
        of.write("    ref $TRACKS = VDIF       : Oe : Ow : On ;\n")
        of.write("    ref $PHASE_CAL_DETECT = Standard  : Oe : Ow : On ;\n")
        of.write("enddef;\n")
    elif setup=="rv157":
        of.write("def rv157;\n")
        of.write("    ref $FREQ = FREQ_20m     : On ;\n")
        of.write("    ref $FREQ = FREQ_OTT     : Oe : Ow ;\n")
        of.write("    ref $BBC = BBC_20m       : On ;\n")
        of.write("    ref $BBC = BBC_OTT       : Oe : Ow ;\n")
        of.write("    ref $IF = IF_20m         : On ;\n")
        of.write("    ref $IF = OTT            : Oe : Ow ;\n")
        of.write("    ref $TRACKS = VDIF       : Oe : Ow : On ;\n")
        of.write("    ref $PHASE_CAL_DETECT = Standard  : Oe : Ow : On ;\n")
        of.write("enddef;\n")

def fillbbc(of, setup):
    if setup == "VGOS":
        of.write("  def VGOS;\n")
        of.write("    BBC_assign = &BBC01 : 01 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC02 : 02 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC03 : 03 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC04 : 04 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC05 : 05 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC06 : 06 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC07 : 07 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC08 : 08 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC09 : 09 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC10 : 10 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC11 : 11 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC12 : 12 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC13 : 13 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC14 : 14 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC15 : 15 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC16 : 16 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC17 : 17 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC18 : 18 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC19 : 19 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC20 : 20 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC21 : 21 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC22 : 22 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC23 : 23 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC24 : 24 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC25 : 25 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC26 : 26 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC27 : 27 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC28 : 28 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC29 : 29 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC30 : 30 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC31 : 31 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC32 : 32 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC33 : 33 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC34 : 34 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC35 : 35 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC36 : 36 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC37 : 37 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC38 : 38 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC39 : 39 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC40 : 40 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC41 : 41 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC42 : 42 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC43 : 43 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC44 : 44 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC45 : 45 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC46 : 46 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC47 : 47 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC48 : 48 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC49 : 49 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC50 : 50 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC51 : 51 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC52 : 52 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC53 : 53 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC54 : 54 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC55 : 55 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC56 : 56 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC57 : 57 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC58 : 58 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC59 : 59 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC60 : 60 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC61 : 61 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC62 : 62 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC63 : 63 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC64 : 64 : &IF_3N;\n")
        of.write("  enddef;\n")
    elif setup=="on1323":
        of.write("def BBC_20m;\n")
        of.write("    BBC_assign = &BBC01 :    01 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC02 :    02 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC03 :    03 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC04 :    04 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC05 :    05 : &IF_B1;\n")
        of.write("    BBC_assign = &BBC06 :    06 : &IF_B1;\n")
        of.write("    BBC_assign = &BBC07 :    07 : &IF_B1;\n")
        of.write("    BBC_assign = &BBC08 :    08 : &IF_B1;\n")
        of.write("enddef;\n")
        of.write("def BBC_OTT;\n")
        of.write("    BBC_assign = &BBC01 : 01 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC02 : 02 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC03 : 03 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC04 : 04 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC05 : 05 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC06 : 06 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC07 : 07 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC08 : 08 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC09 : 09 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC10 : 10 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC11 : 11 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC12 : 12 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC13 : 13 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC14 : 14 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC15 : 15 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC16 : 16 : &IF_3N;\n")
        of.write("enddef;\n")
    elif setup=="r11089":
        of.write("def BBC_20m;\n")
        of.write("    BBC_assign = &BBC01 :    01 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC02 :    02 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC03 :    03 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC04 :    04 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC05 :    05 : &IF_B1;\n")
        of.write("    BBC_assign = &BBC06 :    06 : &IF_B1;\n")
        of.write("    BBC_assign = &BBC07 :    07 : &IF_B1;\n")
        of.write("    BBC_assign = &BBC08 :    08 : &IF_B1;\n")
        of.write("    BBC_assign = &BBC09 :    09 : &IF_C1;\n")
        of.write("    BBC_assign = &BBC10 :    10 : &IF_C1;\n")
        of.write("    BBC_assign = &BBC11 :    11 : &IF_C1;\n")
        of.write("    BBC_assign = &BBC12 :    12 : &IF_C1;\n")
        of.write("    BBC_assign = &BBC13 :    13 : &IF_D1;\n")
        of.write("    BBC_assign = &BBC14 :    14 : &IF_D1;\n")
        of.write("enddef;\n")
        of.write("def BBC_OTT;\n")
        of.write("    BBC_assign = &BBC01 : 01 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC02 : 02 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC03 : 03 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC04 : 04 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC05 : 05 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC06 : 06 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC07 : 07 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC08 : 08 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC09 : 09 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC10 : 10 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC11 : 11 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC12 : 12 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC13 : 13 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC14 : 14 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC15 : 15 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC16 : 16 : &IF_3N;\n")
        of.write("enddef;\n")
    elif setup=="rv157":
        of.write("def BBC_20m;\n")
        of.write("    BBC_assign = &BBC03 : 03 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC04 : 04 : &IF_A1;\n")
        of.write("    BBC_assign = &BBC05 : 05 : &IF_B1;\n")
        of.write("    BBC_assign = &BBC06 : 06 : &IF_B1;\n")
        of.write("    BBC_assign = &BBC09 : 09 : &IF_C1;\n")
        of.write("    BBC_assign = &BBC10 : 10 : &IF_C1;\n")
        of.write("    BBC_assign = &BBC13 : 13 : &IF_D1;\n")
        of.write("    BBC_assign = &BBC14 : 14 : &IF_D1;\n")
        of.write("enddef;\n")
        of.write("def BBC_OTT;\n")
        of.write("    BBC_assign = &BBC01 : 01 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC02 : 02 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC03 : 03 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC04 : 04 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC05 : 05 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC06 : 06 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC07 : 07 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC08 : 08 : &IF_1N;\n")
        of.write("    BBC_assign = &BBC09 : 09 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC10 : 10 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC11 : 11 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC12 : 12 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC13 : 13 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC14 : 14 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC15 : 15 : &IF_3N;\n")
        of.write("    BBC_assign = &BBC16 : 16 : &IF_3N;\n")
        of.write("enddef;\n")

def fillfreq(of, setup, antennas):
    if setup == "VGOS":
        # Always include all to avoid vex2difx vex-parsing confusion, does not hurt.
        of.write("  def VGOS_Is;\n")
        of.write("    chan_def = &X : 3032.40 MHz : L : 32.000 MHz : &Ch01 : &BBC01 : &L_cal;\n")
        of.write("    chan_def = &X : 3064.40 MHz : L : 32.000 MHz : &Ch02 : &BBC02 : &L_cal;\n")
        of.write("    chan_def = &X : 3096.40 MHz : L : 32.000 MHz : &Ch03 : &BBC03 : &L_cal;\n")
        of.write("    chan_def = &X : 3224.40 MHz : L : 32.000 MHz : &Ch04 : &BBC04 : &L_cal;\n")
        of.write("    chan_def = &X : 3320.40 MHz : L : 32.000 MHz : &Ch05 : &BBC05 : &L_cal;\n")
        of.write("    chan_def = &X : 3384.40 MHz : L : 32.000 MHz : &Ch06 : &BBC06 : &L_cal;\n")
        of.write("    chan_def = &X : 3448.40 MHz : L : 32.000 MHz : &Ch07 : &BBC07 : &L_cal;\n")
        of.write("    chan_def = &X : 3480.40 MHz : L : 32.000 MHz : &Ch08 : &BBC08 : &L_cal;\n")
        of.write("    chan_def = &X : 3032.40 MHz : L : 32.000 MHz : &Ch09 : &BBC09 : &L_cal;\n")
        of.write("    chan_def = &X : 3064.40 MHz : L : 32.000 MHz : &Ch10 : &BBC10 : &L_cal;\n")
        of.write("    chan_def = &X : 3096.40 MHz : L : 32.000 MHz : &Ch11 : &BBC11 : &L_cal;\n")
        of.write("    chan_def = &X : 3224.40 MHz : L : 32.000 MHz : &Ch12 : &BBC12 : &L_cal;\n")
        of.write("    chan_def = &X : 3320.40 MHz : L : 32.000 MHz : &Ch13 : &BBC13 : &L_cal;\n")
        of.write("    chan_def = &X : 3384.40 MHz : L : 32.000 MHz : &Ch14 : &BBC14 : &L_cal;\n")
        of.write("    chan_def = &X : 3448.40 MHz : L : 32.000 MHz : &Ch15 : &BBC15 : &L_cal;\n")
        of.write("    chan_def = &X : 3480.40 MHz : L : 32.000 MHz : &Ch16 : &BBC16 : &L_cal;\n")
        of.write("    chan_def = &X : 5272.40 MHz : L : 32.000 MHz : &Ch17 : &BBC17 : &L_cal;\n")
        of.write("    chan_def = &X : 5304.40 MHz : L : 32.000 MHz : &Ch18 : &BBC18 : &L_cal;\n")
        of.write("    chan_def = &X : 5336.40 MHz : L : 32.000 MHz : &Ch19 : &BBC19 : &L_cal;\n")
        of.write("    chan_def = &X : 5464.40 MHz : L : 32.000 MHz : &Ch20 : &BBC20 : &L_cal;\n")
        of.write("    chan_def = &X : 5560.40 MHz : L : 32.000 MHz : &Ch21 : &BBC21 : &L_cal;\n")
        of.write("    chan_def = &X : 5624.40 MHz : L : 32.000 MHz : &Ch22 : &BBC22 : &L_cal;\n")
        of.write("    chan_def = &X : 5688.40 MHz : L : 32.000 MHz : &Ch23 : &BBC23 : &L_cal;\n")
        of.write("    chan_def = &X : 5720.40 MHz : L : 32.000 MHz : &Ch24 : &BBC24 : &L_cal;\n")
        of.write("    chan_def = &X : 5272.40 MHz : L : 32.000 MHz : &Ch25 : &BBC25 : &L_cal;\n")
        of.write("    chan_def = &X : 5304.40 MHz : L : 32.000 MHz : &Ch26 : &BBC26 : &L_cal;\n")
        of.write("    chan_def = &X : 5336.40 MHz : L : 32.000 MHz : &Ch27 : &BBC27 : &L_cal;\n")
        of.write("    chan_def = &X : 5464.40 MHz : L : 32.000 MHz : &Ch28 : &BBC28 : &L_cal;\n")
        of.write("    chan_def = &X : 5560.40 MHz : L : 32.000 MHz : &Ch29 : &BBC29 : &L_cal;\n")
        of.write("    chan_def = &X : 5624.40 MHz : L : 32.000 MHz : &Ch30 : &BBC30 : &L_cal;\n")
        of.write("    chan_def = &X : 5688.40 MHz : L : 32.000 MHz : &Ch31 : &BBC31 : &L_cal;\n")
        of.write("    chan_def = &X : 5720.40 MHz : L : 32.000 MHz : &Ch32 : &BBC32 : &L_cal;\n")
        of.write("    chan_def = &X : 6392.40 MHz : L : 32.000 MHz : &Ch33 : &BBC33 : &L_cal;\n")
        of.write("    chan_def = &X : 6424.40 MHz : L : 32.000 MHz : &Ch34 : &BBC34 : &L_cal;\n")
        of.write("    chan_def = &X : 6456.40 MHz : L : 32.000 MHz : &Ch35 : &BBC35 : &L_cal;\n")
        of.write("    chan_def = &X : 6584.40 MHz : L : 32.000 MHz : &Ch36 : &BBC36 : &L_cal;\n")
        of.write("    chan_def = &X : 6680.40 MHz : L : 32.000 MHz : &Ch37 : &BBC37 : &L_cal;\n")
        of.write("    chan_def = &X : 6744.40 MHz : L : 32.000 MHz : &Ch38 : &BBC38 : &L_cal;\n")
        of.write("    chan_def = &X : 6808.40 MHz : L : 32.000 MHz : &Ch39 : &BBC39 : &L_cal;\n")
        of.write("    chan_def = &X : 6840.40 MHz : L : 32.000 MHz : &Ch40 : &BBC40 : &L_cal;\n")
        of.write("    chan_def = &X : 6392.40 MHz : L : 32.000 MHz : &Ch41 : &BBC41 : &L_cal;\n")
        of.write("    chan_def = &X : 6424.40 MHz : L : 32.000 MHz : &Ch42 : &BBC42 : &L_cal;\n")
        of.write("    chan_def = &X : 6456.40 MHz : L : 32.000 MHz : &Ch43 : &BBC43 : &L_cal;\n")
        of.write("    chan_def = &X : 6584.40 MHz : L : 32.000 MHz : &Ch44 : &BBC44 : &L_cal;\n")
        of.write("    chan_def = &X : 6680.40 MHz : L : 32.000 MHz : &Ch45 : &BBC45 : &L_cal;\n")
        of.write("    chan_def = &X : 6744.40 MHz : L : 32.000 MHz : &Ch46 : &BBC46 : &L_cal;\n")
        of.write("    chan_def = &X : 6808.40 MHz : L : 32.000 MHz : &Ch47 : &BBC47 : &L_cal;\n")
        of.write("    chan_def = &X : 6840.40 MHz : L : 32.000 MHz : &Ch48 : &BBC48 : &L_cal;\n")
        of.write("    chan_def = &X : 10232.40 MHz : L : 32.000 MHz : &Ch49 : &BBC49 : &L_cal;\n")
        of.write("    chan_def = &X : 10264.40 MHz : L : 32.000 MHz : &Ch50 : &BBC50 : &L_cal;\n")
        of.write("    chan_def = &X : 10296.40 MHz : L : 32.000 MHz : &Ch51 : &BBC51 : &L_cal;\n")
        of.write("    chan_def = &X : 10424.40 MHz : L : 32.000 MHz : &Ch52 : &BBC52 : &L_cal;\n")
        of.write("    chan_def = &X : 10520.40 MHz : L : 32.000 MHz : &Ch53 : &BBC53 : &L_cal;\n")
        of.write("    chan_def = &X : 10584.40 MHz : L : 32.000 MHz : &Ch54 : &BBC54 : &L_cal;\n")
        of.write("    chan_def = &X : 10648.40 MHz : L : 32.000 MHz : &Ch55 : &BBC55 : &L_cal;\n")
        of.write("    chan_def = &X : 10680.40 MHz : L : 32.000 MHz : &Ch56 : &BBC56 : &L_cal;\n")
        of.write("    chan_def = &X : 10232.40 MHz : L : 32.000 MHz : &Ch57 : &BBC57 : &L_cal;\n")
        of.write("    chan_def = &X : 10264.40 MHz : L : 32.000 MHz : &Ch58 : &BBC58 : &L_cal;\n")
        of.write("    chan_def = &X : 10296.40 MHz : L : 32.000 MHz : &Ch59 : &BBC59 : &L_cal;\n")
        of.write("    chan_def = &X : 10424.40 MHz : L : 32.000 MHz : &Ch60 : &BBC60 : &L_cal;\n")
        of.write("    chan_def = &X : 10520.40 MHz : L : 32.000 MHz : &Ch61 : &BBC61 : &L_cal;\n")
        of.write("    chan_def = &X : 10584.40 MHz : L : 32.000 MHz : &Ch62 : &BBC62 : &L_cal;\n")
        of.write("    chan_def = &X : 10648.40 MHz : L : 32.000 MHz : &Ch63 : &BBC63 : &L_cal;\n")
        of.write("    chan_def = &X : 10680.40 MHz : L : 32.000 MHz : &Ch64 : &BBC64 : &L_cal;\n")
        of.write("    sample_rate = 64.0 Ms/sec;\n")
        of.write("  enddef;\n")
        # Write OeOw data
        of.write("  def VGOS;\n")
        of.write("    chan_def = &X : 3480.40 MHz : L : 32.000 MHz : &Ch01 : &BBC01 : &L_cal;\n")
        of.write("    chan_def = &X : 3448.40 MHz : L : 32.000 MHz : &Ch02 : &BBC02 : &L_cal;\n")
        of.write("    chan_def = &X : 3384.40 MHz : L : 32.000 MHz : &Ch03 : &BBC03 : &L_cal;\n")
        of.write("    chan_def = &X : 3320.40 MHz : L : 32.000 MHz : &Ch04 : &BBC04 : &L_cal;\n")
        of.write("    chan_def = &X : 3224.40 MHz : L : 32.000 MHz : &Ch05 : &BBC05 : &L_cal;\n")
        of.write("    chan_def = &X : 3096.40 MHz : L : 32.000 MHz : &Ch06 : &BBC06 : &L_cal;\n")
        of.write("    chan_def = &X : 3064.40 MHz : L : 32.000 MHz : &Ch07 : &BBC07 : &L_cal;\n")
        of.write("    chan_def = &X : 3032.40 MHz : L : 32.000 MHz : &Ch08 : &BBC08 : &L_cal;\n")
        of.write("    chan_def = &X : 3480.40 MHz : L : 32.000 MHz : &Ch09 : &BBC09 : &L_cal;\n")
        of.write("    chan_def = &X : 3448.40 MHz : L : 32.000 MHz : &Ch10 : &BBC10 : &L_cal;\n")
        of.write("    chan_def = &X : 3384.40 MHz : L : 32.000 MHz : &Ch11 : &BBC11 : &L_cal;\n")
        of.write("    chan_def = &X : 3320.40 MHz : L : 32.000 MHz : &Ch12 : &BBC12 : &L_cal;\n")
        of.write("    chan_def = &X : 3224.40 MHz : L : 32.000 MHz : &Ch13 : &BBC13 : &L_cal;\n")
        of.write("    chan_def = &X : 3096.40 MHz : L : 32.000 MHz : &Ch14 : &BBC14 : &L_cal;\n")
        of.write("    chan_def = &X : 3064.40 MHz : L : 32.000 MHz : &Ch15 : &BBC15 : &L_cal;\n")
        of.write("    chan_def = &X : 3032.40 MHz : L : 32.000 MHz : &Ch16 : &BBC16 : &L_cal;\n")
        of.write("    chan_def = &X : 5720.40 MHz : L : 32.000 MHz : &Ch17 : &BBC17 : &L_cal;\n")
        of.write("    chan_def = &X : 5688.40 MHz : L : 32.000 MHz : &Ch18 : &BBC18 : &L_cal;\n")
        of.write("    chan_def = &X : 5624.40 MHz : L : 32.000 MHz : &Ch19 : &BBC19 : &L_cal;\n")
        of.write("    chan_def = &X : 5560.40 MHz : L : 32.000 MHz : &Ch20 : &BBC20 : &L_cal;\n")
        of.write("    chan_def = &X : 5464.40 MHz : L : 32.000 MHz : &Ch21 : &BBC21 : &L_cal;\n")
        of.write("    chan_def = &X : 5336.40 MHz : L : 32.000 MHz : &Ch22 : &BBC22 : &L_cal;\n")
        of.write("    chan_def = &X : 5304.40 MHz : L : 32.000 MHz : &Ch23 : &BBC23 : &L_cal;\n")
        of.write("    chan_def = &X : 5272.40 MHz : L : 32.000 MHz : &Ch24 : &BBC24 : &L_cal;\n")
        of.write("    chan_def = &X : 5720.40 MHz : L : 32.000 MHz : &Ch25 : &BBC25 : &L_cal;\n")
        of.write("    chan_def = &X : 5688.40 MHz : L : 32.000 MHz : &Ch26 : &BBC26 : &L_cal;\n")
        of.write("    chan_def = &X : 5624.40 MHz : L : 32.000 MHz : &Ch27 : &BBC27 : &L_cal;\n")
        of.write("    chan_def = &X : 5560.40 MHz : L : 32.000 MHz : &Ch28 : &BBC28 : &L_cal;\n")
        of.write("    chan_def = &X : 5464.40 MHz : L : 32.000 MHz : &Ch29 : &BBC29 : &L_cal;\n")
        of.write("    chan_def = &X : 5336.40 MHz : L : 32.000 MHz : &Ch30 : &BBC30 : &L_cal;\n")
        of.write("    chan_def = &X : 5304.40 MHz : L : 32.000 MHz : &Ch31 : &BBC31 : &L_cal;\n")
        of.write("    chan_def = &X : 5272.40 MHz : L : 32.000 MHz : &Ch32 : &BBC32 : &L_cal;\n")
        of.write("    chan_def = &X : 6840.40 MHz : L : 32.000 MHz : &Ch33 : &BBC33 : &L_cal;\n")
        of.write("    chan_def = &X : 6808.40 MHz : L : 32.000 MHz : &Ch34 : &BBC34 : &L_cal;\n")
        of.write("    chan_def = &X : 6744.40 MHz : L : 32.000 MHz : &Ch35 : &BBC35 : &L_cal;\n")
        of.write("    chan_def = &X : 6680.40 MHz : L : 32.000 MHz : &Ch36 : &BBC36 : &L_cal;\n")
        of.write("    chan_def = &X : 6584.40 MHz : L : 32.000 MHz : &Ch37 : &BBC37 : &L_cal;\n")
        of.write("    chan_def = &X : 6456.40 MHz : L : 32.000 MHz : &Ch38 : &BBC38 : &L_cal;\n")
        of.write("    chan_def = &X : 6424.40 MHz : L : 32.000 MHz : &Ch39 : &BBC39 : &L_cal;\n")
        of.write("    chan_def = &X : 6392.40 MHz : L : 32.000 MHz : &Ch40 : &BBC40 : &L_cal;\n")
        of.write("    chan_def = &X : 6840.40 MHz : L : 32.000 MHz : &Ch41 : &BBC41 : &L_cal;\n")
        of.write("    chan_def = &X : 6808.40 MHz : L : 32.000 MHz : &Ch42 : &BBC42 : &L_cal;\n")
        of.write("    chan_def = &X : 6744.40 MHz : L : 32.000 MHz : &Ch43 : &BBC43 : &L_cal;\n")
        of.write("    chan_def = &X : 6680.40 MHz : L : 32.000 MHz : &Ch44 : &BBC44 : &L_cal;\n")
        of.write("    chan_def = &X : 6584.40 MHz : L : 32.000 MHz : &Ch45 : &BBC45 : &L_cal;\n")
        of.write("    chan_def = &X : 6456.40 MHz : L : 32.000 MHz : &Ch46 : &BBC46 : &L_cal;\n")
        of.write("    chan_def = &X : 6424.40 MHz : L : 32.000 MHz : &Ch47 : &BBC47 : &L_cal;\n")
        of.write("    chan_def = &X : 6392.40 MHz : L : 32.000 MHz : &Ch48 : &BBC48 : &L_cal;\n")
        of.write("    chan_def = &X : 10680.40 MHz : L : 32.000 MHz : &Ch49 : &BBC49 : &L_cal;\n")
        of.write("    chan_def = &X : 10648.40 MHz : L : 32.000 MHz : &Ch50 : &BBC50 : &L_cal;\n")
        of.write("    chan_def = &X : 10584.40 MHz : L : 32.000 MHz : &Ch51 : &BBC51 : &L_cal;\n")
        of.write("    chan_def = &X : 10520.40 MHz : L : 32.000 MHz : &Ch52 : &BBC52 : &L_cal;\n")
        of.write("    chan_def = &X : 10424.40 MHz : L : 32.000 MHz : &Ch53 : &BBC53 : &L_cal;\n")
        of.write("    chan_def = &X : 10296.40 MHz : L : 32.000 MHz : &Ch54 : &BBC54 : &L_cal;\n")
        of.write("    chan_def = &X : 10264.40 MHz : L : 32.000 MHz : &Ch55 : &BBC55 : &L_cal;\n")
        of.write("    chan_def = &X : 10232.40 MHz : L : 32.000 MHz : &Ch56 : &BBC56 : &L_cal;\n")
        of.write("    chan_def = &X : 10680.40 MHz : L : 32.000 MHz : &Ch57 : &BBC57 : &L_cal;\n")
        of.write("    chan_def = &X : 10648.40 MHz : L : 32.000 MHz : &Ch58 : &BBC58 : &L_cal;\n")
        of.write("    chan_def = &X : 10584.40 MHz : L : 32.000 MHz : &Ch59 : &BBC59 : &L_cal;\n")
        of.write("    chan_def = &X : 10520.40 MHz : L : 32.000 MHz : &Ch60 : &BBC60 : &L_cal;\n")
        of.write("    chan_def = &X : 10424.40 MHz : L : 32.000 MHz : &Ch61 : &BBC61 : &L_cal;\n")
        of.write("    chan_def = &X : 10296.40 MHz : L : 32.000 MHz : &Ch62 : &BBC62 : &L_cal;\n")
        of.write("    chan_def = &X : 10264.40 MHz : L : 32.000 MHz : &Ch63 : &BBC63 : &L_cal;\n")
        of.write("    chan_def = &X : 10232.40 MHz : L : 32.000 MHz : &Ch64 : &BBC64 : &L_cal;\n")
        of.write("    sample_rate = 64.0 Ms/sec;\n")
        of.write("  enddef;\n")
    elif setup == "on1323":
        of.write("def FREQ_20m;\n")
        of.write("    chan_def = &X :  8099.99 MHz : U : 32.000 MHz : &CH01 : &BBC01 : &U_cal;\n")
        of.write("    chan_def = &X :  8139.99 MHz : U : 32.000 MHz : &CH02 : &BBC02 : &U_cal;\n")
        of.write("    chan_def = &X :  8384.99 MHz : U : 32.000 MHz : &CH03 : &BBC03 : &U_cal;\n")
        of.write("    chan_def = &X :  8544.99 MHz : U : 32.000 MHz : &CH04 : &BBC04 : &U_cal;\n")
        of.write("    chan_def = &X :  8764.99 MHz : U : 32.000 MHz : &CH05 : &BBC05 : &U_cal;\n")
        of.write("    chan_def = &X :  8884.99 MHz : U : 32.000 MHz : &CH06 : &BBC06 : &U_cal;\n")
        of.write("    chan_def = &X :  8924.99 MHz : U : 32.000 MHz : &CH07 : &BBC07 : &U_cal;\n")
        of.write("    chan_def = &X :  8964.99 MHz : U : 32.000 MHz : &CH08 : &BBC08 : &U_cal;\n")
        of.write("    sample_rate = 64.00 Ms/sec;\n")
        of.write("enddef;\n")
        of.write("def FREQ_OTT;\n")
        of.write("    chan_def = &X :  8996.99 MHz : L : 32.000 MHz : &CH01 : &BBC01 : &U_cal;\n")
        of.write("    chan_def = &X :  8956.99 MHz : L : 32.000 MHz : &CH02 : &BBC02 : &U_cal;\n")
        of.write("    chan_def = &X :  8916.99 MHz : L : 32.000 MHz : &CH03 : &BBC03 : &U_cal;\n")
        of.write("    chan_def = &X :  8796.99 MHz : L : 32.000 MHz : &CH04 : &BBC04 : &U_cal;\n")
        of.write("    chan_def = &X :  8576.99 MHz : L : 32.000 MHz : &CH05 : &BBC05 : &U_cal;\n")
        of.write("    chan_def = &X :  8416.99 MHz : L : 32.000 MHz : &CH06 : &BBC06 : &U_cal;\n")
        of.write("    chan_def = &X :  8171.99 MHz : L : 32.000 MHz : &CH07 : &BBC07 : &U_cal;\n")
        of.write("    chan_def = &X :  8131.99 MHz : L : 32.000 MHz : &CH08 : &BBC08 : &U_cal;\n")
        of.write("    chan_def = &X :  8996.99 MHz : L : 32.000 MHz : &CH09 : &BBC09 : &U_cal;\n")
        of.write("    chan_def = &X :  8956.99 MHz : L : 32.000 MHz : &CH10 : &BBC10 : &U_cal;\n")
        of.write("    chan_def = &X :  8916.99 MHz : L : 32.000 MHz : &CH11 : &BBC11 : &U_cal;\n")
        of.write("    chan_def = &X :  8796.99 MHz : L : 32.000 MHz : &CH12 : &BBC12 : &U_cal;\n")
        of.write("    chan_def = &X :  8576.99 MHz : L : 32.000 MHz : &CH13 : &BBC13 : &U_cal;\n")
        of.write("    chan_def = &X :  8416.99 MHz : L : 32.000 MHz : &CH14 : &BBC14 : &U_cal;\n")
        of.write("    chan_def = &X :  8171.99 MHz : L : 32.000 MHz : &CH15 : &BBC15 : &U_cal;\n")
        of.write("    chan_def = &X :  8131.99 MHz : L : 32.000 MHz : &CH16 : &BBC16 : &U_cal;\n")
        of.write("    sample_rate = 64.0 Ms/sec;\n")
        of.write("enddef;\n")
    elif setup == "r11089":
        of.write("def FREQ_20m;\n")
        of.write("  chan_def = &X :  8212.99 MHz : U :  8.000 MHz : &CH01 : &BBC01 : &U_cal;\n")
        of.write("  chan_def = &X :  8252.99 MHz : U :  8.000 MHz : &CH02 : &BBC02 : &U_cal;\n")
        of.write("  chan_def = &X :  8352.99 MHz : U :  8.000 MHz : &CH03 : &BBC03 : &U_cal;\n")
        of.write("  chan_def = &X :  8512.99 MHz : U :  8.000 MHz : &CH04 : &BBC04 : &U_cal;\n")
        of.write("  chan_def = &X :  8732.99 MHz : U :  8.000 MHz : &CH05 : &BBC05 : &U_cal;\n")
        of.write("  chan_def = &X :  8852.99 MHz : U :  8.000 MHz : &CH06 : &BBC06 : &U_cal;\n")
        of.write("  chan_def = &X :  8912.99 MHz : U :  8.000 MHz : &CH07 : &BBC07 : &U_cal;\n")
        of.write("  chan_def = &X :  8932.99 MHz : U :  8.000 MHz : &CH08 : &BBC08 : &U_cal;\n")
        of.write("  chan_def = &X :  8212.99 MHz : L :  8.000 MHz : &CH09 : &BBC01 : &U_cal;\n")
        of.write("  chan_def = &X :  8932.99 MHz : L :  8.000 MHz : &CH10 : &BBC08 : &U_cal;\n")
        of.write("  chan_def = &S :  2225.99 MHz : U :  8.000 MHz : &CH11 : &BBC09 : &U_cal;\n")
        of.write("  chan_def = &S :  2245.99 MHz : U :  8.000 MHz : &CH12 : &BBC10 : &U_cal;\n")
        of.write("  chan_def = &S :  2265.99 MHz : U :  8.000 MHz : &CH13 : &BBC11 : &U_cal;\n")
        of.write("  chan_def = &S :  2295.99 MHz : U :  8.000 MHz : &CH14 : &BBC12 : &U_cal;\n")
        of.write("  chan_def = &S :  2345.99 MHz : U :  8.000 MHz : &CH15 : &BBC13 : &U_cal;\n")
        of.write("  chan_def = &S :  2365.99 MHz : U :  8.000 MHz : &CH16 : &BBC14 : &U_cal;\n")
        of.write("  sample_rate = 16.0 Ms/sec;\n")
        of.write("enddef;\n")
        of.write("def FREQ_OTT;\n")
        of.write("    chan_def = &X : 8952.99  MHz : L : 32.000 MHz : &CH01 : &BBC01 : &U_cal;\n")
        of.write("    chan_def = &X : 8932.99  MHz : L : 32.000 MHz : &CH02 : &BBC02 : &U_cal;\n")
        of.write("    chan_def = &X : 8872.99  MHz : L : 32.000 MHz : &CH03 : &BBC03 : &U_cal;\n")
        of.write("    chan_def = &X : 8752.99  MHz : L : 32.000 MHz : &CH04 : &BBC04 : &U_cal;\n")
        of.write("    chan_def = &X : 8532.99  MHz : L : 32.000 MHz : &CH05 : &BBC05 : &U_cal;\n")
        of.write("    chan_def = &X : 8372.99  MHz : L : 32.000 MHz : &CH06 : &BBC06 : &U_cal;\n")
        of.write("    chan_def = &X : 8272.99  MHz : L : 32.000 MHz : &CH07 : &BBC07 : &U_cal;\n")
        of.write("    chan_def = &X : 8232.99  MHz : L : 32.000 MHz : &CH08 : &BBC08 : &U_cal;\n")
        of.write("    chan_def = &X : 8952.99  MHz : L : 32.000 MHz : &CH09 : &BBC09 : &U_cal;\n")
        of.write("    chan_def = &X : 8932.99  MHz : L : 32.000 MHz : &CH10 : &BBC10 : &U_cal;\n")
        of.write("    chan_def = &X : 8872.99  MHz : L : 32.000 MHz : &CH11 : &BBC11 : &U_cal;\n")
        of.write("    chan_def = &X : 8752.99  MHz : L : 32.000 MHz : &CH12 : &BBC12 : &U_cal;\n")
        of.write("    chan_def = &X : 8532.99  MHz : L : 32.000 MHz : &CH13 : &BBC13 : &U_cal;\n")
        of.write("    chan_def = &X : 8372.99  MHz : L : 32.000 MHz : &CH14 : &BBC14 : &U_cal;\n")
        of.write("    chan_def = &X : 8272.99  MHz : L : 32.000 MHz : &CH15 : &BBC15 : &U_cal;\n")
        of.write("    chan_def = &X : 8232.99  MHz : L : 32.000 MHz : &CH16 : &BBC16 : &U_cal;\n")
        of.write("    sample_rate = 64.0 Ms/sec;\n")
        of.write("enddef;\n")
    elif setup == "rv157":
        of.write("def FREQ_20m;\n")
        of.write("  chan_def = &X :  8365.75 MHz : U : 16.000 MHz : &CH01 : &BBC03 : &U_cal;\n")
        of.write("  chan_def = &X :  8445.75 MHz : U : 16.000 MHz : &CH02 : &BBC04 : &U_cal;\n")
        of.write("  chan_def = &X :  8805.75 MHz : U : 16.000 MHz : &CH03 : &BBC05 : &U_cal;\n")
        of.write("  chan_def = &X :  8925.75 MHz : U : 16.000 MHz : &CH04 : &BBC06 : &U_cal;\n")
        of.write("  chan_def = &S :  2212.75 MHz : U : 16.000 MHz : &CH05 : &BBC09 : &U_cal;\n")
        of.write("  chan_def = &S :  2242.75 MHz : U : 16.000 MHz : &CH06 : &BBC10 : &U_cal;\n")
        of.write("  chan_def = &S :  2282.75 MHz : U : 16.000 MHz : &CH07 : &BBC13 : &U_cal;\n")
        of.write("  chan_def = &S :  2372.75 MHz : U : 16.000 MHz : &CH08 : &BBC14 : &U_cal;\n")
        of.write("  sample_rate = 32.0 Ms/sec;\n")
        of.write("enddef;\n")
        of.write("def FREQ_OTT;\n")
        of.write("*NOTE: We ignore 4 channels since PRC doubled the freqs, since rv157 is just 4x16 MHz for 20m\n")
        of.write("    chan_def = &X : 8949.75  MHz : L : 32.000 MHz : &CH01 : &BBC01 : &U_cal;\n")
        of.write("    chan_def = &X : 8829.75  MHz : L : 32.000 MHz : &CH02 : &BBC02 : &U_cal;\n")
        of.write("    chan_def = &X : 8469.75  MHz : L : 32.000 MHz : &CH03 : &BBC03 : &U_cal;\n")
        of.write("    chan_def = &X : 8389.75  MHz : L : 32.000 MHz : &CH04 : &BBC04 : &U_cal;\n")
        of.write("    chan_def = &X :    1.00  MHz : L : 32.000 MHz : &CH05 : &BBC05 : &U_cal;\n")
        of.write("    chan_def = &X :    2.00  MHz : L : 32.000 MHz : &CH06 : &BBC06 : &U_cal;\n")
        of.write("    chan_def = &X :    3.00  MHz : L : 32.000 MHz : &CH07 : &BBC07 : &U_cal;\n")
        of.write("    chan_def = &X :    4.00  MHz : L : 32.000 MHz : &CH08 : &BBC08 : &U_cal;\n")
        of.write("    chan_def = &X : 8949.75  MHz : L : 32.000 MHz : &CH09 : &BBC09 : &U_cal;\n")
        of.write("    chan_def = &X : 8829.75  MHz : L : 32.000 MHz : &CH10 : &BBC10 : &U_cal;\n")
        of.write("    chan_def = &X : 8469.75  MHz : L : 32.000 MHz : &CH11 : &BBC11 : &U_cal;\n")
        of.write("    chan_def = &X : 8389.75  MHz : L : 32.000 MHz : &CH12 : &BBC12 : &U_cal;\n")
        of.write("    chan_def = &X :    1.00  MHz : L : 32.000 MHz : &CH13 : &BBC13 : &U_cal;\n")
        of.write("    chan_def = &X :    2.00  MHz : L : 32.000 MHz : &CH14 : &BBC14 : &U_cal;\n")
        of.write("    chan_def = &X :    3.00  MHz : L : 32.000 MHz : &CH15 : &BBC15 : &U_cal;\n")
        of.write("    chan_def = &X :    4.00  MHz : L : 32.000 MHz : &CH16 : &BBC16 : &U_cal;\n")
        of.write("    sample_rate = 64.0 Ms/sec;\n")
        of.write("enddef;\n")

def fillif(of, setup):
    if setup=="VGOS":
        of.write("  def VGOS;\n")
        of.write("    if_def = &IF_1N : 1N : X :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_3N : 3N : Y :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
        of.write("  enddef;\n")
    elif setup=="on1323":
        of.write("  def OTT;\n")
        of.write("    if_def = &IF_1N : 1N : X :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_3N : 3N : Y :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
        of.write("  enddef;\n")
        of.write("  def IF_20m;\n")
        of.write("   if_def = &IF_A1 :  A1 : R : 8080.00 MHz : U : 1.00 MHz : 0.00 Hz; \n")
        of.write("   if_def = &IF_A1 :  A1 : R : 8080.00 MHz : U : 1.00 MHz : 0.00 Hz; \n")
        of.write("  enddef;\n")
    elif setup=="r11089":
        of.write("  def OTT;\n")
        of.write("    if_def = &IF_1N : 1N : X :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_3N : 3N : Y :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
        of.write("  enddef;\n")
        of.write("  def IF_20m;\n")
        of.write("    if_def = &IF_A1 : A1 : R :  8080.0 MHz : U : 1 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_B1 : B1 : R :  8080.0 MHz : U : 1 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_C1 : C1 : R :  2020.0 MHz : U : 1 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_D1 : D1 : R :  2020.0 MHz : U : 1 MHz : 0 Hz;\n")
        of.write("  enddef;\n")
    elif setup=="rv157":
        of.write("  def OTT;\n")
        of.write("    if_def = &IF_1N : 1N : X :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_3N : 3N : Y :  8080.0 MHz : U : 5 MHz : 0 Hz;\n")
        of.write("  enddef;\n")
        of.write("  def IF_20m;\n")
        of.write("    if_def = &IF_A1 : A1 : R :  8080.0 MHz : U : 1 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_B1 : B1 : R :  8080.0 MHz : U : 1 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_C1 : C1 : R :  2020.0 MHz : U : 1 MHz : 0 Hz;\n")
        of.write("    if_def = &IF_D1 : D1 : R :  2020.0 MHz : U : 1 MHz : 0 Hz;\n")
        of.write("  enddef;\n")

def getfslogs(exp, antennas):
    print("Getting FS logs...")
    if "Oe" in antennas:
        run(['scp','fulla:/usr2/log/'+exp+'oe.log', '.'])
    if "Ow" in antennas:
        run(['scp','freja:/usr2/log/'+exp+'ow.log', '.'])
    if "On" in antennas:
        run(['scp','fold:/usr2/log/'+exp+'on.log', '.'])
    if "Is" in antennas:
        os.system('curl --ssl-reqd -u anonymous:anonymous ftp://ivs.bkg.bund.de/pub/vlbi/ivsdata/aux/'+year+'/'+exp+'/'+exp+'is.log -o'+exp+'is.log')


def fillclock(of, fslog):
    print("Finding CLOCK values from " + fslog)
    peculiaroff = {"Ow": [6.183,"from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
                   "Oe": [6.211,"from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
                   "On": [1.6,"between 1.5 and 1.7; different DBBC2 lock-states?"],
                   "Is": [1.268,"from https://github.com/whi-llc/adjust/blob/files/data/bb_po_v1.1.dat"],
                   }
    vals = []
    times = []
    for l in open(fslog):
        if ("/gps-fmout/" in l ) or ("/gps-maser/" in l) or ("/gps-dbbcout2/" in l):
            ls = l.split("/")
            time = datetime.datetime.strptime(ls[0], "%Y.%j.%H:%M:%S.%f")
            val = -float(ls[2]) # negative, as fmout-gps is the "clock early" convention
            vals.append(val) # Seconds
            times.append(time)
        elif ("/fmout-gps/" in l ):
            ls = l.split("/")
            time = datetime.datetime.strptime(ls[0], "%Y.%j.%H:%M:%S.%f")
            val = float(ls[2]) # pos, as fmout-gps is the "clock early" convention
            vals.append(val) # Seconds
            times.append(time)
        elif ("!dbe_gps_offset?" in l ):
            ls = re.split(r"/|[?]0:|;",l.strip())
            time = datetime.datetime.strptime(ls[0], "%Y.%j.%H:%M:%S.%f")
            val = float(ls[3])
            vals.append(val) # Seconds
            times.append(time)
    vals = np.array(vals)
    times = np.array(times)
    
    # Filter outliers
    avg = np.average(vals)
    std = np.std(vals)
    diff = np.abs(vals-avg)
    cut = 10*std
    # Filtering should really be done first fitting once without filters, removing linear trend, then filter outliers. 
    # But this works well enough for Onsala big jumps as is.
    bad = np.where(diff>cut)
    vals = np.delete(vals, bad)
    times = np.delete(times,bad)
    
    x = mdates.date2num(times) # decimal days
    pf = np.polyfit(x, vals, 1)
    p = np.poly1d(pf)
    
    xx = np.linspace(x.min(), x.max(), 100)
    dd = mdates.num2date(xx)
    
    fn = os.path.basename(fslog)
    station = fn[-6:-5].upper()+fn[-5:-4].lower()
    
    refdate = datetime.datetime(dd[0].year, dd[0].month, dd[0].day) # Floor to midnight
    reftime = refdate.strftime("%Yy%jd%Hh%Mm%Ss") # Integer seconds; we don't need more precision
    
    # Get fitted clock, add peculiar offset
    pecoff = peculiaroff[station]
    refclock_nopecoff = p(mdates.date2num(refdate))
    refclock = refclock_nopecoff + pecoff[0]*1e-6
    rate = pf[0]/(24*3600) # convert to s/s
    of.write("*NOTE: Using peculiar offset {0} us for {1}. Make sure this is correct!\n".format(pecoff[0], station))
    of.write("*                  valid from           clock_early    clock_early_epoch        rate\n")
    of.write("def {:s};  clock_early = {:s} : {:.3f} usec : {:s} : {:.3f}e-12; enddef;\n".format(station,reftime,refclock*1e6,reftime,rate*1e12))
    
def fillEOP(of, start):
    print("Downloading EOPs...")
    os.system('EMAIL_ADDR=eskil.varenius@chalmers.se geteop.pl ' + start + ' 5')
    print("Writing EOP section...")
    for el in open("EOP.txt"):
        of.write(el)

def getvex(exp):
    print("Getting VEX files from FS, or SKD from FS and converting SKD to VEX...")
    vex = exp+".vex"
    # Clear any existing vexfile
    if os.path.exists(vex):
        os.remove(vex)
    
    for fs in ["fulla", "freja"]:
        if not os.path.exists(vex):
            # Look for vex file on FS computer
            run(['scp','{0}:/usr2/sched/'.format(fs)+vex, '.'])
        # If not vexfile exists, look for skd instead
        if not os.path.exists(vex):
            run(['scp','{0}:/usr2/sched/'.format(fs)+exp+'.skd', '.'])
            # Convert SKD to VEX
            p = run(['/opt/sked/bin/sked', exp+".skd"], stdout=PIPE, input='VEC '+vex+'\rq\r', encoding='ascii')
    os.system('cp {0}.vex {0}.vex.org.bkp'.format(exp))

def writezoomsection(vf,setup):
    if setup == "on1323":
        vf.write("ZOOM zoom\n")
        vf.write("{\n")
        vf.write("addZoomFreq = freq@8099.99/bw@32.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8139.99/bw@32.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8384.99/bw@32.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8544.99/bw@32.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8764.99/bw@32.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8884.99/bw@32.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8924.99/bw@32.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8964.99/bw@32.0/noparent@true\n")
        vf.write("}\n")
    elif setup == "r11089":
        vf.write("ZOOM zoom\n")
        vf.write("{\n")
        vf.write("addZoomFreq = freq@8212.99/bw@8.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8252.99/bw@8.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8352.99/bw@8.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8512.99/bw@8.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8732.99/bw@8.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8852.99/bw@8.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8912.99/bw@8.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8932.99/bw@8.0/noparent@true\n")
        vf.write("}\n")
    elif setup == "rv157":
        vf.write("ZOOM zoom\n")
        vf.write("{\n")
        vf.write("addZoomFreq = freq@8365.75/bw@16.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8445.75/bw@16.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8805.75/bw@16.0/noparent@true\n")
        vf.write("addZoomFreq = freq@8925.75/bw@16.0/noparent@true\n")
        vf.write("}\n")

def makev2d(exp, ants, setup):
    print("Making .v2d file for DiFX...")
    vf = open(exp+".v2d",'w')
    vf.write("vex = {0}.vex\n".format(exp))
    vf.write("antennas = {}\n".format(", ".join(ants)))
    vf.write("# Ensure we get cross-auto corrs, just in case (i.e. Oe X-pol correlated with Oe Y-pol)\n")
    vf.write("exhaustiveAutocorrs = true\n")
    vf.write("# Keep 2h of data as one job regardless of gaps\n")
    vf.write("maxGap = 7200\n")
    vf.write("#select single scan for fringefinding/test\n")
    vf.write("#mjdStart=2023y038d00h56m40s\n")
    vf.write("#mjdStop=2023y038d00h59m40s\n")
    vf.write("SETUP default\n")
    vf.write("{\n")
    vf.write(" tInt=1\n")
    vf.write(" # High res to be able to notch-filter RFI on Oe-Ow baseline\n")
    vf.write(" fftSpecRes=0.1 \n")
    vf.write(" specRes=0.1\n")
    if setup=="rv157":
        vf.write(" freqId=0,1,2,3,8,9,10,11,16,17,18,19\n")
    vf.write("}\n")
    vf.write("\n")
    for ant in ants:
        print("Writing v2d content for antenna " + ant + "...")
        if ant in ["Oe", "Ow"]:
            streams = []
            if setup == "VGOS":
                for i in range(8):
                    stream = "{0}{1}".format(ant.lower(),i)
                    streams.append(stream)
            else:
                # Assume OTT X-band only
                for i in range(6,8):
                    stream = "{0}{1}".format(ant.lower(),i)
                    streams.append(stream)
            for stream in streams:
                vf.write("DATASTREAM {0}\n".format(stream))
                vf.write("{\n")
                vf.write("  format = VDIF/8032/2\n")
                vf.write("  filelist = {0}.files\n".format(stream))
                vf.write("}\n")
            vf.write("ANTENNA {0}\n".format(ant.capitalize()))
            vf.write("{\n")
            vf.write(" datastreams = {0}\n".format(", ".join(streams)))
            vf.write(" sampling=REAL\n")
            vf.write(" phaseCalInt=5\n")
            vf.write(" toneSelection = all\n")
            if not setup=="VGOS":
                vf.write(" zoom=zoom\n")
            vf.write("}\n")
            vf.write("\n")
        elif ant == "On":
            vf.write("ANTENNA On\n")
            vf.write("{\n")
            vf.write(" filelist=on.files\n")
            vf.write(" sampling = REAL\n")
            vf.write(" format = VDIF/8032/2\n")
            vf.write(" #format = VDIF/8032/1\n")
            vf.write(" phaseCalInt = 1\n")
            vf.write(" zoom=zoom\n")
            vf.write("}\n")
        elif ant == "Is":
            vf.write("DATASTREAM is0\n")
            vf.write("{\n")
            vf.write("  format = VDIF/1312/2\n")
            vf.write("  filelist = is0.files\n")
            vf.write("}\n")
            vf.write("DATASTREAM is1\n")
            vf.write("{\n")
            vf.write("  format = VDIF/1312/2\n")
            vf.write("  filelist = is1.files\n")
            vf.write("}\n")
            vf.write("DATASTREAM is2\n")
            vf.write("{\n")
            vf.write("  format = VDIF/1312/2\n")
            vf.write("  filelist = is2.files\n")
            vf.write("}\n")
            vf.write("DATASTREAM is3\n")
            vf.write("{\n")
            vf.write("  format = VDIF/1312/2\n")
            vf.write("  filelist = is3.files\n")
            vf.write("}\n")
            vf.write("ANTENNA Is\n")
            vf.write("{\n")
            vf.write(" datastreams = is0, is1, is2, is3\n")
            vf.write(" sampling = REAL\n")
            vf.write(" toneSelection = all\n")
            vf.write(" phaseCalInt = 5\n")
            vf.write(" }\n")
    if not setup=="VGOS":
        writezoomsection(vf,setup)

def makedatascripts(exp, ants, dnodes, setup):
    print("Making data scripts to mount and index voltage data...")
    cwd = os.getcwd()
    for i, a in enumerate(ants):
        ant = a.lower()
        dn = dnodes[i].lower()
        datadir = "/mnt/corrdata/{}/{}_{}".format(dn, exp, ant)
        print("Antenna " + ant + " will get data from " + dn + ":/" + datadir)
        of = open("mountandlist.{0}.{1}.sh".format(ant, dn), "w")
        of.write("# THIS FILE WILL BE RUN ON {0}\n".format(dn.upper()))
        of.write("ssh {} 'fusermount -u {}'\n".format(dn, datadir))
        of.write("ssh {} 'mkdir -p {}'\n".format(dn, datadir))
        of.write("ssh {3} \"vbs_fs -R '/mnt/disk*' -I '{0}_{1}*' {2}\"\n".format(exp, ant, datadir, dn))
        of.write("echo 'Will index all data with vsum. May take a few hours...'\n")
        if not dn=="gyller":
            of.write("ssh {} 'sshfs oper@gyller:/mnt/raidz0 /mnt/raidz0/'\n".format(dn))
        if ant=="on":
            of.write("ssh {3} 'vsum -s {0}/{1}_on* > {2}/on.files'\n".format(datadir, exp, cwd, dn))
        elif ant in ["oe", "ow"]:
            if setup == "VGOS":
                nmin = 0
                nmax = 8
            else:
                # Assume OTT X-band only
                nmin = 6
                nmax = 8
            for datastream in range(nmin, nmax):
                of.write("ssh {5} 'vsum -s {0}/{1}_{3}*_{2} > {4}/{3}{2}.files'\n".format(datadir, exp, datastream, ant, cwd, dn))
        elif ant == "is":
            if setup == "VGOS":
                nmin = 0
                nmax = 4
            for datastream in range(nmin, nmax):
                of.write("ssh {5} 'vsum -s {0}/{1}_{3}*_{2} > {4}/{3}{2}.files'\n".format(datadir, exp, datastream, ant, cwd, dn))
        of.close()

def makeexfiles(hnode, dnodes, cnodes, cpuspern, antennas, setup):
    print("Writing ex.machines...")
    of = open("ex.machines", "w")
    # First write head node, one line
    of.write(hnode + "\n")
    # Then write datanodes, one line per stream. So 8 per VGOS, 2 for OTT X-band only, and 1 for On
    for (d, dn) in enumerate(dnodes):
        if antennas[d]=="On":
            nstream = 1
        elif antennas[d] in ["Oe", "Ow"]:
            if setup == "VGOS":
                nstream = 8
            else:
                # Assume OTT X-band only
                nstream = 2
        elif antennas[d]=="Is":
            nstream = 4
        for i in range(nstream):
            of.write(dn+"\n")
    #Finally write computing nodes, on line per node
    for cn in cnodes:
        of.write(cn+"\n")
    of.close()
    print("Writing ex.threads")
    of = open("ex.threads", "w")
    of.write("NUMBER OF CORES:    {}\n".format(len(cnodes)))
    for cpus in cpuspern:
        of.write(cpus+"\n")
    of.close()
    
def fixvex(exp, antennas, setup):
    print("Modifying VEX file with setups, tracks etc.")
    # Read all lines of VEX file
    invex = exp+".vex"
    vex = [l for l in open(invex)]
    keep = True
    of = open(exp+".vex","w")
    start = ""
    for line in vex:
        if line.startswith("$"):
            keep = True
        if keep:
            if "mode = " in line:
                if setup == "VGOS":
                    of.write("        mode = VGOS;\n")
                elif setup=="on1323":
                    of.write("        mode = on1323;\n")
                elif setup=="r11089":
                    of.write("        mode = r11089;\n")
                elif setup=="rv157":
                    of.write("        mode = rv157;\n")
            elif "station =" in line:
                if setup=="r11089" or setup=="rv157":
                    if "station = On" in line:
                       of.write(line)
                       of.write(line.replace("On", "Oe"))
                       of.write(line.replace("On", "Ow"))
                else:
                    of.write(line)
            else:
                of.write(line)
        if "$MODE;" in line:
            keep=False
            fillmode(of, setup, antennas)
        if "$BBC;" in line:
            keep=False
            fillbbc(of, setup)
        if "$FREQ;" in line:
            keep=False
            fillfreq(of, setup, antennas)
        if "$IF;" in line:
            keep=False
            fillif(of, setup)
        if "$TRACKS;" in line:
            keep=False
            filltracks(of, setup)
        if "$SITE;" in line:
            keep=False
            fillsite(of, antennas)
        if "$STATION;" in line:
            keep=False
            fillstation(of, antennas)
        if "$ANTENNA;" in line:
            keep=False
            fillantenna(of, antennas)
        if "start = " in line and start=="":
            year = line.split()[2][0:4]
            doy = str(int(line.split()[2][5:8])-2)
            start = year+"-"+doy
    fillEOP(of, start)
    print("Writing CLOCK section...")
    of.write("$CLOCK;\n")
    for ant in antennas:
        fillclock(of, exp+"{0}.log".format(ant.lower()))
    of.close()

def makecorrscript(exp):
    print("Making correlation script to be run to correlate the data...")
    of = open(exp+".correlate.sh", "w")
    of.write("# Prepare correlation files\n")
    of.write("vex2difx -v -v -v -d "+exp+".v2d\n")
    of.write("# Check ex.machines and ex.threads before running next command\n")
    os.system("wget https://raw.githubusercontent.com/varenius/oso/master/CORR/makemachines.py")
    of.write("python3 makemachines.py\n")
    of.write("# Ensure that the CalcServer is running: will restart if already exists\n")
    of.write("startCalcServer\n")
    of.write("# Run calcif2 for farfield delays\n")
    of.write("calcif2 *.calc\n")
    of.write("# SCRIPT FINISHED. Check the output. If all seems OK, start correlation (in a screen!) by running\n")
    of.write("startdifx -n -f *.input -v\n")
    of.close()

## SCRIPT STARTS HERE
exp = input("Please type experiment to prepare e.g. fm3031: ")
year = input("Please type the year this was observed (to get logfiles etc) e.g. 2023: ")
setups = ['VGOS', 'on1323', 'r11089', 'rv157']
print("Available frequency setups:")
for i, s in enumerate(setups):
    print(str(i) + ": "+s)
setup = setups[int(input("Please select frequency setup by number e.g. 2 : ").strip())]
antennas_raw = input("Please type antennas to include separated by space e.g. Oe Ow : ")
antennas = antennas_raw.strip().split()
antennas_unsort = [a.capitalize() for a in antennas]
datanodes_raw = input("Please type the respective machines where the data is located e.g. gyller skirner : ")
datanodes_unsort = datanodes_raw.strip().split()
# Put antennas and the respective machine in order so that antenna names are sorted alphabetically
# This is needed because the machines file generated need the datastream order to be the same as 
# antenna order, and antennas will be sorted alphabetically by DiFX by default
antennas = sorted(antennas_unsort)
datanodes = [x for _,x in sorted(zip(antennas_unsort,datanodes_unsort))]
headnode = input("Please type head node for correlation job e.g. gyller : ").strip().lower()
computingnodes_raw = input("Please type machines to use for actual correlation computation e.g. gyller skirner kare hjuke oldbogar : ")
computingnodes = computingnodes_raw.strip().split()
cpuspernode_raw = input("Please type number of CPUs to use per node e.g. 10 8 4 20 16 : ")
cpuspernode = cpuspernode_raw.strip().split()

print("You have selected: ")
print("Experiment: " + exp)
print("Year: " + year)
print("Freq. setup: " + setup)
print("Antennas: " + " ".join(antennas))
print("Datanodes: " + " ".join(datanodes))
print("Computingnodes: " + " ".join(computingnodes))
print("CPUS per node: " + " ".join(cpuspernode))
print("Head node: " + headnode)

ans = input("Will run preparation actions for experiment " + exp + ".\nNOTE: This may overwrite files in this directory - type 'yes' to proceed:")
if not ans.lower()=="yes":
    print("Did not get yes, aborting")
    sys.exit(1)

getfslogs(exp, antennas)
getvex(exp)
fixvex(exp, antennas, setup)
makev2d(exp, antennas, setup)
makedatascripts(exp, antennas, datanodes, setup)
makeexfiles(headnode, datanodes, computingnodes, cpuspernode, antennas, setup)
makecorrscript(exp)
