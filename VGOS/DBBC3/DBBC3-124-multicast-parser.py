import socket
import struct
import datetime

# Multicast configuration
mcast_port  = 25000 # Taken from DBBC3 firmware v124 parser.py example file
#TODO: Add mcast_port to DBBC3 config file
mcast_group = "224.0.0.20" # Set in DBBC3 config file
# IP of network interface to use on this computer.  If you have multiple
# interfaces, set this to one which is on the same network as your DBBC3
# Note: This is the computer IP where you run this script, NOT the DBBC3 IP
iface_ip    = "192.165.6.72" 

# Create date-time-string without spaces or dots, do be used in log filename
starttime = datetime.datetime.utcnow().strftime('%Y-%m-%d--%H-%M-%S')
logfile = "MULTICAST_DBBC3_"+starttime + ".log"
# To print on screen instead of a logfile, set logfile="".
#logfile = ""

#LOs = [0,0,7700,7700,7700,7700,11600,11600]
#SBs = ['U', 'U', 'L', 'L', 'L', 'L', 'L', 'L',]

def getTcalJy(bbc):
    """ Return the Tcal value in Jansky for this BBC.  Note: does not read any
        info, just assumes it is always the same!. """
    bbcd={
    #BBC: Tcal[Jy]
          '001l': -141.948,
          '001u': -144.225,
          '002l': 84.224,
          '002u': 133.610,
          '003l': 209.342,
          '003u': 304.421,
          '004l': 216.392,
          '004u': 277.134,
          '005l': 25.113,
          '005u': 223.232,
          '006l': 14.509,
          '006u': 119.416,
          '007l': 124.876,
          '007u': 60.572,
          '008l': 49.458,
          '008u': -25.529,
          '009l': -795.494,
          '009u': 236.930,
          '010l': 260.435,
          '010u': 259.212,
          '011l': 341.939,
          '011u': 270.206,
          '012l': 225.410,
          '012u': 199.282,
          '013l': 340.693,
          '013u': 216.972,
          '014l': -204.667,
          '014u': 54.649,
          '015l': -8237.315,
          '015u': 264.678,
          '016l': 264.942,
          '016u': 140.481,
          '017l': 176.086,
          '017u': 154.637,
          '018l': 166.736,
          '018u': 178.133,
          '019l': 182.752,
          '019u': 178.067,
          '020l': 148.182,
          '020u': 156.499,
          '021l': 164.278,
          '021u': 191.800,
          '022l': 129.875,
          '022u': 149.372,
          '023l': 135.367,
          '023u': 130.053,
          '024l': 104.407,
          '024u': 135.281,
          '025l': 184.819,
          '025u': 171.009,
          '026l': 180.495,
          '026u': 184.486,
          '027l': 203.500,
          '027u': 182.275,
          '028l': 144.300,
          '028u': 184.189,
          '029l': 139.974,
          '029u': 182.902,
          '030l': 63.566,
          '030u': 94.791,
          '031l': 68.982,
          '031u': 62.169,
          '032l': 87.012,
          '032u': 74.845,
          '033l': 108.221,
          '033u': 100.751,
          '034l': 107.551,
          '034u': 110.036,
          '035l': 116.619,
          '035u': 105.581,
          '036l': 135.477,
          '036u': 140.049,
          '037l': 145.856,
          '037u': 128.146,
          '038l': 112.973,
          '038u': 116.928,
          '039l': 112.093,
          '039u': 114.813,
          '040l': 115.591,
          '040u': 112.131,
          '041l': 74.691,
          '041u': 119.632,
          '042l': 121.224,
          '042u': 102.983,
          '043l': 132.298,
          '043u': 119.593,
          '044l': 173.071,
          '044u': 158.550,
          '045l': 119.384,
          '045u': 102.848,
          '046l': 151.881,
          '046u': 152.969,
          '047l': 125.591,
          '047u': 153.303,
          '048l': 110.476,
          '048u': 120.747,
          '049l': 90.941,
          '049u': 91.500,
          '050l': 88.957,
          '050u': 90.335,
          '051l': 114.929,
          '051u': 103.562,
          '052l': 114.636,
          '052u': 118.240,
          '053l': 111.252,
          '053u': 106.671,
          '054l': 131.678,
          '054u': 131.122,
          '055l': 137.441,
          '055u': 132.237,
          '056l': 143.887,
          '056u': 140.016,
          '057l': 126.681,
          '057u': 127.400,
          '058l': 128.483,
          '058u': 127.240,
          '059l': 141.061,
          '059u': 118.104,
          '060l': 203.013,
          '060u': 181.659,
          '061l': 199.131,
          '061u': 191.884,
          '062l': 232.870,
          '062u': 227.839,
          '063l': 243.052,
          '063u': 235.199,
          '064l': 228.583,
          '064u': 245.356,
      }
    return bbcd[bbc]

