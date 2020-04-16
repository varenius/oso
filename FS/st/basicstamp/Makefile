###############################################################################
#
# FILE: Makefile
#
#    This file is the makefile for the Onsala-specific basic stamp handling
#    code.
#
# HISTORY
#
# who          when           what
# ---------    -----------    ----------------------------------------------
# lerner       30 Jan 2015    Original version
#
###############################################################################

all: ../bin/basic_stamp

../bin/basic_stamp: basic_stamp.o
	            cc basic_stamp.o -lm -o ../bin/basic_stamp

basic_stamp.o: basic_stamp.c

clean:
	rm -f *.o ../bin/basic_stamp
