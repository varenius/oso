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
starttime = datetime.datetime.utcnow().strftime('%Y-%m-%d--%H:%M:%S.%f')
logfile = "DBBC3_"+starttime + ".log"
# To print on screen instead of a logfile, set logfile="".
#logfile = ""

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

        #try:
        #    # Calculate approximate Tsys from rxg-file Tcal-values
        #    Tcal = getTcal() # Kelvin
        #    bbcTsys = - Tcal * bbcTPUOff / (bbcTPUOn-bbcTPUOff)
        #    bbcInfo += [" Approximate Tsys: " + str(round(bbcTsys)) + " K",]
        #except ZeroDivisionError:
        #    bbcInfo += ["Tsys: INF",]

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
        logString("BBC["+str(i+1) + "]", bbcString)
        
        # Jump to next BBC byte offset position
        offset = offset + 40