def joinMcast(mcast_addr,port,if_ip):
    """
    Returns a live multicast socket
    mcast_addr is a dotted string format of the multicast group
    port is an integer of the UDP port you want to receive
    if_ip is a dotted string format of the interface you will use
    """
    
    #create a UDP socket
    mcastsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    #allow other sockets to bind this port too
    mcastsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    #explicitly join the multicast group on the interface specified
    mcastsock.setsockopt(socket.SOL_IP,socket.IP_ADD_MEMBERSHIP,
                socket.inet_aton(mcast_addr)+socket.inet_aton(if_ip))

    #finally bind the socket to start getting data into your socket
    mcastsock.bind((mcast_addr,port))

    return mcastsock

def logString(desc, msg):
    ls = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
    ls += " UTC: "
    ds = desc + ": "
    ls += ds.ljust(32)
    ls += msg
    
    if logfile=="":
        print(ls)
    else:
        with open(logfile, 'a') as of:
            of.write(ls + "\n")

# Connect to multicast
sock = joinMcast(mcast_group, mcast_port, iface_ip)

# Start loop to forever receiver and decode packets
# Values are extracted by stepping through the bitstream using
# an offset parameter, extracting the relevant bytes
# according to the Multicast Format Definition Document
while True:
    #print(sock.recv(1024))
    valueArray = sock.recv(16384)
    offset = 0
    versionString = valueArray[offset:offset+32].decode("utf-8") 
    logString("F/W VER", versionString.strip())
    offset = offset + 32
    
    # GCoMo values
    for i in range(0,8):
        shortArray = struct.unpack('HHH', valueArray[offset+i*8+2:offset+i*8+8])
        if valueArray[32+i*8] == 0:
            mode = "MAN"
        else:
            mode = "AGC"
        logString("GCOMO ["+str(i+1) + "] " + mode, str(shortArray))
            
    offset = offset + (8 * 8)
           
    # Downconverter Values        
    for i in range(0,8):
        shortArray = struct.unpack('HHHH', valueArray[offset+i*8:offset+i*8+8])
        logString("DOWNCONVERTER [" + str(i+1) + "]",  str(shortArray))
        
    offset = offset + (8 * 8)
        
    # ADB3L Values
    for i in range(0,8):
        powerArray = struct.unpack('IIII', valueArray[offset:offset+16])
        logString("ADBL ["+str(i+1)+"] POWER", str(powerArray))
        offset = offset + 16
        
        bstatArray_0 = struct.unpack('IIII', valueArray[offset:offset+16])
        logString("ADBL ["+str(i+1)+"] BSTAT0", str(bstatArray_0) + ", SUM:" + str(sum(bstatArray_0)))
        offset = offset + 16
        
        bstatArray_1 = struct.unpack('IIII', valueArray[offset:offset+16])
        logString("ADBL ["+str(i+1)+"] BSTAT1", str(bstatArray_1) + ", SUM:" + str(sum(bstatArray_1)))
        offset = offset + 16
        
        bstatArray_2 = struct.unpack('IIII', valueArray[offset:offset+16])
        logString("ADBL ["+str(i+1)+"] BSTAT2", str(bstatArray_2) + ", SUM:" + str(sum(bstatArray_2)))
        offset = offset + 16
        
        bstatArray_3 = struct.unpack('IIII', valueArray[offset:offset+16])
        logString("ADBL ["+str(i+1)+"] BSTAT3", str(bstatArray_3) + ", SUM:" + str(sum(bstatArray_3)))
        offset = offset + 16
        
        corrArray = struct.unpack('III', valueArray[offset:offset+12])
        logString("ADBL ["+str(i+1)+"] DCORR", str(corrArray))
        offset = offset + 12
        
    # Core3H Values    
    for i in range(0,8):
        # VDIF TIME (only included in DDC_U v125 or higher) 
        timeValue = struct.unpack('I', valueArray[offset:offset+4])
        #logString("CORE3H ["+str(i+1)+"] VDIF TIME", str(timeValue))
        offset = offset + 4
        
        ppsDelayValue = struct.unpack('I', valueArray[offset:offset+4])
        logString("CORE3H ["+str(i+1)+"] PPS_DELAY", str(ppsDelayValue))
        offset = offset + 4
        
        tpS0On = struct.unpack('I', valueArray[offset:offset+4])
        logString("CORE3H ["+str(i+1)+"] TP On S0", str(tpS0On))
        offset = offset + 4
        
        tpS0Off = struct.unpack('I', valueArray[offset:offset+4])
        logString("CORE3H ["+str(i+1)+"] TP Off S0", str(tpS0Off))
        offset = offset + 4
        
        # TSys for the full band for IFA (only included in DDC_U v125 or higher) 
        tsysValue = struct.unpack('I', valueArray[offset:offset+4])
        #logString("CORE3H ["+str(i+1)+"] TSYS", str(tsysValue))
        offset = offset + 4
        
        # SEFD for the full band for IFA (only included in DDC_U v125 or higher) 
        sefdValue = struct.unpack('I', valueArray[offset:offset+4])
        #logString("CORE3H ["+str(i+1)+"] SEFD", str(sefdValue))
        offset = offset + 4
        
    # BBC Values
    #for i in range(0,128):
    # We only use 64 BBCs for now
    for i in range(0,64):
        # Extract all values for this BBC
        bbcValues = struct.unpack('IBBBBIIIIHHHHII', valueArray[offset:offset+40])
        # Add list to be filled with values for logging
        bbcInfo = []

        # Extract and append basic info for logging
        bbcfreq = bbcValues[0]//524288
        bbcBw = bbcValues[1]
        bbcAgcVal = bbcValues[2]
        # Convert 0/1 AGC status to man/agc for readability
        if bbcAgcVal == 1:
            bbcAgc = "agc"
        else:
            bbcAgc= "man"
        bbcGainU = bbcValues[3]
        bbcGainL = bbcValues[4]
        bbcInfo += [bbcfreq, bbcBw, bbcAgc, bbcGainU, bbcGainL]
        
        # Extract and append Total power values on/off for logging. These can be used to calculate Tsys/SEFD
        # given a table of diode levels in Kelvin/Jansky
        bbcTPUOn = bbcValues[5]
        bbcTPLOn = bbcValues[6]
        bbcTPUOff = bbcValues[7]
        bbcTPLOff = bbcValues[8]
        bbcInfo += [bbcTPUOn, bbcTPLOn, bbcTPUOff, bbcTPLOff]

        try:
            # Calculate approximate Tsys from rxg-file Tcal-values
            bbc = str(i+1).rjust(3,"0")
            TcalL = getTcalJy(bbc+"l") # Jansky
            TcalU = getTcalJy(bbc+"u") # Jansky
            bbcSEFDU = - TcalU * bbcTPUOff / (bbcTPUOn-bbcTPUOff)
            bbcSEFDL = - TcalL * bbcTPLOff / (bbcTPLOn-bbcTPLOff)
            bbcInfo += ["SEFDU: " + str(round(bbcSEFDU)) + " Jy","SEFDL: " + str(round(bbcSEFDL)) + " Jy"]
        except ZeroDivisionError:
            bbcInfo += ["SEFDU: INF Jy","SEFDL: INF Jy"]

        # Extract and append Bit statitics for logging. N/A in DDC F/W ver <=124
        #bbcstat0 = bbcValues[9]
        #bbcstat1 = bbcValues[10]
        #bbcstat2 = bbcValues[11]
        #bbcstat3 = bbcValues[12]
        #bbcInfo += [bbcbstat0, bbcbstat1, bbcbstat2, bbcbstat3]

        # Extract and append Tsys/Sefd for logging. N/A in DDC F/W ver <=124
        #bbcTsysU = bbcValues[13]
        #bbcTsysL = bbcValues[14]
        #bbcSefdU = bbcValues[15]
        #bbcSefdL = bbcValues[16]
        #bbcinfo += [bbcTsysU, bbcTsysL, bbcSefdU, bbcSefdL]

        # Add together all extracted values into comma-separated string for logging/printing
        bbcString = ",".join([str(k) for k in bbcInfo])
        logString("BBC"+str(i+1).rjust(3,"0"), bbcString)
        
        # Jump to next BBC byte offset position
        offset = offset + 40
