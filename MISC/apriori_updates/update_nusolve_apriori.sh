EMAIL_ADDR=eskil.varenius@chalmers.se
NUSOLVE_APRIORI=/opt/nusolve/apriori_files/
#ECCDAT.ecc not updated automatically due to manual modifications (added dome numbers for OTT)
curl -u anonymous:$EMAIL_ADDR --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/vlbi/gsfc/ancillary/solve_apriori/usno_finals.erp > $NUSOLVE_APRIORI/usno_finals.erp
curl -u anonymous:$EMAIL_ADDR --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/vlbi/gsfc/ancillary/solve_apriori/usno500_finals.erp > $NUSOLVE_APRIORI/usno500_finals.erp
curl -u anonymous:$EMAIL_ADDR --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/vlbi/gsfc/ancillary/solve_apriori/ut1ls.dat > $NUSOLVE_APRIORI/ut1ls.dat
curl -u anonymous:$EMAIL_ADDR --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/vlbi/gsfc/ancillary/solve_apriori/blokq.c11.dat > $NUSOLVE_APRIORI/blokq.c11.dat
curl -u anonymous:$EMAIL_ADDR --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/vlbi/gsfc/ancillary/solve_apriori/source.names > $NUSOLVE_APRIORI/source.names
curl -u anonymous:$EMAIL_ADDR --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/vlbi/gsfc/ancillary/solve_apriori/tilt.dat > $NUSOLVE_APRIORI/tilt.dat
curl -u anonymous:$EMAIL_ADDR --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/vlbi/gsfc/ancillary/solve_apriori/IVS_SrcNamesTable.txt > $NUSOLVE_APRIORI/IVS_SrcNamesTable.txt

# Get all masterfiles
startyear=1979
endyear=$(date +%Y)
for i in $(seq $startyear $endyear)
  do
    yy=${i:2:2}
    echo $yy
    # Get masterfile for this year
    curl ftp://ivs.bkg.bund.de/pub/vlbi/ivscontrol/master$yy.txt > $NUSOLVE_APRIORI/masterfiles/master$yy.txt
    # Get INT-masterfile for this year, if it exists
    inturl="ftp://ivs.bkg.bund.de/pub/vlbi/ivscontrol/master$yy-int.txt"
    if curl --output /dev/null --silent --head --fail "$inturl"; then
      curl $inturl > $NUSOLVE_APRIORI/masterfiles/master$yy-int.txt
    else
      echo "URL does not exist: $inturl"
    fi
done
