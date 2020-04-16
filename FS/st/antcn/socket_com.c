/*****************************************************************************
 *
 * FILE: socket_com.c
 *
 *   This file contains internal routines used to communicate via normal
 *   TCP/IP sockets and it is used by 'antcn' to communicate with the OTTs.
 *
 * HISTORY
 *
 * who          when           what
 * ---------    -----------    ----------------------------------------------
 * lerner       25 Jan 2017    Original version (based on procedures by Lars
 *                             Petterson)
 *
 *****************************************************************************/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdarg.h>
#include <fcntl.h>
#include <errno.h>
#include <netdb.h>
#include <sys/ioctl.h>



/*****************************************************************************
 *
 *   Macros
 *
 *****************************************************************************/

#define CONNECT_TIMEOUT        5



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

int open_connection(int *fd, char *host, char *host_port);
int connect_timeout(int sock, struct sockaddr *addr, socklen_t addrlen,
		    int seconds);
int sendtimeout(int socket, char *buf, size_t buf_len, unsigned int timeout);
int recvtimeout(int socket, char *buf, size_t buf_len, unsigned int timeout);
void write_to_log(char *format, ...);



/*****************************************************************************
 *
 *   open_connection
 *
 *     open a socket connection --- code written by Lars Petterson with
 *     slight modifications
 *
 *****************************************************************************/

int open_connection(int *fd, char *host, char *host_port)
{
    struct addrinfo hints;
    struct addrinfo *result, *rp;
    int opts, s;

    memset(&hints, 0, sizeof(struct addrinfo));
    hints.ai_family = AF_UNSPEC;	/* Allow IPv4 or IPv6 */
    hints.ai_socktype = SOCK_STREAM;	/* Stream (TCP) socket */
    hints.ai_flags = 0;
    hints.ai_protocol = 0;	/* Any protocol */

    if ((s = getaddrinfo(host, host_port, &hints, &result))) {
        write_to_log("getaddrinfo() => %s", gai_strerror(s));
	return -1;
    }

    /* getaddrinfo() returns a list of address structures. Try each
     * address until we successfully connect(2). If socket(2) (or
     * connect(2)) fails, we (close the socket and) try the next
     * address.
     */
    for (rp = result; rp != NULL; rp = rp->ai_next) {

	*fd = socket(rp->ai_family, rp->ai_socktype, rp->ai_protocol);

	if (*fd == -1) {
	    write_to_log("socket() => %s", strerror(errno));
	    continue;
	}

	if (connect_timeout(*fd, rp->ai_addr, rp->ai_addrlen,
			    CONNECT_TIMEOUT) != -1) {
	    break;		/* Success */
	}

	write_to_log("connect() => %s", strerror(errno));

	close(*fd);
    }

    freeaddrinfo(result);	/* No longer needed */

    if (rp == NULL) {		/* No address succeeded */
	write_to_log("open_connection() => could not connect, no address "
		     "succeeded");
	*fd = -1;
	return -1;
    }

    if ((opts = fcntl(*fd, F_GETFL)) < 0) {
	write_to_log("fcntl(serv_sock, F_GETFL) => %s", strerror(errno));
	(void) close(*fd);
	return -1;
    }
    opts |= O_NONBLOCK;
    if (fcntl(*fd, F_SETFL, opts) < 0) {
	write_to_log("fcntl(serv_sock, F_SETFL, opts) => %s", strerror(errno));
	(void) close(*fd);
	return -1;
    }

    return 0;
}



/*****************************************************************************
 *
 *   connect_timeout
 *
 *     this is an alternative 'connect' routine which allows you to set
 *     a time-out instead of having to wait many minutes on non-existing
 *     addresses as with the standard 'connect'
 *
 *****************************************************************************/

