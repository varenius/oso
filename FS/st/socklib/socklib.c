/*****************************************************************************
 *
 * FILE: socklib.c
 *
 *   This is the BIFROST socket library.
 *
 *   Any program using this library should include 'socklib.h'.
 *
 * HISTORY
 *
 * who          when           what
 * ---------    -----------    ----------------------------------------------
 * lerner       14 Oct 2009    Original version (using the CIMA socklib
 *                             developed by Jeff Hagen)
 * lerner       13 Jun 2012    Added 'sock_seln', added missing 'sin_family'
 *                             assignment in 'sock_bind' and corrected a number
 *                             of type bugs
 * lerner        6 Jul 2015    Added 'sock_domain' and 'sock_allowed', added
 *                             mailbox macro 'LOCAL' and removed 'isxview'
 *
 *****************************************************************************/

/* new one file version of library with open/close hooks */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
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
#include <arpa/inet.h>

#include "socklib.h"


#define DEFAULT_MAILBOX "/usr2/st/socklib/mailboxdefs"


/*
    Jeff's socket library

    -  is used for socket communication when VMS features
       and global memory are not required

    -  is simpler - without signals and the asynchronous maintainance
       of structures.

    -  Only one bound socket is permitted

    -  Binding must be done to receive messages

    Routines:
      sock_bind(name) - binds this process to name as defined in mailboxdefs
      sock_connect(name) - returns an SOCK structure that is passed to
        sock_send
      sock_send(s, message) - sends message to mailbox associated with s
        from sock_connect
      sock_write(s, data, n) - sends data to mailbox associated with s
        from sock_connect
      read_sock(s, message, ml, l) - reads a message
      sock_sel(message, ml, l, p, n, tim, rd) - blocks on connections and
        messages
        message is the buffer where a socket message will be put
        ml is the size of the 'message' buffer
        l is the length of message (returned);
        p is an array of file descriptors that sock_sel will select on
        n is the length of p;
        tim is a timeout in seconds
        rd true means that sock_sel will read stdin
        sock_sel returns:
          -1 if a timeout
          -2 if an error
          -3 if interrupted by a signal
          0 if standard in is ready for input
          or the file descriptor from 'p' that is ready.
          or the file descriptor of the socket that filled in message
      sock_seln(message, ml, l, p, n, tim, rd) - same as sock_sel, but strips
        the message of any trailing new line characters or white space
      sock_ssel(s, ns, message, ml, l, p, n, tim, rd) - same as sock_sel, but
        does not block on messages for the sockets in array, s (sock_connect
        return values)
        ns is the length of s
        rest of parameters same as sock_sel
      sock_close(name) - close opened connection - if NULL close all
      sock_name(last_msg()) - returns a status string pointing to the mbname
      sock_find(name) - returns handle for name
      sock_only(handle, message, ml, tim) - blocks only on handle or timeout
      sock_poll(handle, message, ml, tim, plen) - polls one socket and returns
        len
      sock_fd(handle) - returns a fd associated with handle
      sock_intr(flag) - sock_sel will return when select is interrupted if flag
        is true.
      sock_bufct(n) - set out-of-sync size normally 4096
      sock_domain(string) - specify the socket domain, i.e. which network
        the socket should be listening to, default is "any", use "local" to
        only accept connections from localhost (the computer needs to be
        specified as 'LOCAL' or 'localhost' in the mailbox file) or "n.n.n.n"
        to specify a certain network if the computer is connected to several
        networks (needs to be called BEFORE sock_bind) - note though that the
        latter can be a problem if you also expect calls via localhost
      sock_allowed(string) - a list of hosts or domains from which a call will
        be allowed, a maximum of 5 space-separated entries of the format
        "n.[n.[n.[n]]]" are allowed (e.g. "101.202.42. 127.0.0.1") as well as
        'any' or 'local[host]'

      window manager support is gained with calls to the open/close
      file descriptor

      sock_openclose(open, close);
      sock_seterror(err);
*/



struct BOUND sock_bound = { 0, NULL, NULL, { 0 }, 4096, 0,
			    { "any", "", "", "", "" }, "any", NULL, NULL,
			    standard_error };

