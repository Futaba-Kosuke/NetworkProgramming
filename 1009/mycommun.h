#ifndef MYCOMMUN
#define MYCOMMUN

#include<sys/socket.h>
#include<arpa/inet.h>
#include<unistd.h>
#include<string.h>
#include<stdio.h>

#define BUFSIZE 512

int prepare_sock_s(int);
int prepare_sock_c(char *, int);
#endif
