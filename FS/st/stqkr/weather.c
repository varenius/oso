/***********************************************************************
 *
 * file: weather.c
 *
 *
 * who      when         what
 * -------- ------------ -----------------------------------------------
 * lundahl  14 Jan 1992  Original form
 * lundahl  22 Mar 2002  Linux port
 * lundahl  22 Apr 2002  Added ymer for testing dopcal
 * lundahl  24 Mar 2009  Last verison by Lasse
 * lerner   20 Jan 2015  Switched to new server on port 6003 and remodeled
 *                       after Pegasus wx_data.c with addition of 0.8 mbar
 *                       correction to 25m station (G. Elgered)
 * lerner   16 Mar 2020  Switched IP-address
 *
 ***********************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <ctype.h>


#define STATION 1

#define CORRECTION 0.8  /* mbar */
#define OLD_LIMIT 300   /* seconds */

#define JD_ERR -1.0

#define TEMP_MIN -50.0
#define TEMP_MAX 50.0
#define TEMP_ERR -999.0

#define PRES_MIN 913.0
#define PRES_MAX 1113.0
#define PRES_ERR -999.0

#define RHUM_MIN 1.0
#define RHUM_MAX 99.0
#define RHUM_ERR -999.0

#define WIND_MIN 0.0
#define WIND_MAX 99.0
#define WIND_ERR -999.0

#define WDIR_MIN 0.0
#define WDIR_MAX 360.0
#define WDIR_ERR -999.0