/*
    sock_bind is used to establish a destination socket
      that is defined in the mailboxdefs file
      you should only call this once.
*/

struct BOUND *bs = &sock_bound;
static struct DEST sock_ano = { 0, "anonymous", "ANONYMOUS" };
struct SOCK sock_kbd = { 0, &sock_ano, 0, {0} };
struct SOCK *last_conn;

static int destflag = 0;
static struct DEST mailboxes[MAXDEST];

static struct DEST def_mailboxes[MAXDEST] = {
  { 0, "", "" }
};



static int readtm(int fd, char *buf, int len);
static void init_dest();



int sock_bind(char *mbname) {

  int on, count = 0, anon;
  struct hostent *hploc;
  char host[80];

  if ( ! bs->error )
    bs->error = standard_error;

  if ( bs->bind_fd > 0 )
    return(bs->bind_fd);

  anon = ( strcmp(mbname, "ANONYMOUS") == 0 );

  if ( anon ) {
    bs->dest = &sock_ano;
  } else if ( ( bs->dest = find_dest(mbname) ) == NULL ) {
    (*bs->error)("sock_bind: unknown mailbox '%s'", mbname);
    return(0);
  }

  gethostname(host, 80);
/*
  if ( strcmp(host, bs->dest->host) ) {
    (*bs->error)("sock_bind: %s is not localhost", bs->dest->host);
    return(0);
  }
*/

  if ( ! anon && ( hploc = gethostbyname(bs->dest->host) ) == NULL ) {
    (*bs->error)("sock_bind: can't find '%s'", bs->dest->host);
    return(0);
  }


  if ( ( bs->bind_fd = socket(AF_INET, SOCK_STREAM, 0) ) < 0 ) {
    (*bs->error)("sock_bind: 'socket' error --- %s", strerror(errno));
    return(0);
  }

  if ( fcntl(bs->bind_fd, F_SETFD,  FD_CLOEXEC) < 0 ) {
    (*bs->error)("sock_bind: 'fcntl' error --- %s", strerror(errno));
    return(0);
  }

  bs->sin.sin_family = AF_INET;
  bs->sin.sin_port = htons(bs->dest->dport);
  if ( strcmp(bs->domain, "any") == 0 )
    bs->sin.sin_addr.s_addr = htonl(INADDR_ANY);
  else if ( strcmp(bs->domain, "local") == 0 )
    bs->sin.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
  else
    bs->sin.sin_addr.s_addr = inet_addr(bs->domain);

  on = 1;
  setsockopt(bs->bind_fd, SOL_SOCKET, SO_REUSEADDR, (void *) &on, sizeof(on));

  while ( bind(bs->bind_fd, (void *) &bs->sin,
	       sizeof(struct sockaddr_in)) < 0 ) {
    (*bs->error)("sock_bind: 'bind' error --- %s --- retrying",
		 strerror(errno));
    if ( ++count > 12 ) {
      (*bs->error)("sock_bind: giving up trying to bind to socket", NULL);
      return(0);
    }
    sleep(5);
  }
  if ( count > 0 )
    (*bs->error)("sock_bind: finally bound", NULL);

  if ( listen(bs->bind_fd, 5) < 0 ) {
    (*bs->error)("sock_bind: 'listen' error --- %s", strerror(errno));
    return(0);
  }
  signal(SIGPIPE, SIG_IGN);
  if ( bs->open )
    (*bs->open)(NULL, bs->bind_fd);

  return(bs->bind_fd);
}



/*
    sock_connect returns a pointer to a structure that can be later passed to
    sock_send for sending a message
*/

struct SOCK *sock_connect(char *mbname) {

  struct SOCK *s;
  struct DEST *d;
  struct hostent *hp;
  int bflag = 1;
  extern struct DEST sock_ano;

  s = bs->head;

  if ( strcmp(mbname, "ANONYMOUS") ) {
    while ( s ) {
      if ( s->dest && strcmp(mbname, s->dest->dname) == 0 )
        return(s);
      s = s->next;
    }
    if ( ( d = find_dest(mbname) ) == NULL ) {
      (*bs->error)("sock_connect: unknown mailbox '%s'", mbname);
      return(NULL);
    }
  } else {
    while ( s ) {
      if ( s->dest && strcmp(mbname, s->dest->dname) == 0 && s->fd < 0 )
        break;
      s = s->next;
    }
    d = &sock_ano;
    bflag = 0;
  }

