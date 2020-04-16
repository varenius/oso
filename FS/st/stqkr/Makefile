#
#CFLAGS= -g
#LIBES = ../stlib/stlib.a ../dbbc/dbbclib.a
LIBES = ../../fs/fslb/fslb.a ../../fs/lnfch/lnfch.a\
../../fs/newlb/newlb.a ../../fs/flib/flib.a ../../fs/fclib/fclib.a\
../../fs/clib/clib.a ../../fs/poclb/poclb.a ../../fs/rtelb/rtelb.a
#LIBES = ../bosslb/bosslb.a ../polb/polb.a ../fslb/fslb.a ../lnfch/lnfch.a\
#../newlb/newlb.a ../flib/flib.a ../fclib/fclib.a ../clib/clib.a\
#../poclb/poclb.a ../newlb/newlb.a ../fmpsee/fmpsee.a ../rtelb/rtelb.a
#
OBJECTS =\
stqkr.o tsys.o fc_get_tcal_fwhm1.o get_tcal_fwhm1.o chopperwheel.o\
atmcorr.o tplis.o tplisd.o tplisv.o tplisl.o tplisn.o fixtmp.o fixtmpdis.o weather.o wx.o fc_tpi_dbbc1.o tpi_dbbc1.o
#
../bin/stqkr: $(OBJECTS)
	fort77 -o ../bin/stqkr $(OBJECTS) $(LIBES) -lm
	strip ../bin/stqkr
#
stqkr:
	rm -f ../bin/stqkr
	make
