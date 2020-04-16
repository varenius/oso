/********************************************************************************

    MATLAB function [CF,Tsys,tau,rat] = atmcorr(dbl,Fsig,Fima,SBR,Trec,Tair)

    % Calculates the correction factor of the chopper-wheel calibration
    % for a receiver with image band response
    %
    % INPUT PARAMETERS
    %  dbl: calibration [dB]
    % Fsig: signal frequency [GHz] 
    % Fima: image frequency [GHz] (Fima=Fsig+-8 GHz)
    % SBR: sideband rejection (SBR=Gain(image)/Gain(signal))
    %  or as dB ...
    % SBRdB: sideband rejection in dB (10log[Gain(signal)/Gain(Image)])
    % Trec: receiver temperature [K] (not corrected to SSB)
    % Tair: air temperature at ground level [K]
    %
    % OUTPUT PARAMETERS
    %   CF: calibration correction factor (Ta*=dV(sig)/dV(cal)*Tload*CF)
    % Tsys: corrected SSB system temperature in the Ta* scale
    %  tau: optical depth of the atmosphere in the signal band
    %  rat: ratio of optical depths in the image and signal bands
    %
    % CONSTANTS
    % loss=eta*exp(-TAUradome)
    % q=Tatm/Tair

    loss=0.9; q=0.95;

    % Read atmosphere attenuation file and calculate "rat"
    % dBatm tabulates the attenuation between 75 and 117 Ghz with a step of 100 MHz
    % The attenuation is tabulated in dB

    load dBatm.txt;
    dBa=dBatm; 
    Nsig=1+round(10*(Fsig-75.0));Nima=1+round(10*(Fima-75.0));
  % rat=10^((dBa(Nima)-dBa(Nsig))/10);
    rat=     dBa(Nima)/dBa(Nsig);

    % Calculate the optical depth of the atmosphere (signal band) by iterations
    
    denom=(1+SBR)+Trec/Tair;
    A=loss*(1-q)*(1+SBR)/denom;
    B=loss*q/denom;
    x=10^(0.1*dbl);
    C=(1-1/x-A)/B;

    taus=-0.5;diff=200;
    for n=1:400
        taus=taus+0.01;
        taui=rat*taus;
        dd=abs(C-exp(-taus)-SBR*exp(-taui));
        if dd<diff;diff=dd;tau=taus;end
    end

    % Calculate the correction factor CF and the SSB system temperature

    CF=(SBR+1)*((1-q)*exp(tau)+q*(1+SBR*exp(tau*(1-rat)))); 
    Tsys=Tair*CF/(x-1);  

    fprintf(1,'dB=%4.2f R=%4.2f Trec=%2.0f CF=%4.2f Tsys=%4.0f tau=%4.2f \n',dbl,SBR,Trec,CF,Tsys,tau);

********************************************************************************************************/
/********************************************************************************************************
   lundahl  2007-12-03	Translated into C-code
   lundahl  2008-02-01  Last version by Lasse
   lerner   2010-11-23  Decreased delta-tau in loop from 0.01 to 0.001
********************************************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include "dBatm.h"

#define noMAIN
#define SBRinDB

int Iround(double value)
{
    double round;
    if (value < 0) round = -floor(-value + 0.5);
    else	   round =  floor( value + 0.5);
    return (int)round;
}

#ifdef SBRinDB
double atmcorr(double dbl, double Fsig, double Fima, double SBRdB, double Trec, double Tair, double *Tsys, double *tau, double *rat)  
#else
double atmcorr(double dbl, double Fsig, double Fima, double SBR, double Trec, double Tair, double *Tsys, double *tau, double *rat)  
#endif
{
    int n;
    double loss=0.9;
    double q=0.95;
    double CF;

#ifdef SBRinDB
    double SBR = 1.0/(pow(10.0,SBRdB/10.0)); // use this line if SBRdB is used as input parameter to convert from SBRdB to SBR
#endif

    int Nsig=Iround(10*(Fsig-75.0));
    int Nima=Iround(10*(Fima-75.0));

    double denom=(1+SBR)+Trec/Tair;
    double A=loss*(1-q)*(1+SBR)/denom;
    double B=loss*q/denom;
    double x=pow(10.0,0.1*dbl);
    double C=(1-1/x-A)/B;

    double taui, dd;
    double taus=-0.5;
    double diff=200;

//  *rat=pow(10.0,(dBa[Nima]-dBa[Nsig])/10.0);
    *rat=          dBa[Nima]/dBa[Nsig];

    for (n=0; n<4000; n++) {
        taus=taus+0.001;
        taui=(*rat)*taus;
        dd=fabs(C-exp(-taus)-SBR*exp(-taui));
        if (dd<diff) {
	    diff=dd;
	    *tau=taus; 
 	}
    }
    CF=(SBR+1)*(1-q)*exp(*tau)+q*(1+SBR*exp(*tau*(1-*rat))); 
    *Tsys=Tair*CF/(x-1);  
    return CF;
}

#ifdef MAIN
//			testing: cc atmcorr.c -lm; ./a.out
int main(int argc, char **argv)
{
    double CF, Tsys, tau, rat;
    double dbl, Fsig, Fima, SBR, Trec, Tair;

    dbl = 1.83;		// test 1 
    Fsig = 115.27;
    Fima = 107.27;
#ifdef SBRinDB
    SBR = 3.979400;
#else
    SBR = 0.4;
#endif
    Trec = 30;
    Tair = 273;
    printf("INPUTS -> dB=%4.2f Fsig=%4.2f Fima=%4.2f SBR=%4.2f Trec=%4.0f Tair=%4.0f \n",dbl,Fsig,Fima,SBR,Trec,Tair);
    CF = atmcorr(dbl, Fsig, Fima, SBR, Trec, Tair,        &Tsys, &tau, &rat);  
    printf("C-CODE -> dB=%4.2f R=%4.2f Trec=%2.0f CF=%4.2f Tsys=%4.0f tau=%4.2f \n",dbl,SBR,Trec,CF,Tsys,tau);
    //printf("MATLAB -> dB=1.83 R=0.40 Trec=30 CF=2.43 Tsys=1267 tau=1.14\n\n"); ??? 

    dbl = 4.8; 		// test 2
    Fsig = 86.24;
    Fima = 94.24;
#ifdef SBRinDB
    SBR = 6.020600;
#else
    SBR = 0.25;
#endif
    Trec = 40;
    Tair = 280;
    printf("INPUTS -> dB=%4.2f Fsig=%4.2f Fima=%4.2f SBR=%4.2f Trec=%4.0f Tair=%4.0f \n",dbl,Fsig,Fima,SBR,Trec,Tair);
    CF = atmcorr(dbl, Fsig, Fima, SBR, Trec, Tair,        &Tsys, &tau, &rat);  
    printf("C-CODE -> dB=%4.2f R=%4.2f Trec=%2.0f CF=%4.2f Tsys=%4.0f tau=%4.2f \n",dbl,SBR,Trec,CF,Tsys,tau);
    //printf("MATLAB -> dB=4.80 R=0.25 Trec=40 CF=1.56 Tsys= 216 tau=0.20 \n\n") ???;
    return 0;
}
#endif
