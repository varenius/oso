/* antcn.c
 *
 * This is the Onsala version of antcn (ANTenna CoNtrol program) adapted
 * for the OTT.
 * This version sends a log message whenever it is called.
 *
 * Lerner      7 Feb 2017     New version for OTT
 * Lerner      7 Jul 2017     Fixed a socket bug and added handling of name
 * Lerner     27 Sep 2017     Added check of 'Done' message and added wrapping
 *                            to uppercase for 'case 4' commands
 * Lerner      9 Jan 2018     Added 'SAT' command to 'case 4'
 * Lerner     19 Apr 2018     Added 'CLOSEST' keyword
 * HACK
 *
 */

/* Input */
/* IP(1) = mode
       0 = initialize LU
       1 = pointing (from SOURCE command)
       2 = offset (from RADECOFF, AZELOFF, or XYOFF commands)
       3 = on/off source status (from ONSOURCE command)
       4 = direct communications (from ANTENNA command)
       5 = on/off source status for pointing programs
       6 = reserved for future focus control
       7 = log tracking data (from TRACK command)
       8 = Station detectors, see /usr2/fs/misc/stndet.txt
       9 = Satellite traking, see /usr2/fs/misc/satellites.txt
      10 = termination mode, must return promptly
 11 - 99 = reserved for future use
100 - 32767 = for site specific use

   IP(2) = class number (mode 4 only)
   IP(3) = number of records in class (mode 4 only)
   IP(4) - not used
   IP(5) - not used
*/

/* Output */
/*  IP(1) = class with returned message
      (2) = number of records in class
      (3) = error number
            0 - ok
           -1 - illegal mode
           -2 - timeout
           -3 - wrong number of characters in response
           -4 - interface not set to remote
           -5 - error return from antenna
           -6 - error in pointing model initialization
            others as defined locally
      (4) = 2HAN for above errors, found in FSERR.CTL
          = 2HST for site defined errors, found in STERR.CTL
      (5) = not used
*/

/* Defined variables */
#define MINMODE 0  /* min,max modes for our operation */
#define MAXMODE 10

#define MAX_WAIT            4     /* time-out in seconds for socket messages */
#define MAX_GENERAL_WAIT   60     /* time-out in seconds for general messages */

#define SEND_TIMEOUT        3     /* time-out in seconds for OTT ACU messages */
#define RECEIVE_TIMEOUT     3     /* time-out in seconds for OTT ACU messages */
#define ACTION_TIMEOUT     60     /* time-out in seconds for OTT actions */

#define FS_PORT1            7     /* OTT ACU FS-socket port 1 code */
#define FS_PORT2            8     /* OTT ACU FS-socket port 2 code */
#define OTT1_PORT       "8050"    /* the OTT FS-socket port 1 */
#define OTT2_PORT       "8051"    /* the OTT FS-socket port 2 */

#define FROM_NAME_FREJA "VLBI_ANTENNA_FREJA" /* our own mailbox name */
#define FROM_NAME_FULLA "VLBI_ANTENNA_FULLA" /* our own mailbox name */
#define TO_NAME_OTT1    "EXECUTIVE_OTT1"     /* the destination mailbox name */
#define TO_NAME_OTT2    "EXECUTIVE_OTT2"     /* the destination mailbox name */

#define OTT1_ADDRESS    "192.165.6.70"       /* the OTT-1 address */
#define OTT2_ADDRESS    "192.165.6.71"       /* the OTT-2 address */

#define TELESCOPE_FILE     "/tmp/telescope_choice"
#define SELECT_TELESCOPE   "zenity --title='Antenna control destination' "   \
                           "--list --text='Select a destination for\nthe "   \
                           "antenna control program:' --radiolist "   \
                           "--height=280 --width=320 --column='Pick' "   \
                           "--column='Telescope' "   \
                           "FALSE 'OTT-1 (South) --- direct' "   \
                           "FALSE 'OTT-2 (North) --- direct' "   \
                           "FALSE 'OTT-1 (South) --- via BIFROST' "   \
                           "FALSE 'OTT-2 (North) --- via BIFROST' "   \
                           "FALSE 'None (FAKE connection)' >" TELESCOPE_FILE

