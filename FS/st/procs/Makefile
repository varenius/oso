###############################################################################
#
# FILE: Makefile
#
#    This file is the makefile for the Onsala-specific procedures.
#
# HISTORY
#
# who          when           what
# ---------    -----------    ----------------------------------------------
# lerner        6 Feb 2017    Original version
# lerner       18 Oct 2017    Replaced 'noisediode' with new procedures
# lerner       19 Feb 2018    Added 'cdms_baseline' and 'cdms_delay'
#
###############################################################################

all: ../bin/atten_pcal ../bin/cdms_baseline ../bin/cdms_delay ../bin/ncal_en ../bin/noise_force ../bin/noise_gate_en ../bin/pcal_en


../bin/atten_pcal: atten_pcal
	           cp atten_pcal ../bin

../bin/cdms_baseline: cdms_baseline
	              cp cdms_baseline ../bin

../bin/cdms_delay: cdms_delay
	           cp cdms_delay ../bin

../bin/ncal_en: ncal_en
	        cp ncal_en ../bin

../bin/noise_force: noise_force
	            cp noise_force ../bin

../bin/noise_gate_en: noise_gate_en
	              cp noise_gate_en ../bin

../bin/pcal_en: pcal_en
	        cp pcal_en ../bin

clean:
	rm -f *.o ../bin/atten_pcal ../bin/cdms_baseline ../bin/cdms_delay ../bin/ncal_en ../bin/noise_force ../bin/noise_gate_en ../bin/pcal_en