  if ( ! s ) {
    s = (struct SOCK *) malloc(sizeof(struct SOCK));
    bzero(s, sizeof(struct SOCK));
    s->fd = -1;
    s->dest = d;
    s->next = bs->head;
    bs->head = s;
  }

  if ( bflag ) { /* if anon then it wont ever connect */
    if ( ( hp = gethostbyname(s->dest->host) ) == NULL ) {
      (*bs->error)("sock_connect: can't find host '%s'", s->dest->host);
      return(NULL);
    }

    s->sin.sin_family = hp->h_addrtype;
    bcopy(hp->h_addr, &s->sin.sin_addr, hp->h_length);
    s->sin.sin_port = htons(s->dest->dport);
  }

  return(s);
}



int read_sock(struct SOCK *s, char *msg, int max_len, int *l) {

  unsigned long count, ct;
  uint32_t net;
  int n;

  last_conn = &sock_kbd;
  if ( ( n = read(s->fd, &net, sizeof(uint32_t)) ) > 0 ) {
    count = (unsigned long) ntohl(net);
    if ( count <= sock_bound.bufct ) {
      ct = count;
      while ( ( n = read(s->fd, &msg[count - ct], ct) ) < ct && n > 0 )
        ct -= n;
    } else if ( count >= max_len ) {
      (*bs->error)("read_sock: message too long for string", NULL);
    } else
      (*bs->error)("read_sock: read count out of sync", NULL);
  }

  *l = count;
  if ( n < 0 )
    (*bs->error)("read_sock: read error --- %s", strerror(errno));

  if ( n <= 0 || count > sock_bound.bufct || count >= max_len ) {
    if ( bs->close )
      (*bs->close)(s->fd);
    close(s->fd);
    s->fd = -1;
    return(-2);
  }
  msg[count] = '\0';
  last_conn = s;
  return(s->fd);
}



int sock_close(char *name) {

  struct SOCK *s, *p;

  if ( name ) { /* close name and de-queue */
    s = bs->head;
    p = NULL;
    while ( s ) {
      if ( s->dest && strcmp(name, s->dest->dname) == 0 )
        break;
      p = s;
      s = s->next;
    }
    if ( s ) {
      close(s->fd);
      if ( p )
        p->next = s->next;
      else
        bs->head = NULL;
      free(s);
    }
  } else { /* close all */
    s = bs->head;
    while ( s ) {
      close(s->fd);
      p = s->next;
      free(s);
      s = p;
    }
    close(bs->bind_fd);
    bs->bind_fd = -1;
    bs->dest = NULL;
  }

  return(0);
}



struct SOCK *last_msg() {

  return(last_conn);
}



char *sock_name(struct SOCK *handle) {

  return(handle ? handle->dest->dname : NULL);
}



int sock_fd(struct SOCK *handle) {

  return(handle ? handle->fd : -1);
}



int sock_bufct(int bufct) {

  if ( bufct )
    sock_bound.bufct = bufct;
  return(bufct);
}



struct SOCK *sock_find(char *mbname) {

  struct SOCK *s;

  s = bs->head;
  while ( s ) {
    if ( s->dest && strcmp(mbname, s->dest->dname) == 0 )
      return(s);
    s = s->next;
  }
  return(NULL);
}



struct SOCK *sock_findfd(int fd) {

  struct SOCK *s;

  s = bs->head;
  while ( s ) {
    if ( s->dest && s->fd == fd )
      return(s);
    s = s->next;
  }
  return(NULL);
}



void sock_intr(int flag) {

  sock_bound.interrupt = flag;
}



void sock_domain(char *domain) {

  if ( strlen(domain) < MAXNAME )
    strcpy(bs->domain, domain);
}