#define TLE_DIR         "/usr2/st/tle/"      /* directory for TLE files */

#define UNKNOWN       0
#define TEL_OTT1      1
#define TEL_OTT2      2
#define TEL_NONE      3

#define BIFROST       1
#define OTT_ACU       2

#define FAIL          0
#define OK            1

#define QUIET         0
#define VERBOSE       1



/* Include files */

#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <errno.h>
#include <termio.h>
#include <signal.h>
#include <setjmp.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/time.h>

#include "../../fs/include/params.h" /* FS parameters            */
#include "../../fs/include/fs_types.h" /* FS header files        */
#include "../../fs/include/fscom.h"  /* FS shared mem. structure */
#include "../../fs/include/shm_addr.h" /* FS shared mem. pointer */
#include "rad2deg.h" /*Conversions from radians to degrees       */

#include "../socklib/socklib.h"  /* Include the socklib header file */

struct fscom *fs;

struct SOCK *sock;
int acu_socket = -1;

static int imode;
int dest_type = UNKNOWN;
char name[10];
char receive[256];
int fs_port = 0;
int ierr = 0;



/* Subroutines called */

void setup_ids();
void putpname();
void skd_run();
void logit();

int open_connection(int *fd, char *host, char *host_port);
int sendtimeout(int socket, char *buf, size_t buf_len, unsigned int timeout);
int recvtimeout(int socket, char *buf, size_t buf_len, unsigned int timeout);
void write_to_log(char *format, ...);



/* convert a string to uppercase */

void convert_to_uppercase(char *string) {

  char *p;

  p = string;

  while ( *p != '\0' ) {
    if ( *p >= 'a' && *p <= 'z' )
      *p -= 32;
    p++;
  }
}



/* socklib error handling */

void socklib_error(char *format, char *string) {

  char line[512], text[512];

  snprintf(line, sizeof(line), format, string);
  snprintf(text, sizeof(text), "socklib ERROR - %s", line);
  logit(text, 0, NULL);
}



/* socket communication */

