###############################################################################
#
# FILE: Makefile
#
#    This file is the makefile for the Onsala-specific antenna control code.
#
# HISTORY
#
# who          when           what
# ---------    -----------    ----------------------------------------------
# lerner       16 Jan 2017    Original version
#
###############################################################################

#
CFLAGS= 
LIBES = ../../fs/poclb/poclb.a ../../fs/clib/clib.a\
../../fs/rtelb/rtelb.a ../socklib/socklib.o -lm
#
OBJECTS = antcn.o socket_com.o
#
../bin/antcn: $(OBJECTS)
	cc  -o ../bin/antcn $(OBJECTS) $(LIBES)
	strip ../bin/antcn
#
antcn:
	rm -f ../bin/antcn
	make

clean:
	rm -f *.o ../bin/antcn