int connect_timeout(int sock, struct sockaddr *addr, socklen_t addrlen,
		    int seconds) {

  fd_set write_fd;
  struct timeval timeout;
  unsigned long mode;
  int status;

/*  Set up a non-blocking socket  */

  mode = 1;

  status = ioctl(sock, FIONBIO, &mode);

  if ( status != 0 ) {
    write_to_log("ioctl failed with error: %ld   errno = %d", status, errno);
    return(-1);
  }

/*  Try the connect and return immediately if we get an error that is not
    EINPROGRESS  */

  status = connect(sock, addr, addrlen);

  if ( status == -1 && errno != EINPROGRESS )
    return(-1);

/*  Reset the socket to blocking mode  */

  mode = 0;

  status = ioctl(sock, FIONBIO, &mode);

  if ( status != 0 ) {
    write_to_log("ioctl failed with error: %ld   errno = %d", status, errno);
    return(-1);
  }

/*  Set up the time-out and the file descriptor list  */

  timeout.tv_sec = seconds;
  timeout.tv_usec = 0;

  FD_ZERO(&write_fd);
  FD_SET(sock, &write_fd);

/*  Check if the socket is ready  */

  status = select(FD_SETSIZE, NULL, &write_fd, NULL, &timeout);

  if ( FD_ISSET(sock, &write_fd) )
    return(0);

  return(-1);
}



/*****************************************************************************
 *
 *   sendtimeout
 *
 *     send a message to a socket with a time-out --- code written by
 *     Lars Petterson with slight modifications
 *
 *****************************************************************************/

/* --- send characters, but do not wait forever ---
 *
 * Returns:
 *  number of bytes sent on success
 *  0 if remote side has closed the connection
 *  -1 on error
 *  -2 on timeout
 *  -3 on select error
 */

int sendtimeout(int socket, char *buf, size_t buf_len, unsigned int timeout)
{
    fd_set fds;
    struct timeval tv;

    /* set up the file descriptor set */
    FD_ZERO(&fds);
    FD_SET(socket, &fds);

    /* set up the timeval struct for the timeout */
    tv.tv_sec = timeout;
    tv.tv_usec = 0;

    /* wait until timeout or ready to send */
    switch (select(socket + 1, NULL, &fds, NULL, &tv)) {
    case 0:
	/* timeout */
	return -2;
    case -1:
	/* error */
	return -3;
    default:
	/* data available */
	break;
    }
    return send(socket, buf, buf_len, 0);
}



/*****************************************************************************
 *
 *   recvtimeout
 *
 *     receive a message from a socket with a time-out --- code written by
 *     Lars Petterson with slight modifications
 *
 *****************************************************************************/

/* --- receive characters, but do not wait forever ---
 *
 * Returns:
 *  number of bytes received on success
 *  0 if remote side has closed the connection
 *  -1 on error
 *  -2 on timeout
 *  -3 on select error
 */

int recvtimeout(int socket, char *buf, size_t buf_len, unsigned int timeout)
{
    fd_set fds;
    struct timeval tv;

    /* set up the file descriptor set */
    FD_ZERO(&fds);
    FD_SET(socket, &fds);

    /* set up the timeval struct for the timeout */
    tv.tv_sec = timeout;
    tv.tv_usec = 0;

    /* wait until timeout or data received */
    switch (select(socket + 1, &fds, NULL, NULL, &tv)) {
    case 0:
	/* timeout */
	return -2;
    case -1:
	/* error */
	return -3;
    default:
	/* data available */
	break;
    }
    return recv(socket, buf, buf_len, 0);
}



/*****************************************************************************
 *
 *   write_to_log
 *
 *     write a message to a log file --- the arguments take the same syntax
 *     as 'printf' --- any trailing newline is removed automatically
 *
 *****************************************************************************/

void write_to_log(char *format, ...) {

  va_list var_args;
  char line[512];

/*  Set up the variable argument list  */

  va_start(var_args, format);

/*  Format the line  */

  vsnprintf(line, sizeof(line)-1, format, var_args);

/*  Clean up the variable argument list  */

  va_end(var_args);

/*  Remove any newline at the end of the message, if we have one  */

  if ( line[strlen(line) - 1] == '\n' )
    line[strlen(line) - 1] == '\0';

/*  Log the message  */

  logit(line, 0, NULL);
}