void sock_allowed(char *allowed_list) {

  char list[256];
  char *p;
  int i;

  if ( strlen(allowed_list) < sizeof(list) )
    strcpy(list, allowed_list);
  else
    return;

  strcpy(bs->allowed[0], "any");
  for ( i = 1 ; i < MAXALLOWED ; i++ )
    strcpy(bs->allowed[i], "");

  if ( ( p = strtok(list, ", \n") ) == NULL )
    return;

  if ( strlen(p) < MAXNAME ) {
    if ( strncmp(p, "local", 5) == 0 )
      strcpy(bs->allowed[0], "127.0.0.1");
    else
      strcpy(bs->allowed[0], p);
  }

  i = 0;

  while ( ( p = strtok(NULL, ", \n") ) != NULL && ++i < MAXALLOWED )
    if ( strlen(p) < MAXNAME ) {
      if ( strncmp(p, "local", 5) == 0 )
        strcpy(bs->allowed[i], "127.0.0.1");
      else
        strcpy(bs->allowed[i], p);
    }
}



/*
   blocks for a message on all bound sockets
     p is a pointer to an array of additional sockets to block on.
     n is the length of p.
      returns -1 on timeout.
              or the socket number on success
     timeout is in seconds
     the size of message is up to the caller
     returns without reading when the 'p' descriptors are detected
*/

int sock_sel(char *message, int max_len, int *l, int *p, int n, int tim,
	     int rd_in) {

  return(sock_ssel(NULL, 0, message, max_len, l, p, n, tim, rd_in));
}



/*
   same as 'sock_sel' but strips any trailing new-line characters or white space
*/

int sock_seln(char *message, int max_len, int *l, int *p, int n, int tim,
	      int rd_in) {

  int status, index;

  if ( ( status = sock_ssel(NULL, 0, message, max_len, l, p, n, tim,
			    rd_in) ) <= 0 )
    return(status);

  index = strlen(message) - 1;

  while ( ( message[index] == ' ' || message[index] == '\n' ) && index >= 0 )
    message[index--] = '\0';

  return(status);
}



/*
   blocks for a message on all bound sockets except those listed in ss.
     ss is a pointer to an array of sockets (sock_connect return values)
     ns is the length of ss
     p is a pointer to an array of additional sockets to block on.
     n is the length of p.
      returns -1 on timeout.
              or the socket number on success
     timeout is in seconds; if <0, does a poll only (returns 0 if nothing ready)
     the size of message is up to the caller
     returns without reading when the 'p' descriptors are detected
*/

int sock_ssel(struct SOCK *ss[], int ns, char *message, int max_len, int *l,
	      int *p, int n, int tim, int rd_in) {

  fd_set rfd;
  int sel, i;
  static struct timeval timeout;
  static int rd_dead = 0;
  struct timeval *pt;
  struct SOCK *s;

  if ( ! message && tim >= 0 ) {
    (*bs->error)("sock_ssel: no message buffer given", NULL);
    return(-3);
  }

  while ( 1 ) {

    FD_ZERO(&rfd);
    if ( rd_in && ! rd_dead )
      FD_SET(0, &rfd);

    if ( bs->bind_fd > 0 )
      FD_SET(bs->bind_fd, &rfd);

    for ( s = bs->head ; s ; s = s->next ) {
      if ( s->fd > 0 ) {
        for ( i = 0 ; i < ns && ss[i] != s ; i++ )
          continue;
        if ( i >= ns )
          FD_SET(s->fd, &rfd);
      }
    }
    if ( p && n > 0 )
      for ( i = 0 ; i < n ; i++ )
        FD_SET(p[i], &rfd);

    if ( tim > 0 ) {
      if ( tim < 10000 ) {
        timeout.tv_sec = tim;
        timeout.tv_usec = 0;
      } else {
        timeout.tv_sec = 0;
        timeout.tv_usec = tim;
      }
      pt = &timeout;
    } else if ( tim == 0 )
      pt = NULL;
    else {
      timeout.tv_sec = 0;               /* Do a poll only */
      timeout.tv_usec = 0;
      pt = &timeout;
    }
    sel = select(FD_SETSIZE, &rfd, NULL, NULL, pt);

    if ( sel < 0 ) {
      if ( errno != EINTR )
        (*bs->error)("sock_ssel: 'select' error --- %s", strerror(errno));
      else if ( bs->interrupt )
        return(-3);
      continue;
    }
    if ( tim < 0 )
      return(sel);                       /* Was only polling */

    if ( sel == 0 )
      return(-1);

    if ( bs->bind_fd > 0 && FD_ISSET(bs->bind_fd, &rfd) )
      accept_sock();

    if ( p && n > 0 )
      for ( i = 0 ; i < n ; i++ )
        if ( FD_ISSET(p[i], &rfd) )
          return(p[i]);

    for ( s = bs->head ; s ; s = s->next )
      if ( s->fd > 0 )
        if ( FD_ISSET(s->fd, &rfd) )
	  if ( ( sel = read_sock(s, message, max_len-1, l) ) > 0 )
            return(sel);

    if ( rd_in && ! rd_dead && FD_ISSET(0, &rfd) ) {
      last_conn = &sock_kbd;
      if ( ( i = read(0, message, 256) ) <= 0 ) {
	rd_dead = 1;
	return(-2);
      }
      *l = i;
      message[i] = '\0';
      return(0);
    }
  }
}



