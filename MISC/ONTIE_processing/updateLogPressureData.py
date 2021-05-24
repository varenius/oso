import glob, os, sys, string
import numpy, math
import string
import argparse
from shutil import copyfile


# heights [m] to be used for pressure corrections
# logfile pressure is from OSO weather station at 46.6m
deltaH = {}
deltaH['on']=59.3
deltaH['oe']=53.2
deltaH['ow']=53.2
deltaH['wx']=46.6


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Updating log files with new meteo data')
    parser.add_argument("-i", "--input",
                        action="store", dest="log_file_in",
                        type=str, required=True,
                        help="File that is to be processed")

    parser.add_argument("-o", "--output",
                        action="store", dest="log_file_out",
                        type=str, required=True,
                        help="File with the updated data")

    args = parser.parse_args()
    inputFile=args.log_file_in
    outputFile=args.log_file_out
    fileName=inputFile.rsplit("/",1)[1]
    fileNameNew=fileName.rsplit(".",1)[0]
    stationCode=fileNameNew[6:8]
    print("InputFile:", inputFile)
    print("OutputFile")
    print("StationCode:", stationCode)

    with open(inputFile, "rt") as fin:
        with open(outputFile, "wt") as fout:
            for line in fin:
                if ("/wx/" in line) and (",") in line:
                        print("OLDstring:", line)
                        pressure_old=float(line.rsplit(",")[1])
                        pressure_new=str(round(pressure_old * (1 - 0.0000226*(deltaH[stationCode]-deltaH['wx']))**5.225,1))
                        pressure_old=str(pressure_old)
                        old_str=str(line)
                        new_string=old_str.replace(pressure_old,pressure_new)
                        print("NEWstring:",new_string)
                        fout.write(new_string)
                else:
                    fout.write(line)
    print("The new logfile stored as ",outputFile,"...")
