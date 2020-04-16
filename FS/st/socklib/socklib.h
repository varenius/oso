/*****************************************************************************
 *
 * FILE: socklib.h
 *
 *   Structures and procedures used by 'socklib'.
 *
 *   This file should be included in any program that uses 'socklib'.
 *
 * HISTORY
 *
 * who          when           what
 * ---------    -----------    ----------------------------------------------
 * lerner       13 Jun 2012    Original version
 * lerner        6 Jul 2015    Modified BOUND structure and added 'sock_domain'
 *                             and 'sock_allowed'
 *
 *****************************************************************************/



#include <netinet/in.h>



/*****************************************************************************
 *
 *   Set up some useful constants
 *
 *****************************************************************************/

/*  Constants for 'socklib.c'  */

#define MAXDEST      100
#define MAXNAME       30
#define MAXALLOWED     5



/*****************************************************************************
 *
 *   Set up some useful macros
 *
 *****************************************************************************/



/*****************************************************************************
 *
 *   Define the structures we need
 *
 *****************************************************************************/

/*  Structures for 'socklib.c'  */

struct DEST {
  in_port_t dport;
  char host[MAXNAME];
  char dname[MAXNAME];
};

struct SOCK {
  struct SOCK *next;
  struct DEST *dest;
  int fd;
  struct sockaddr_in sin;
};

struct BOUND {
  int bind_fd;
  struct DEST *dest;
  struct SOCK *head; /* head of list */
  struct sockaddr_in sin;
  unsigned int bufct;
  int interrupt;
  char allowed[MAXALLOWED][MAXNAME];
  char domain[MAXNAME];
  int (*open)(struct SOCK *, int);
  int (*close)(int);
  void (*error)(char *, char *);
};



/*****************************************************************************
 *
 *   Set up some external variable declarations
 *
 *****************************************************************************/



/*****************************************************************************
 *
 *   All the procedures in 'socklib'
 *
 *****************************************************************************/

/*  Procedures in 'socklib.c'  */

int sock_bind(char *mbname);
struct SOCK *sock_connect(char *mbname);
int read_sock(struct SOCK *s, char *msg, int max_len, int *l);
int sock_close(char *name);
struct SOCK *last_msg();
char *sock_name(struct SOCK *handle);
int sock_fd(struct SOCK *handle);
int sock_bufct(int bufct);
struct SOCK *sock_find(char *mbname);
struct SOCK *sock_findfd(int fd);
void sock_intr(int flag);
void sock_domain(char *domain);
void sock_allowed(char *allowed_list);
int sock_sel(char *message, int max_len, int *l, int *p, int n, int tim,
	     int rd_in);
int sock_seln(char *message, int max_len, int *l, int *p, int n, int tim,
	      int rd_in);
int sock_ssel(struct SOCK *ss[], int ns, char *message, int max_len, int *l,
	      int *p, int n, int tim, int rd_in);
int sock_fastsel(char *message, int max_len, int *l, int *p, int n,
		 struct timeval *tim, int rd_in);
int sock_only(struct SOCK *handle, char *message, int max_len, int tim);
int sock_poll(struct SOCK *handle, char *message, int max_len, int *plen);
int accept_sock();
int sock_send(struct SOCK *s, char *message);
int sock_write(struct SOCK *s, char *message, int l);
struct DEST *find_dest(char *name);
struct DEST *find_port(int p);
void bind_any(int fd);
void sock_openclose(int (*open)(struct SOCK *, int), int (*close)(int));
void sock_seterror(void (*err)(char *, char *));
void standard_error(char *a, char *b);