int sock_fastsel(char *message, int max_len, int *l, int *p, int n,
		 struct timeval *tim, int rd_in) {

  fd_set rfd;
  int sel, i;
  static int rd_dead = 0;
  struct SOCK *s;

  if ( ! message ) {
    (*bs->error)("sock_fastsel: no message buffer given", NULL);
    return(-3);
  }

  while ( 1 ) {

    FD_ZERO(&rfd);
    if ( rd_in && ! rd_dead )
      FD_SET(0, &rfd);

    if ( bs->bind_fd > 0 )
      FD_SET(bs->bind_fd, &rfd);

    for ( s = bs->head ; s ; s = s->next ) {
      if ( s->fd > 0 ) {
        FD_SET(s->fd, &rfd);
      }
    }
    if ( p && n > 0 )
      for ( i = 0 ; i < n ; i++ )
        FD_SET(p[i], &rfd);

    sel = select(FD_SETSIZE, &rfd, NULL, NULL, tim);

    if ( sel < 0 ) {
      if ( errno != EINTR )
        (*bs->error)("sock_fastsel: 'select' error --- %s", strerror(errno));
      else if ( bs->interrupt )
        return(-3);
      continue;
    }

    if ( sel == 0 )
      return(-1);

    if ( bs->bind_fd > 0 && FD_ISSET(bs->bind_fd, &rfd) )
      accept_sock();

    if ( p && n > 0 )
      for ( i = 0 ; i < n ; i++ )
        if ( FD_ISSET(p[i], &rfd) )
          return(p[i]);

    for ( s = bs->head ; s ; s = s->next )
      if ( s->fd > 0 )
        if ( FD_ISSET(s->fd, &rfd) )
          if ( ( sel = read_sock(s, message, max_len-1, l) ) > 0 )
            return(sel);

    if ( rd_in && ! rd_dead && FD_ISSET(0, &rfd) ) {
      last_conn = &sock_kbd;
      if ( ( i = read(0, message, 256) ) <= 0 ) {
	rd_dead = 1;
	return(-2);
      }
      *l = i;
      message[i] = '\0';
      return(0);
    }
  }
}



int sock_only(struct SOCK *handle, char *message, int max_len, int tim) {

  fd_set rfd;
  int sel, len;
  static struct timeval timeout;
  struct timeval *pt;

  if ( ! handle ) {
    (*bs->error)("sock_only: no socket given", NULL);
    return(-3);
  }

  while ( 1 ) {

    FD_ZERO(&rfd);
    if ( bs->bind_fd > 0 )
      FD_SET(bs->bind_fd, &rfd);

    if ( handle->fd > 0 )
      FD_SET( handle->fd, &rfd);

    if ( tim > 0 ) {
      if ( tim < 10000 ) {
        timeout.tv_sec = tim;
        timeout.tv_usec = 0;
      } else {
        timeout.tv_sec = 0;
        timeout.tv_usec = tim;
      }
      pt = &timeout;
    } else if ( tim == 0 )
      pt = NULL;
    else
      pt = &timeout;

    if ( ( sel = select(FD_SETSIZE, &rfd, NULL, NULL, pt) ) < 0 ) {
      if ( errno == EINTR )
        return(-3);
      (*bs->error)("sock_only: 'select' error --- %s", strerror(errno));
      continue;
    }

    if ( sel == 0 )
      return(-1);

    if ( bs->bind_fd > 0 && FD_ISSET(bs->bind_fd, &rfd) )
      accept_sock();

    if ( handle->fd > 0 )
      if ( FD_ISSET(handle->fd, &rfd) )
	if ( ( sel = read_sock(handle, message, max_len, &len) ) > 0 )
          return(sel);
  }
}