void weather_(double *JD, double *T, double* Pr,
	      double *rH, double *Ws, double *Wd) {

    fd_set readfds;
    struct timeval timeout;
    socklen_t length;
    int sock, n;
    char recvline[512]; 
    static char msg[256];
    struct sockaddr_in serv_addr, from;
    double wxJD[3], wxT[3], wxPr[3], wxrH[3], wxWs[3], wxWd[3];
    time_t t, t1, t2;
    int n1 = 0, n2 = 1, n3 = 2;
    char *p;
    int i;

    if (STATION == 1) { n1 = 0; n2 = 1; n3 = 2; }  /* 1st, 2nd and 3rd choice */
    if (STATION == 2) { n1 = 1; n2 = 0; n3 = 2; }
    if (STATION == 3) { n1 = 2; n2 = 1; n3 = 0; }

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family      = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr("192.165.6.10"); /* wx.oso.chalmers.se */
    serv_addr.sin_port        = htons(6003);

    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
	fprintf(stderr, "can't open stream socket\n");
	return;
    }

    if (sendto(sock, "?", 1, MSG_DONTWAIT, (struct sockaddr *) &serv_addr,
	       sizeof(struct sockaddr_in)) < 0) {
      close(sock);
      fprintf(stderr, "failed to send '?' to wx\n");
      return;
    }

    timeout.tv_sec = 2; 
    timeout.tv_usec = 0;

    FD_ZERO(&readfds);
    FD_SET(sock, &readfds);

    if (select(sock+1, &readfds, NULL, NULL, &timeout) <= 0) {
      close(sock);
      fprintf(stderr, "failed waiting on reply from wx\n");
      return;
    }

    if (!FD_ISSET(sock, &readfds)) {
      close(sock);
      fprintf(stderr, "no reply from wx\n");
      return;
    }

    memset(recvline, 0, sizeof(recvline));
    length = sizeof(struct sockaddr_in);
    if (recvfrom(sock, recvline, sizeof(recvline), MSG_DONTWAIT,
		 (struct sockaddr *)&from, &length) < 0) {
      close(sock);
      fprintf(stderr, "failed to receive weather message\n");
      return;
    }
    close(sock);

    *JD = JD_ERR;
    *T = TEMP_ERR;
    *Pr = PRES_ERR;
    *rH = RHUM_ERR;
    *Ws = WIND_ERR;
    *Wd = WDIR_ERR;

    t2 = time(NULL);      /* t2 is actual time in seconds */

    p = strtok(recvline, "\n");
    for ( i = 0 ; i < 3 ; i++ ) {
      wxJD[i] = JD_ERR;
      wxT[i] = TEMP_ERR;
      wxPr[i] = PRES_ERR;
      wxrH[i] = RHUM_ERR;
      wxWs[i] = WIND_ERR;
      wxWd[i] = WDIR_ERR;
      sscanf(p, "%lf %lf %lf %lf %lf %lf", &wxJD[i], &wxT[i], &wxPr[i],
	     &wxrH[i], &wxWs[i], &wxWd[i]);
      if ( i == 1 && wxPr[1] != PRES_ERR )
	wxPr[1] += CORRECTION;
      t1 = (wxJD[i] - 40587.0) * 86400.0;   /* t1 is the wx readout time in seconds */
      t = t2 - t1;                          /* t is elapsed seconds since data was read */
      if ( t > OLD_LIMIT ) {
	wxJD[i] = JD_ERR;
	wxT[i] = TEMP_ERR;
	wxPr[i] = PRES_ERR;
	wxrH[i] = RHUM_ERR;
	wxWs[i] = WIND_ERR;
	wxWd[i] = WDIR_ERR;
      }
      p = strtok(NULL, "\n");
    }

    if (wxJD[n1] == JD_ERR)                           wxJD[n1] = wxJD[n2];
    if (wxJD[n1] == JD_ERR)                           wxJD[n1] = wxJD[n3];

    if (wxT[n1] == TEMP_ERR)                          wxT[n1] = wxT[n2];
    if (wxT[n1] == TEMP_ERR)                          wxT[n1] = wxT[n3];
    if (wxT[n1]  > TEMP_ERR && wxT[n1] < TEMP_MIN)    wxT[n1] = TEMP_MIN;
    if (wxT[n1]  > TEMP_ERR && wxT[n1] > TEMP_MAX)    wxT[n1] = TEMP_MAX;

    if (wxPr[n1] == PRES_ERR)                         wxPr[n1] = wxPr[n2];
    if (wxPr[n1] == PRES_ERR)                         wxPr[n1] = wxPr[n3];
    if (wxPr[n1]  > PRES_ERR && wxPr[n1] < PRES_MIN)  wxPr[n1] = PRES_MIN;
    if (wxPr[n1]  > PRES_ERR && wxPr[n1] > PRES_MAX)  wxPr[n1] = PRES_MAX;

    if (wxrH[n1] == RHUM_ERR)                         wxrH[n1] = wxrH[n2];
    if (wxrH[n1] == RHUM_ERR)                         wxrH[n1] = wxrH[n3];
    if (wxrH[n1]  > RHUM_ERR && wxrH[n1] < RHUM_MIN)  wxrH[n1] = RHUM_MIN;
    if (wxrH[n1]  > RHUM_ERR && wxrH[n1] > RHUM_MAX)  wxrH[n1] = RHUM_MAX;

    if (wxWs[n1] == WIND_ERR)                         wxWs[n1] = wxWs[n2];
    if (wxWs[n1] == WIND_ERR)                         wxWs[n1] = wxWs[n3];
    if (wxWs[n1]  > WIND_ERR && wxWs[n1] < WIND_MIN)  wxWs[n1] = WIND_MIN;
    if (wxWs[n1]  > WIND_ERR && wxWs[n1] > WIND_MAX)  wxWs[n1] = WIND_MAX;

    if (wxWd[n1] == WDIR_ERR)                         wxWd[n1] = wxWd[n2];
    if (wxWd[n1] == WDIR_ERR)                         wxWd[n1] = wxWd[n3];
    if (wxWd[n1]  > WDIR_ERR && wxWd[n1] < WDIR_MIN)  wxWd[n1] = WDIR_MIN;
    if (wxWd[n1]  > WDIR_ERR && wxWd[n1] > WDIR_MAX)  wxWd[n1] = WDIR_MAX;

    *JD = wxJD[n1];
    *T = wxT[n1];
    *Pr = wxPr[n1];
    *rH = wxrH[n1];
    *Ws = wxWs[n1];
    *Wd = wxWd[n1];
}
