#include <stdio.h>      /* declares sprintf */

#define HMS 0
#define DMS 1
#define DEG 2
#define PI 3.14159265

char *angle(radian, system)
double radian;
int system;
{
    static char w[] = "+000:00:00.0";
    long cs, d, m, s;
    char sign;
    
    /* check sign, save as character for later      */
    /* positive value of radian needed further down */	
    sign = '+';
    if (radian < 0.0) {
        sign = '-';
        radian = -radian;   
    }

    /* convert to 1/100 of arcsecs (variable cs)    */
    if (system == HMS) radian *= 12.0/PI;
    else               radian *= 180.0/PI;
    cs = (int)(radian*3600.0*10.0);
    d = cs/36000L;       /* hours or degrees        */
    m = (cs/600L)%60L;   /* mins or arcmins         */
    s = (cs/10L)%60L;    /* secs or arcsecs         */
    cs %= 10L;           /* keep only last digit    */
    if (sign == '-') d = -d;
    if (system != DEG) {
        sprintf(w,"%4d %02d %02d.%1d", d, m, s, cs);
        if (abs(d) < 100) w[1] = sign;
        if (abs(d) < 10)  w[2] = '0';
    } else {
        sprintf(w,"%12.7lf", radian);
    }
    return (w);
}