int sock_poll(struct SOCK *handle, char *message, int max_len, int *plen) {

  fd_set rfd;
  int sel;
  static struct timeval timeout;
  struct timeval *pt;

  *plen = 0;
  if ( ! handle ) {
    (*bs->error)("sock_poll: no socket given", NULL);
    return(-3);
  }

  while ( 1 ) {

    FD_ZERO(&rfd);
    if ( bs->bind_fd > 0 )
      FD_SET(bs->bind_fd, &rfd);

    if ( handle->fd > 0 )
      FD_SET(handle->fd, &rfd);

    timeout.tv_sec = 0;
    timeout.tv_usec = 0;
    pt = &timeout;

    if ( ( sel = select(FD_SETSIZE, &rfd, NULL, NULL, pt) ) < 0 ) {
      if ( errno == EINTR )
        return(-3);
      (*bs->error)("sock_poll: 'select' error --- %s", strerror(errno));
      continue;
    }

    if ( sel == 0 )
      return(-1);

    if ( bs->bind_fd > 0 && FD_ISSET(bs->bind_fd, &rfd) )
      accept_sock();

    if ( handle->fd > 0 )
      if ( FD_ISSET(handle->fd, &rfd) )
        if ( ( sel = read_sock(handle, message, max_len, plen) ) > 0 )
          return(sel);
  }
}



int accept_sock() {

  char dname[4096];
  struct SOCK sock, *s;
  struct sockaddr_in client_address;
  char *client_ip;
  socklen_t client_len;
  unsigned long count, ct;
  uint32_t net;
  int allowed, len, i, n;

  client_len = sizeof(struct sockaddr);
  if ( ( sock.fd = accept(bs->bind_fd, (struct sockaddr *) &client_address,
			  &client_len) ) < 0 ) {
    (*bs->error)("accept_sock: 'accept' error --- %s", strerror(errno));
    return(-1);
  }

  if ( strcmp(bs->allowed[0], "any") != 0 ) {
    client_len = sizeof(struct sockaddr);
    if ( getpeername(sock.fd, (struct sockaddr *) &client_address,
		     &client_len) < 0 ) {
      close(sock.fd);
      (*bs->error)("accept_sock: can't get address of incoming socket --- %s",
		   strerror(errno));
      return(-1);
    }

    client_ip = inet_ntoa(client_address.sin_addr);

    allowed = 0;
    for ( i = 0 ; i < MAXALLOWED ; i++ ) {
      len = strlen(bs->allowed[i]);
      if ( len > 0 ) {
        if ( strncmp(client_ip, bs->allowed[i], len) == 0 ) {
          allowed = 1;
          break;
	}
      }
    }

    if ( ! allowed ) {
// Can't print message here since that will set the error flag for the following
// message from an allowed client when it reaches 'sockmsg'
//      (*bs->error)("accept_sock: refusing connection from '%s'", client_ip);
      close(sock.fd);
      return(-1);
    }
  }

  if ( fcntl(sock.fd, F_SETFD, FD_CLOEXEC) < 0 ) {
    (*bs->error)("accept_sock: 'fcntl' error --- %s", strerror(errno));
    return(0);
  }

/* can't use read_sock because I want a timeout on read */

  if ( ( n = readtm(sock.fd, (char *) &net, sizeof(uint32_t)) ) > 0 ) {
    count = (unsigned long) ntohl(net);
    if ( count <= bs->bufct ) {
      ct = count;
      while ( ( n = readtm(sock.fd, &dname[count - ct], ct) ) < ct && n > 0 )
        ct -= n;
    } else
      (*bs->error)("accept_sock: read count out of sync", NULL);
  }

  if ( n < 0 )
    (*bs->error)("accept_sock: 'read' error --- %s", strerror(errno));

  if ( n <= 0 || count > bs->bufct ) {
    close(sock.fd);
    sock.fd = -1;
    return(-1);
  }
  dname[count] = '\0';

  if ( ( s = (struct SOCK *) sock_connect(dname) ) == 0 )
    s = (struct SOCK *) sock_connect("ANONYMOUS");

  if ( s->fd >= 0 ) {
    if ( bs->close )
      (*bs->close)(s->fd);
    close(s->fd);
  }

  s->fd = sock.fd;
  if ( bs->open )
    (*bs->open)(s, s->fd);

  return(sock.fd);
}



