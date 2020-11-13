#ifndef MYCOMMUN
#define MYCOMMUN

#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define BUFSIZE 30
#define DIGITS 10
int prepare_sock_s(int);
int prepare_sock_c(char *, int);
void my_scanf(char *, int);
int myrecv_delimiter(int, char *, int, char);
#endif
