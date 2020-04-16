/*****************************************************************************
 *
 * FILE: basic_stamp.c
 *
 *   Send a message and receive an answer from a basic stamp.
 *
 *   Call sequence:
 *
 *     basic_stamp "192.168.1.18 10001 2 117 ?"
 *
 * HISTORY
 *
 * who          when           what
 * ---------    -----------    ----------------------------------------------
 * lerner       13 Jun 2012    Original version
 * lerner        8 May 2014    Incresead DATA_MAX
 * lerner        1 Feb 2017    Allowed address 0
 *
 *****************************************************************************/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>



/*****************************************************************************
 *
 *   Macros
 *
 *****************************************************************************/

#define DATA_MIN           0
#define DATA_MAX       65535

#define STRING_END       '\0'
#define STX            '\002'
#define ETX            '\003'
#define EOT            '\004'
#define ENQ            '\005'
#define ACK            '\006'
#define NAK            '\025'

#define NONE               0
#define COMMAND            1
#define QUESTION           2

#define OK                 1
#define FAIL               0



/*****************************************************************************
 *
 *   Type definitions
 *
 *****************************************************************************/



/*****************************************************************************
 *
 *   Initial data
 *
 *****************************************************************************/

char Host[80];
int Host_port;



/*****************************************************************************
 *
 *   Global variables
 *
 *****************************************************************************/



/*****************************************************************************
 *
 *   Subroutine declarations
 *
 *****************************************************************************/

int send_and_receive(char *senddata, char *recvdata, int size);



/*****************************************************************************
 *
 *   main
 *
 *****************************************************************************/

int main(int argc, char *argv[], char *envp[]) {

  char command[256], reply[256];
  char address_string[10], data[80], character;
  char bcc = 0;
  char *p;
  int address, parameter, value, read_parameter;
  int type = NONE;

/*  Get the command from the command line  */

  if ( argc != 2 ) {
    printf("FAILED\n");
    exit(0);
  }

/*  Parse the command line  */

  if ( sscanf(argv[1], "%s %d %d %d %d", Host, &Host_port, &address,
	      &parameter, &value) == 5 ) {
    if ( address >= 0 && address < 100 && parameter > 0 && parameter < 10000 &&
	 value >= DATA_MIN && value <= DATA_MAX )
      type = COMMAND;
  } else if ( sscanf(argv[1], "%s %d %d %d %c", Host, &Host_port, &address,
		     &parameter, &character) == 5 )
    if ( address >= 0 && address < 100 && parameter > 0 && parameter < 10000 &&
	 character == '?' )
      type = QUESTION;

  if ( type == NONE ) {
    printf("FAILED\n");
    exit(0);
  }

/*  Set up the command  */

  sprintf(address_string, "%1d%1d%1d%1d", address/10, address/10, address%10,
	  address%10);

  if ( type == COMMAND ) {
    sprintf(data, "%04d%+d%c", parameter, value, ETX);
    p = data;
    while ( *p != STRING_END )
      bcc ^= *p++;
    if ( bcc < 32 )
      bcc += 32;
    sprintf(command, "%c%s%c%s%c", EOT, address_string, STX, data, bcc);
  } else
    sprintf(command, "%c%s%04d%c", EOT, address_string, parameter, ENQ);

/*  Send the message  */

  if ( send_and_receive(command, reply, sizeof(reply)) == OK ) {
    if ( type == COMMAND ) {
      if ( reply[0] == ACK ) {
	printf("OK\n");
	exit(0);
      }
    } else {
      if ( sscanf(&reply[1], "%d%d", &read_parameter, &value) == 2 ) {
	if ( parameter == read_parameter ) {
	  printf("%d\n", value);
	  exit(0);
	}
      }
    }
  }

  printf("FAILED\n");

  return(0);
}



/*****************************************************************************
 *
 *   send_and_receive
 *
 *     send a message and wait for the reply
 *
 *****************************************************************************/

int send_and_receive(char *senddata, char *recvdata, int size) {

  struct sockaddr_in address;
  fd_set rfds, wfds;
  struct timeval tv;
  int sockfd;

  int nwrite = -1;
  int nread = -1;
  int total_read = 0;

  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  address.sin_family = AF_INET;
  address.sin_addr.s_addr = inet_addr(Host);
  address.sin_port = htons(Host_port);

/*  Set up a time-out and connect to the socket  */

  tv.tv_sec = 1;
  tv.tv_usec = 0;

  if ( setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, (char *) &tv,
		  sizeof(tv)) < 0 )
    return(FAIL);

  if ( connect(sockfd, (struct sockaddr *) &address, sizeof(address)) == -1 )
    return(FAIL);

/*  Check that the socket is available for writing without hanging  */

//ZZZ Is this needed with the new time-out above???
  FD_ZERO(&wfds);
  FD_SET(sockfd, &wfds);

  tv.tv_sec = 0;
  tv.tv_usec = 500000;

  if ( select(sockfd+1, NULL, &wfds, NULL, &tv) <= 0 )
    return(FAIL);

  nwrite = write(sockfd, senddata, strlen(senddata) + 1);
  if ( nwrite != strlen(senddata) + 1 )
    return(FAIL);

  /* Watch socket fd to see when it has input. */
  FD_ZERO(&rfds);
  FD_SET(sockfd, &rfds);

  /* set timeout struct */
  tv.tv_sec = 0;
  tv.tv_usec = 500000;

  memset(recvdata, '\0', size);

  /* read a big data chunk */
  while ( select(sockfd+1, &rfds, NULL, NULL, &tv) > 0 && total_read < size ) {
    nread = read(sockfd, &recvdata[total_read], size - total_read);
    if ( nread > 0 )
      total_read += nread;
  /* set inter char timeout */
    tv.tv_sec = 0;
    tv.tv_usec = 50000;
  }

  if ( total_read == 0 )
    return(FAIL);

  if ( recvdata[0] != STX && recvdata[0] != ACK )
    return(FAIL);

  return(OK);
}
