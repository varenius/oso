###############################################################################
#
# FILE: Makefile
#
#    This file is the makefile for the Onsala-specific socket handling code.
#
# HISTORY
#
# who          when           what
# ---------    -----------    ----------------------------------------------
# lerner       29 Apr 2011    Original version
#
###############################################################################

all: ../bin/sendsock

../bin/sendsock: sendsock.o socklib.o
	         cc sendsock.o socklib.o -lm -o ../bin/sendsock

sendsock.o: sendsock.c

socklib.o: socklib.c socklib.h

clean:
	rm -f *.o ../bin/sendsock