int send_command(char *command, int timeout, int talkative) {

  struct timeval now;
  char message[300], reply[300];
  int tag, len, status, *p;

  /* Handle communication via BIFROST */

  if ( dest_type == BIFROST ) {

    if ( ! sock_send(sock, command) ) {
      ierr = -405;
      return(FAIL);
    }
    status = sock_seln(receive, sizeof(receive), &len, NULL, 0, timeout, 0);
    if ( status == -1 ) {
      ierr = -406;
      return(FAIL);
    } else if ( status == -3 ) {
      ierr = -407;
      return(FAIL);
    } else if ( status <= 0 ) {
      ierr = -408;
      return(FAIL);
    }

  /* Handle communication directly with an OTT ACU */

  } else {

    gettimeofday(&now, NULL);
    tag = ( (int) now.tv_sec % 1000 ) * 1000000 + (int) now.tv_usec;
    p = (int *) message;
    memset(message, '\0', sizeof(message));
    *p++ = 0x1DFCCF1A;
    *p++ = fs_port;
    *p++ = tag;
    strncpy(&message[12], command, strlen(command));
    p += 64;
    *p = 0xA1FCCFD1;
    if ( ( status = sendtimeout(acu_socket, message, 272,
				SEND_TIMEOUT) ) <= 0 ) {
      if ( status == -3 )
	write_to_log("ERROR send select error: %s!", strerror(errno));
      else if ( status == -2 )
	write_to_log("ERROR time-out on send!");
      else if ( status == -1 )
	write_to_log("ERROR send error: %s!", strerror(errno));
      else
	write_to_log("ERROR nothing sent!");
      write_to_log("This occurred when trying to send command '%s'", command);
      ierr = -405;
      close(acu_socket);
      acu_socket = -1;
      return(FAIL);
    }
    memset(reply, '\0', sizeof(reply));
    if ( ( status = recvtimeout(acu_socket, reply, sizeof(reply)-1,
				RECEIVE_TIMEOUT) ) <= 0 ) {
      if ( status == -3 ) {
	write_to_log("ERROR receive select error: %s!", strerror(errno));
	ierr = -407;
      } else if ( status == -2 ) {
	write_to_log("ERROR time-out on receive!");
	ierr = -406;
      } else if ( status == -1 ) {
	write_to_log("ERROR read error: %s!", strerror(errno));
	ierr = -408;
      } else {
	write_to_log("ERROR nothing read!");
	ierr = -408;
      }
      write_to_log("This occurred when waiting on reply for command '%s'",
		   command);
      close(acu_socket);
      acu_socket = -1;
      return(FAIL);
    }
    p = (int *) reply;
    //ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
    if ( p[2] != tag ) {
      memset(reply, '\0', sizeof(reply));
      if ( ( status = recvtimeout(acu_socket, reply, sizeof(reply)-1,
				  RECEIVE_TIMEOUT) ) <= 0 ) {
	if ( status == -3 ) {
	  write_to_log("ERROR-2 receive select error: %s!", strerror(errno));
	  ierr = -407;
	} else if ( status == -2 ) {
	  write_to_log("ERROR-2 time-out on receive!");
	  ierr = -406;
	} else if ( status == -1 ) {
	  write_to_log("ERROR-2 read error: %s!", strerror(errno));
	  ierr = -408;
	} else {
	  write_to_log("ERROR-2 nothing read!");
	  ierr = -408;
	}
	write_to_log("This occurred when waiting on reply for command '%s'",
		     command);
	close(acu_socket);
	acu_socket = -1;
	return(FAIL);
      }
    }

    strcpy(receive, &reply[12]);
    if ( p[1] != fs_port ) {
      write_to_log("ERROR the telescope control computer provided a reply from "
		   "another source (%d)!", p[1]);
      write_to_log("ERROR sent command '%s' and received reply '%s'!", command,
		   receive);
      ierr = -410;
      return(FAIL);
    }
    if ( p[2] != tag ) {
      write_to_log("ERROR the telescope control computer provided a reply for "
		   "another command!");
      write_to_log("ERROR sent command '%s' and received reply '%s'!", command,
		   receive);
      ierr = -411;
      return(FAIL);
    }
    if ( strncmp(receive, "Ignored", 7) == 0 ) {
      write_to_log("ERROR the telescope control computer ignored command '%s'!",
		   command);
      ierr = -410;
      return(FAIL);
    }
    if ( strncmp(receive, "Failed", 6) == 0 ) {
      write_to_log("ERROR command '%s' failed!", command);
      ierr = -409;
      return(FAIL);
    }
    if ( strncmp(receive, "Active", 6) == 0 ) {
      write_to_log("Waiting for command '%s' to finish ...", command);
      memset(reply, '\0', sizeof(reply));
      if ( ( status = recvtimeout(acu_socket, reply, sizeof(reply)-1,
				  ACTION_TIMEOUT) ) <= 0 ) {
	if ( status == -3 ) {
	  write_to_log("ERROR receive select error: %s!", strerror(errno));
	  ierr = -407;
	} else if ( status == -2 ) {
	  write_to_log("ERROR time-out on receive!");
	  ierr = -406;
	} else if ( status == -1 ) {
	  write_to_log("ERROR read error: %s!", strerror(errno));
	  ierr = -408;
	} else {
	  write_to_log("ERROR nothing read!");
	  ierr = -408;
	}
	write_to_log("This occurred when waiting on reply for command '%s'",
		     command);
	close(acu_socket);
	acu_socket = -1;
	return(FAIL);
      }
      strcpy(receive, &reply[12]);
    }
    if ( talkative != QUIET )
      write_to_log("Answer from %s: '%s'", name, receive);

  }

  return(OK);
}