/* just like read with a 5 second timeout */

static int readtm(int fd, char *buf, int len) {

  fd_set rfd;
  int sel;
  struct timeval timeout;

  FD_ZERO(&rfd);
  FD_SET(fd, &rfd);

  timeout.tv_sec = 5;
  timeout.tv_usec = 0;

  if ( ( sel = select(FD_SETSIZE, &rfd, NULL, NULL, &timeout) ) < 0 ) {
    (*bs->error)("readtm: 'select' error --- %s", strerror(errno));
    return(-3);
  }

  if ( sel == 0 )
    return(-1);

  return(read(fd, buf, len));
}



int sock_send(struct SOCK *s, char *message) {

  return(sock_write(s, message, strlen(message)));
}



/*
  like sock_send but takes pointer and count as in write
*/

int sock_write(struct SOCK *s, char *message, int l) {

  int ret, err, flag = 0;
  unsigned long count;
  uint32_t net;
  socklen_t len;
  char *name;

  if ( (long) s == -1 || ! message || l <= 0 )
    return(0);

  if ( ! s ) {
    (*bs->error)("sock_write: no mailbox for: '%s'", message);
    return(0);
  }

  while ( flag < 2 ) {
    if ( s->fd < 0 ) {
      if ( strcmp(s->dest->dname, "ANONYMOUS") == 0 )
        return(0);

      if ( ( s->fd = socket(s->sin.sin_family, SOCK_STREAM, 0) ) < 0 ) {
	(*bs->error)("sock_write: 'socket' error --- %s", strerror(errno));
        return(0);
      }
      if ( bs->open )
        (*bs->open)(s, s->fd);
      bind_any(s->fd);

      if ( connect(s->fd, (struct sockaddr *) &s->sin,
		   sizeof(struct sockaddr_in)) < 0 ) {
        if ( bs->close )
          (*bs->close)(s->fd);
        close(s->fd);
        s->fd = -1;
	(*bs->error)("sock_write: 'connect' error --- %s", strerror(errno));
        return(0);
      }

      if ( bs->bind_fd > 0 ) {
        count = strlen(bs->dest->dname);
        name = bs->dest->dname;
      } else { /* if he never bound then send ANONYMOUS */
        count = 9;
        name = "ANONYMOUS";
      }
      net = htonl((uint32_t) count);
      if ( ( ret = write(s->fd, &net, sizeof(uint32_t)) ) > 0 )
        ret = write(s->fd, name, count);
    }

    count = l;
    net = htonl((uint32_t) count);
    if ( ( ret = write(s->fd, &net, sizeof(uint32_t)) ) > 0 )
      ret = write(s->fd, message, count);

/*
   this checks to see if vxworks box (or sun) has rebooted
*/
    usleep(1);
    len = 4;
    err = 0;
    if ( getsockopt(s->fd, SOL_SOCKET, SO_ERROR, (char *) &err, &len) < 0 ||
	 err != 0 )
      ret = count + 1;

    if ( ret != count ) {
      if ( ret < 0 )
	(*bs->error)("sock_write: 'write' error --- %s", strerror(errno));
      if ( s->dest->dname )
	(*bs->error)("sock_write: closing mailbox '%s'", s->dest->dname);
      else
	(*bs->error)("sock_write: closing mailbox", NULL);
      if ( bs->close )
        (*bs->close)(s->fd);
      close(s->fd);
      s->fd = -1;
      flag += 1;
   } else
     break;
  }
  return(1);
}



struct DEST *find_dest(char *name) {

  int i;

  if ( destflag == 0 )
    init_dest();

