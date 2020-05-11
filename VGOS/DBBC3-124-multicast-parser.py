import socket
import struct
import datetime

# Multicast configuration
mcast_port  = 25000 # Taken from DBBC3 firmware v124 parser.py example file
#TODO: Add mcast_port to DBBC3 config file
mcast_group = "224.0.0.19" # Set in DBBC3 config file
# IP of network interface to use on this computer.  If you have multiple
# interfaces, set this to one which is on the same network as your DBBC3
# Note: This is the computer IP where you run this script, NOT the DBBC3 IP
iface_ip    = "192.165.6.73" 

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
        '001l': 55.097,
        '001u': 58.259,
        '002l': 59.519,
        '002u': 63.846,
        '003l': 68.874,
        '003u': 69.884,
        '004l': 74.490,
        '004u': 77.330,
        '005l': 73.570,
        '005u': 71.341,
        '006l': 93.066,
        '006u': 102.982,
        '007l': 107.936,
        '007u': 123.178,
        '008l': 128.939,
        '008u': 129.922,
        '009l': 90.353,
        '009u': 89.489,
        '010l': 91.020,
        '010u': 92.282,
        '011l': 102.672,
        '011u': 115.908,
        '012l': 147.213,
        '012u': 161.739,
        '013l': 165.486,
        '013u': 167.849,
        '014l': 141.468,
        '014u': 120.471,
        '015l': 122.060,
        '015u': 129.665,
        '016l': 137.025,
        '016u': 182.402,
        '017l': 90.353,
        '017u': 88.360,
        '018l': 87.070,
        '018u': 90.255,
        '019l': 79.530,
        '019u': 83.085,
        '020l': 73.219,
        '020u': 75.438,
        '021l': 63.991,
        '021u': 66.697,
        '022l': 59.844,
        '022u': 60.914,
        '023l': 61.605,
        '023u': 60.236,
        '024l': 64.535,
        '024u': 62.309,
        '025l': 68.710,
        '025u': 66.699,
        '026l': 69.299,
        '026u': 70.145,
        '027l': 63.365,
        '027u': 60.713,
        '028l': 64.299,
        '028u': 57.984,
        '029l': 69.634,
        '029u': 74.198,
        '030l': 66.980,
        '030u': 68.105,
        '031l': 66.070,
        '031u': 67.539,
        '032l': 62.256,
        '032u': 66.381,
        '033l': 37.165,
        '033u': 39.049,
        '034l': 43.053,
        '034u': 37.697,
        '035l': 48.437,
        '035u': 45.066,
        '036l': 44.907,
        '036u': 46.289,
        '037l': 50.952,
        '037u': 51.020,
        '038l': 54.843,
        '038u': 50.696,
        '039l': 56.499,
        '039u': 55.625,
        '040l': 55.670,
        '040u': 56.845,
        '041l': 53.273,
        '041u': 53.919,
        '042l': 56.137,
        '042u': 53.955,
        '043l': 55.490,
        '043u': 58.222,
        '044l': 48.274,
        '044u': 51.645,
        '045l': 59.380,
        '045u': 56.243,
        '046l': 60.268,
        '046u': 56.932,
        '047l': 62.791,
        '047u': 60.881,
        '048l': 60.285,
        '048u': 63.311,
        '049l': 52.585,
        '049u': 47.426,
        '050l': 54.157,
        '050u': 53.424,
        '051l': 43.206,
        '051u': 48.114,
        '052l': 37.088,
        '052u': 38.248,
        '053l': 32.480,
        '053u': 32.968,
        '054l': 35.539,
        '054u': 36.439,
        '055l': 34.335,
        '055u': 35.586,
        '056l': 32.127,
        '056u': 34.245,
        '057l': 59.184,
        '057u': 57.488,
        '058l': 63.133,
        '058u': 67.606,
        '059l': 48.341,
        '059u': 52.685,
        '060l': 53.026,
        '060u': 41.516,
        '061l': 64.009,
        '061u': 64.317,
        '062l': 68.627,
        '062u': 70.067,
        '063l': 57.507,
        '063u': 67.834,
        '064l': 101.819,
        '064u': 46.681
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
            bbcInfo += ["Tsys: INF",]

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