/* get the TLE for a specified satellite */

int get_tle(char *string, int size) {

  FILE *file_id;
  char name[200], line[200], send[200], line1[200], line2[200];
  char satellite[80];
  char *p, *p1;
  int namelength;

  p = string;
  p += 3;

  while ( *++p == ' ' )
    ;

  strcpy(name, TLE_DIR);
  p1 = name + strlen(name);

  while ( *p != ' ' && *p != '\0' )
    *p1++ = *p++;
  *p1 = '\0';

  while ( *++p == ' ' )
    ;

  strncpy(satellite, p, sizeof(satellite));
  satellite[sizeof(satellite)-1] = '\0';

  if ( strlen(satellite) > 0 && satellite[strlen(satellite)-1] == ' ' )
    satellite[strlen(satellite)-1] = '\0';

  if ( strlen(name) == 0 || strlen(satellite) == 0 ) {
    write_to_log("ERROR no catalog or satellite name given!");
    return(FAIL);
  }

  if ( ( file_id = fopen(name, "r") ) == NULL ) {
    write_to_log("ERROR can't open catalog '%s' for reading!", name);
    return(FAIL);
  }

  namelength = strlen(satellite);

  while ( ! feof(file_id) ) {
    if ( fgets(line, sizeof(line), file_id) == NULL ) {
      write_to_log("ERROR unexpected EOF in satellite catalog!");
      fclose(file_id);
      return(FAIL);
    }
    if ( strstr(line, satellite) != NULL ) {
      if ( line[strlen(line)-1] == '\n' )
	line[strlen(line)-1] = '\0';
      if ( line[strlen(line)-1] == '\r' )
	line[strlen(line)-1] = '\0';
      while ( strlen(line) > 1 && line[strlen(line)-1] == ' ' )
	line[strlen(line)-1] = '\0';
      write_to_log("Found satellite '%s'", line);
      if ( fgets(line1, sizeof(line1), file_id) == NULL ) {
	write_to_log("ERROR unexpected EOF when trying to read line-1!");
	fclose(file_id);
	return(FAIL);
      }
      if ( line1[strlen(line1)-1] == '\n' )
	line1[strlen(line1)-1] = '\0';
      if ( line1[strlen(line1)-1] == '\r' )
	line1[strlen(line1)-1] = '\0';
      if ( fgets(line2, sizeof(line2), file_id) == NULL ) {
	write_to_log("ERROR unexpected EOF when trying to read line-2!");
	fclose(file_id);
	return(FAIL);
      }
      if ( line2[strlen(line2)-1] == '\n' )
	line2[strlen(line2)-1] = '\0';
      if ( line2[strlen(line2)-1] == '\r' )
	line2[strlen(line2)-1] = '\0';
      if ( strlen(line1) != 69 || strlen(line2) != 69 ) {
	write_to_log("ERROR line-1 or line-2 has the wrong length (%d & %d)!",
		     strlen(line1), strlen(line2));
	fclose(file_id);
	return(FAIL);
      }
      if ( dest_type != BIFROST ) {
	sprintf(send, "NAME %s", satellite);
	if ( ! send_command(send, MAX_WAIT, QUIET) ) {
	  write_to_log("ERROR sending comand '%s' failed!", send);
	  fclose(file_id);
	  return(FAIL);
	}
      }
      p = satellite;
      while ( *++p != '\0' )
	if ( *p == ' ' )
	  *p = '_';
      snprintf(string, size, "TRA TLE %s %s %s", satellite, line1, line2);
      fclose(file_id);
      return(OK);
    } else {
      fgets(line, sizeof(line), file_id);
      fgets(line, sizeof(line), file_id);
    }
  }

  fclose(file_id);

  write_to_log("ERROR can't find satellite '%s' in catalog '%s'!", satellite,
	       name);
  return(FAIL);
}



