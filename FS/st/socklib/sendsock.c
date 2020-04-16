/*****************************************************************************
 *
 * FILE: sendsock.c
 *
 *   This is a simple program to send (and receive) messages over a socket
 *   using the 'socklib' library and protocol.
 *
 * HISTORY
 *
 * who          when           what
 * ---------    -----------    ----------------------------------------------
 * lerner       23 Mar 2011    Original version (using the CIMA sock.c
 *                             developed by Jeff Hagen)
 * lerner       28 Jan 2014    Added use of 'sock_seterror'
 * lerner        6 Jul 2015    Added use of 'sock_allowed'
 *
 *****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <signal.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include "socklib.h"



void socklib_error(char *format, char *string) {

  char line[512];

  snprintf(line, sizeof(line), format, string);
  printf("socklib ERROR - %s\n", line);
}



int main(int argc, char *argv[]) {

  struct SOCK *to;
  char *to_name, *from_name;
  char *message;
  int len, timeout;
  int quit_flag = 0;
  int response_flag = 0;
  int slam_flag = 0;
  int one_reply_flag = 0;
  int time_flag = 1;
  int ct_flag = 8192;

  to_name = NULL;
  from_name = "ANONYMOUS";
  if ( argc <= 1 ) {
    printf("\nusage: %s [-s] [-r] [-1] [-t secs] [-f from_name] to_name\n",
	   argv[0]);
    printf("  to_name - the destination mailbox name\n");
    printf("  -f from_name - our own mailbox name\n");
    printf("  -r response is expected\n\n");
    printf("  -s slam it down one line at a time with out looking for a "
	   "response\n");
    printf("  -1 wait and quit after one reply has been received\n");
    printf("  -t secs wait a maximum of 'secs' seconds (default 1 sec)\n");
    printf("  -ct ct  size of buffer\n");
    exit(0);
  }

  while ( *++argv ) {
    if ( strcmp(*argv , "-f") == 0 )
      from_name = *++argv;
    else if ( strcmp(*argv , "-r") == 0 )
      response_flag = 1;
    else if ( strcmp(*argv , "-s") == 0 )
      slam_flag = 1;
    else if ( strcmp(*argv , "-1") == 0 )
      response_flag = one_reply_flag = 1;
    else if ( strcmp(*argv , "-t") == 0 )
      time_flag = atoi(*++argv);
    else if ( strcmp(*argv , "-ct") == 0 )
      ct_flag = atoi(*++argv);
    else
      to_name = *argv;
  }

  message = (char *) malloc(ct_flag);

  sock_seterror(socklib_error);

  sock_allowed("local 129.16.208. 192.165.6.");

  if ( from_name )
    sock_bind(from_name);

  sock_bufct(ct_flag);
  if ( to_name )
    to = sock_connect(to_name);

  if ( response_flag )
    timeout = time_flag;
  else
    timeout = 0;

  if ( slam_flag ) {
    while ( fgets(message, ct_flag, stdin) )
      sock_send(to, message);

  } else {
    while ( 1 ) {
      switch ( sock_sel(message, ct_flag, &len, NULL, 0, timeout,
			! quit_flag) ) {
        case 0:
          if ( ! sock_send(to, message) )
	    exit(1);
          break;
        case -1:
          if ( quit_flag )
            exit(1);
        case -2:
        case -3:
          if ( response_flag )
            quit_flag = 1;
          else
            exit(1);
          break;
        default:
	  printf("%s\n", message);
          if ( one_reply_flag )
            exit(0);
          break;
      }
    }
  }

  return(0);
}