  for ( i = 0 ; i < MAXDEST ; i++ )
    if ( mailboxes[i].dname[0] == '\0' )
      break;
    else if ( strcmp(mailboxes[i].dname, name) == 0 )
      return(&mailboxes[i]);

  for ( i = 0 ; i < MAXDEST ; i++ )
    if ( def_mailboxes[i].dname[0] == '\0' )
      break;
    else if ( strcmp(def_mailboxes[i].dname, name) == 0 )
      return(&def_mailboxes[i]);

  return(NULL);
}



struct DEST *find_port(int p) {

  int i;

  if ( destflag == 0 )
    init_dest();

  for ( i = 0 ; i < MAXDEST ; i++ )
    if ( mailboxes[i].dname[0] == '\0' )
      break;
    else if ( mailboxes[i].dport == p )
      return(&mailboxes[i]);

  for ( i = 0 ; i < MAXDEST ; i++ )
    if ( def_mailboxes[i].dname[0] == '\0' )
      break;
    else if ( def_mailboxes[i].dport == p )
      return(&def_mailboxes[i]);

  return(NULL);
}



static void init_dest() {

  static char delim[] = ", \t\n";
  FILE *fd;
  int i, count;
  char host[80], buf[256], mailbox[256], *p, *p1;

  gethostname(host, sizeof(host));

  if ( ( p = (char *) getenv("MAILBOXDEFS") ) == NULL ) {
    if ( ( p1 = (char *) getenv("BIFROST_HOME") ) == NULL )
      p = DEFAULT_MAILBOX;
    else {
      sprintf(mailbox, "%s/Resources/Configurations/mailboxdefs", p1);
      p = mailbox;
    }
  }

  bzero(&mailboxes[0], sizeof(struct DEST)*MAXDEST);
  if ( ( fd = fopen(p, "r") ) == NULL ) {
    destflag = 1;
    (*bs->error)("init_dest: unable to open mailbox definition file '%s'", p);
    return;
  }

  count = 0;
  while ( fgets(buf, 256, fd) != NULL ) {
    if ( buf[0] == '#' || buf[0] == '\n' )
      continue;
    if ( ( i = atoi(strtok(buf, delim)) ) <= 0 )
      continue;
    mailboxes[count].dport = (in_port_t) i;
    strncpy(mailboxes[count].host, strtok(NULL, delim), MAXNAME);
    strncpy(mailboxes[count].dname, strtok(NULL, delim), MAXNAME);

    if ( strcmp(mailboxes[count].host, "SELF") == 0 )
      strncpy(mailboxes[count].host, host, MAXNAME);
    if ( strcmp(mailboxes[count].host, "LOCAL") == 0 )
      strcpy(mailboxes[count].host, "localhost");

    if ( ++count >= MAXDEST ) {
      (*bs->error)("init_dest: too many entries in mailbox definition file "
		   "'%s'", p);
      break;
    }
  }
  fclose(fd);
  destflag = 1;
}



/*
    bind before connect to avoid known OS hang bug
*/

void bind_any(int fd) {

  int port, ret;
  struct sockaddr_in sin;

  port = 30000;

  while ( 1 ) {
    bzero(&sin, sizeof(struct sockaddr_in));
    sin.sin_family = AF_INET;
    if ( strcmp(bs->domain, "any") == 0 )
      sin.sin_addr.s_addr = htonl(INADDR_ANY);
    else if ( strcmp(bs->domain, "local") == 0 )
      sin.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    else
      sin.sin_addr.s_addr = inet_addr(bs->domain);
    sin.sin_port = htons((uint16_t) port);

    if ( ( ret = bind(fd, (struct sockaddr *) &sin, sizeof(sin)) ) >= 0 )
      break;

    if ( port-- < 1800 || errno != EADDRINUSE )
      break;
  }
  if ( ret < 0 )
    (*bs->error)("bind_any: 'bind' error --- %s", strerror(errno));
}



void sock_openclose(int (*open)(struct SOCK *, int), int (*close)(int)) {

  bs->open = open;
  bs->close = close;
}



void sock_seterror(void (*err)(char *, char *)) {

   bs->error = err;
}



void standard_error(char *a, char *b) {

  fprintf(stderr, a, b);
}