/* antcn main program starts here */
main()
{
    FILE *file_ID;

    int nrec, nrecr;
    int dum = 0;
    int destination = UNKNOWN;
    int r1, r2;
    int i,nchar;
    long ip[5], class, clasr;
    char buf[200], buf2[250];
    char send[200];

    char *from;
    char *dest_mailbox;
    char *p;
    char computer[80];
    char ott_address[20], ott_port[10];
    double ra, de, ra_sec, de_sec;
    double az, el, az_sec, el_sec;
    float epoch;
    int out_file;
    int status;
    int len;
    char ra_deg[20];
    char de_deg[20];

    memcpy(ip+3, "ST", 2);

    /* Set up IDs for shared memory, then assign the pointer to
       "fs", for readability.
    */
    setup_ids();
    fs = shm_addr;

    /* Put our program name where logit can find it. */

    putpname("antcn");

    /* Ask the observer which telescope we are going to use */

    while ( destination == UNKNOWN ) {
      system("rm -f "TELESCOPE_FILE);
      if ( system(SELECT_TELESCOPE) == 0 ) {
	if ( ( file_ID = fopen(TELESCOPE_FILE, "r") ) != NULL ) {
	  if ( fgets(buf, sizeof(buf), file_ID) != NULL ) {
	    if ( strncmp(buf, "OTT-1", 5) == 0 ) {
	      destination = TEL_OTT1;
	      dest_mailbox = TO_NAME_OTT1;
	      strcpy(ott_address, OTT1_ADDRESS);
	      strcpy(name, "OTT-1");
	      logit("antcn set to talk to OTT-1 (South)", 0, NULL);
	    } else if ( strncmp(buf, "OTT-2", 5) == 0 ) {
	      destination = TEL_OTT2;
	      dest_mailbox = TO_NAME_OTT2;
	      strcpy(ott_address, OTT2_ADDRESS);
	      strcpy(name, "OTT-2");
	      logit("antcn set to talk to OTT-2 (North)", 0, NULL);
	    } else if ( strncmp(buf, "None", 4) == 0 ) {
	      destination = TEL_NONE;
	      strcpy(name, "NONE");
	      logit("antcn set to FAKE telescope connection", 0, NULL);
	    }
	    if ( strstr(buf, "BIFROST") != NULL ) {
	      dest_type = BIFROST;
	      logit("antcn will communicate via BIFROST", 0, NULL);
	    } else {
	      dest_type = OTT_ACU;
	      if ( destination != TEL_NONE )
		logit("antcn will communicate directly with the OTT ACU", 0,
		      NULL);
	    }
	  }
	  fclose(file_ID);
	}
      }
    }

    /* Find out which mailbox we should be using */

    gethostname(computer, sizeof(computer));

    if ( strncmp(computer, "freja", 5) == 0 ) {
      logit("antcn run from 'freja'", 0, NULL);
      from = FROM_NAME_FREJA;
      fs_port = FS_PORT1;
      strcpy(ott_port, OTT1_PORT);
    } else if ( strncmp(computer, "fulla", 5) == 0 ) {
      logit("antcn run from 'fulla'", 0, NULL);
      from = FROM_NAME_FULLA;
      fs_port = FS_PORT2;
      strcpy(ott_port, OTT2_PORT);
    } else {
      logit("antcn run from a non-FS computer --- will SIMULATE antenna!!!", 0,
	    NULL);
      destination = TEL_NONE;
    }

    /* Set up the socket communication for BIFROST */

    if ( dest_type == BIFROST ) {

      sock_seterror(socklib_error);

/* ZZZ Check what is needed here */
      if ( destination == TEL_OTT1 )
	sock_allowed("129.16.208.220 129.16.208.221");
      else
	sock_allowed("129.16.208.220 129.16.208.221");

      if ( sock_bind(from) == 0 ) {
	ierr = -401;
	destination = TEL_NONE;
	goto End;
      }

      if ( ( sock = sock_connect(dest_mailbox) ) == NULL ) {
	ierr = -402;
	destination = TEL_NONE;
	goto End;
      }

    }

    /* Return to this point to wait until we are called again */

 Continue:
/* Per Bergman 2004-09-02 */
    strcpy(receive, " ");
/* Per Bergman 2004-09-02 */
    skd_wait("antcn", ip, (unsigned) 0);

    memcpy(ip+3, "ST", 2);

    /* Reset clasr and nrecr */
    clasr = 0;
    nrecr = 0;

    /* Reopen the socket communication if it is not open */

    if ( destination != TEL_NONE && dest_type == BIFROST && sock == NULL ) {
      if ( ( sock = sock_connect(dest_mailbox) ) == NULL ) {
	ierr = -403;
	goto End;
      }
    } else if ( destination != TEL_NONE && dest_type == OTT_ACU &&
	        acu_socket == -1 ) {
      if ( open_connection(&acu_socket, ott_address, ott_port) != 0 ) {
	ierr = -403;
	goto End;
      }
    }

    imode = ip[0];
    class = ip[1];
    nrec = ip[2];

    if ( imode < MINMODE || imode > MAXMODE && imode != 101 && imode != 102 ) {
      ierr = -404;
      goto End;
    }

    /* Flush the socket, in case there are old messages hanging around */

    if ( destination != TEL_NONE && dest_type == BIFROST ) {
      while ( sock_sel(receive, sizeof(receive), &len, NULL, 0, 10000, 0) > 0 )
        ;
    } else if ( destination != TEL_NONE && dest_type == OTT_ACU ) {
      while ( recvtimeout(acu_socket, receive, sizeof(receive), 0) > 0 )
	;
    }

    /* Handle each mode in a separate section */

    switch ( imode ) {

      case 0:             /* initialize */
	ierr = 0;
	fs->ionsor = 0;
	/*
	  strcpy(buf,"Initializing antenna interface");
	  logit(buf,0,NULL);
	*/
	break;


      case 1:             /* source= command */
	ierr = 0;
	fs->ionsor = 0;
	/*
	  strcpy(buf,"Commanding to a new source");
	  logit(buf,0,NULL);
	*/

	if ( destination == TEL_NONE )
	  break;

	ra = fs->ra50;
	de = fs->dec50;
	epoch = fs->ep1950;

	strcpy(ra_deg, angle(ra, HMS));
	strcpy(de_deg, angle(de, DMS));

	if ( dest_type == BIFROST )
	  sprintf(send, "TRA %.10s RA %.12s DE %.12s EPOCH %.1f",
                  fs->lsorna, ra_deg, de_deg, epoch);
	else
	  sprintf(send, "TRA RADEC RA %.6lf DEC %.6lf EPOCH %.0f CLOSEST",
	          ra * 180.0 / 3.141592654, de * 180.0 / 3.141592654, epoch);

	if ( ! send_command(send, MAX_WAIT, VERBOSE) )
	  goto End;

	if ( strcmp(receive, "OK") != 0 && strcmp(receive, "Ok") != 0 )
	  ierr = -409;

	if ( dest_type != BIFROST ) {
	  sprintf(send, "NAME %.10s", fs->lsorna);
	  p = send + strlen(send) - 1;
	  while ( *p == ' ' )
	    *p-- = '\0';
	  if ( ! send_command(send, MAX_WAIT, QUIET) )
	    goto End;
	}

	break;


      case 2:             /* offsets         */
	ierr = 0;
	fs->ionsor = 0;
	/*
	  strcpy(buf,"Commanding new offsets");
	  logit(buf,0,NULL);
	*/

	if ( destination == TEL_NONE )
	  break;

	ra = fs->RAOFF * 180.0 / 3.141592654;
	ra_sec = 3600.0 * ra;
	de = fs->DECOFF * 180.0 / 3.141592654;
	de_sec = 3600.0 * de;
	az = fs->AZOFF * 180.0 / 3.141592654;
	az_sec = 3600.0 * az;
	el = fs->ELOFF * 180.0 / 3.141592654;
	el_sec = 3600.0 * el;

	if ( ra != 0.0 || de != 0.0 )
	  if ( dest_type == BIFROST )
	    sprintf(send, "OFF RA %.3lf DE %.3lf", ra_sec, de_sec);
	  else
	    sprintf(send, "TRA OFF RA %.6lf DEC %.6lf", ra, de);
	else
	  if ( dest_type == BIFROST )
	    sprintf(send, "OFF AZR %.3lf ELR %.3lf", az_sec, el_sec);
	  else
	    sprintf(send, "TRA OFF AZR %.6lf ELR %.6lf", az, el);

	if ( ! send_command(send, MAX_WAIT, VERBOSE) )
	  goto End;

	if ( strcmp(receive, "OK") != 0 && strcmp(receive, "Ok") != 0 )
	  ierr = -409;

	break;


      case 3:        /* onsource command with error message */
	ierr = 0;
	fs->ionsor = 0;
	/*
	  strcpy(buf,"Checking onsource status, extended error logging");
	  logit(buf,0,NULL);
	*/

	if ( destination == TEL_NONE ) {
	  fs->ionsor = 1;
	  break;
	}

	if ( ! send_command("TR?", MAX_WAIT, VERBOSE) )
	  goto End;

	if ( strcmp(receive, "YES") == 0 || strcmp(receive, "Yes") == 0 )
	  fs->ionsor = 1; /*ionsor set to 1 if antenna is tracking*/
	else if ( strcmp(receive, "NO") == 0 || strcmp(receive, "No") == 0 )
	  fs->ionsor = 0; /*ionsor set to 0 if antenna is not tracking*/
	else {
	  ierr = -409;
	  fs->ionsor = 0;
	}

	break;


      case 4:            /* direct antenna= command */
	if ( class == 0 )
	  goto End;
	nrecr = 0;
	clasr = 0;
	for ( i = 0 ; i < nrec ; i++ ) {
	  ierr = 0;
	  strcpy(buf2, "Received message for antenna: ");
	  nchar = cls_rcv(class, buf, sizeof(buf), &r1, &r2, dum, dum);
	  strncpy(send, buf, nchar);
	  send[nchar] = '\0';
	  buf[nchar] = '\0';  /* make into a string */
	  strcat(buf2, buf);
	  logit(buf2, 0, NULL);

	  if ( strncmp(send, "SAT ", 4) == 0 ||
	       strncmp(send, "sat ", 4) == 0 ) {
            if ( ! get_tle(send, sizeof(send)) ) {
	      ierr = -412;
	      goto End;
	    }
	  }

	  convert_to_uppercase(send);
	  if ( destination != TEL_NONE ) {
            if ( ! send_command(send, MAX_GENERAL_WAIT, VERBOSE) )
	      goto End;
	    if ( strcmp(receive, "OK") != 0 && strcmp(receive, "Ok") != 0 &&
	         strcmp(receive, "YES") != 0 && strcmp(receive, "Yes") != 0 &&
	         strcmp(receive, "NO") != 0 && strcmp(receive, "No") != 0 &&
  	         strncmp(receive, "AZ ", 3) != 0 &&
	         strcmp(receive, "Done") != 0 ) {
	      ierr = -409;
	      goto End;
	    }
	  }

	  strcpy(buf, "ACK");
	  cls_snd(&clasr, buf, 3, dum, dum);
	  nrecr += 1;
	}

	break;


      case 5:    /* onsource command with no error logging */
	ierr = 0;
	fs->ionsor = 0;
	/*
	  strcpy(buf,"Checking onsource status, extended error logging");
	  logit(buf,0,NULL); */

	if ( destination == TEL_NONE ) {
	  fs->ionsor = 1;
	  break;
	}

	sleep(1);

	if ( ! send_command("TR?", MAX_WAIT, QUIET) )
	  goto End;

	if ( strcmp(receive, "YES") == 0 || strcmp(receive, "Yes") == 0 )
	  fs->ionsor = 1; /*ionsor set to 1 if antenna is tracking*/
	else if ( strcmp(receive, "NO") == 0 || strcmp(receive, "No") == 0 )
	  fs->ionsor = 0; /*ionsor set to 0 if antenna is not tracking*/
	else {
	  ierr = -409;
	  fs->ionsor = 0;
	}

	break;


      case 6:            /* reserved */
	ierr = -1;
	strcpy(buf,"TBD focus control");
	logit(buf,0,NULL);
	logit("Not implemented at Onsala",0,NULL);
	goto End;
	break;


      case 7:    /* onsource command with additional info  */
	ierr = 0;
	fs->ionsor = 0;
	/*
	  strcpy(buf,"Checking onsource status, extended error logging");
	  logit(buf,0,NULL);
	*/

	if ( destination == TEL_NONE ) {
	  fs->ionsor = 1;
	  break;
	}

	if ( ! send_command("TR?", MAX_WAIT, VERBOSE) )
	  goto End;

	if ( strcmp(receive, "YES") == 0 || strcmp(receive, "Yes") == 0 )
	  fs->ionsor = 1; /*ionsor set to 1 if antenna is tracking*/
	else if ( strcmp(receive, "NO") == 0 || strcmp(receive, "No") == 0 )
	  fs->ionsor = 0; /*ionsor set to 0 if antenna is not tracking*/
	else {
	  ierr = -409;
	  fs->ionsor = 0;
	}

	/* new code for handling azimuth/elevation read-back */

	if ( ! send_command("AN?", MAX_WAIT, VERBOSE) )
	  goto End;

	if ( sscanf(receive, "%lf %lf", &az, &el) == 2 ) {
	  sprintf(buf2, "Current az/el: %10.4lf %10.4lf", az, el);
	  logit(buf2, 0, NULL);
        } else if ( sscanf(receive, "AZ %lf EL %lf", &az, &el) == 2 ) {
	  sprintf(buf2, "Current az/el: %10.4lf %10.4lf", az, el);
	  logit(buf2, 0, NULL);
        } else {
	  sprintf(buf2, "Can't read az/el from string '%s'", receive);
	  logit(buf2, 0, NULL);
          ierr = -409;
        }

	break;


      case 8:
	ierr = 0;
	strcpy(buf,"Station dependent detectors access");
	logit(buf,0,NULL);
	logit("Not implemented at Onsala",0,NULL);
	break;


      case 9:
	ierr = 0;
	strcpy(buf,"Satellite tracking mode");
	logit(buf,0,NULL);
	logit("Not implemented at Onsala",0,NULL);
	break;


      case 10: /*normally triggered on FS termination if evironment variable
		 FS_ANTCN_TERMINATION has been defined */
	ierr = 0;
	strcpy(buf,"Termination mode");
	logit(buf,0,NULL);
	logit("Not implemented at Onsala",0,NULL);
	break;


      case 101:        /* local satellite tracking */
	ierr = 0;
	strcpy(buf,"Local satellite tracking mode");
	logit(buf,0,NULL);
	logit("Not implemented at Onsala",0,NULL);
	break;


      case 102:    /* read-out of telescope position for satellite tracking */
	ierr = 0;
	strcpy(buf,"Local satellite tracking mode");
	logit(buf,0,NULL);
	logit("Not implemented at Onsala",0,NULL);
	break;


      default:
	ierr = -404;

    }  /* end of switch */

 End:
    ip[0] = clasr;
    ip[1] = nrecr;
    ip[2] = ierr;
    ip[4] = 0;
    goto Continue;
}
