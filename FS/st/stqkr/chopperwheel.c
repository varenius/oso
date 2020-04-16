#include <stdlib.h>
#include <math.h>

// http://www.alma.nrao.edu/memos/html-memos/alma170/node2.html

double atmcorr(double dbl, double Fsig, double Fima, double SBR, double Trec,
	       double Tair, double *Tsys, double *tau, double *rat);

double chopperwheel (load, sky, Temp, tpzero)
double load, sky, Temp, tpzero;
{
    char buf[256];
    double x, y;
    double Trec;
    double Tair;
    double Tload;
    double Cf;
    double dBload, Fsig, Fima, SBR;
    double Tsys, Od, rat;

/*
43 GHz Trc  =  50 K
22 GHz Trec =  25 K
86 GHz Trec =  90 K (check if 90 K should be used in May 2009!)
*/
    Trec = 25.0;		/* Kelvin */
    Tair = Temp + 273.0;	/* Weather station temperature in Kelvin */
    Tload = Tair + 2.0;		/* Load temperature in Kelvin */
    Cf = 1;			/* default ChopperWheel factor */

    x  = (load-tpzero)/(sky-tpzero);
    y  = 1 + ((x-1)*Trec + x*0.05*Tair - Tload)/(x*0.884*Tair);

   
    if (y > 0) {
       Cf = 1 + (1 - 0.93*Tair/Tload)*(1/y - 1) + 0.0526*(1 - Tair/Tload)/y;
       Od = -log(y);
// This can be calculated if we have the elevation
//        OdZ = Od*sin(elevation*DTR);
    }


    printf(" Trec=%f Tair=%f Tload=%f\n", Trec, Tair, Tload);
    printf(" Cf=%f load=%f sky=%f Temp=%f tpzero=%f\n", Cf, load, sky, Temp, tpzero);
    sprintf(buf, "Chopperwheel factor=%f   Optical depth at current elevation=%f", Cf, Od);
    logit(buf,0,NULL);
 

// This is the way the calculation is done on the 20m
// This was added by Lerner 2012-02-03

//ZZZ
    if ( 0 ) {
      if ( x > 0.0 )
	dBload = 10.0 * log10(x);
      else
 	dBload = 0.0;
//      Fsig = obsfreq/1000000000.0;
//      Fima = imagfreq/1000000000.0;
//      SBR = ???;
      Fsig = 86.4;
      Fima = 88.4;
      SBR = 10.0;
      Cf = atmcorr(dBload, Fsig, Fima, SBR, Trec, Tair, &Tsys, &Od, &rat);
    }


    return(Cf);
}
#ifdef DEBUGX
int main(int argc, char **argv)
{

    double Cf;
    double load, sky, Temp, tpzero;

    load = atof(argv[1]);
    sky  = atof(argv[2]);
    tpzero  = atof(argv[3]);
/*
    Temp  = atof(argv[3]);
*/
    Temp  = 6.85;

    Cf = chopperwheel (load, sky, Temp, tpzero);

    /*
    printf(" LOAD = %f,  SKY = %f, --->  CF = %f \n", load, sky, Cf);
    */
    printf(" %f\n", Cf);
}
#endif
