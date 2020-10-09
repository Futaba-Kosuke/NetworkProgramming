#include<stdio.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<unistd.h>
#include<string.h>

#define BUFSIZE 512

int prepare_sock_c (char *host, int port) { 
  int sock = socket(PF_INET, SOCK_STREAM, 0);
  if (sock < 0) return -1;
  struct sockaddr_in target;
  target.sin_family = AF_INET;
  target.sin_addr.s_addr = inet_addr(host);
  target.sin_port = htons(port);
  int connected = connect(sock, (struct sockaddr *)&target, sizeof(target));
  if (connected < 0) return -2;
  return sock;
}

int communicate(int sock) {
  char *message = "yahoo!";
  int len;
  char buf[BUFSIZE];
  len = send(sock, message, strlen(message), 0);
  if (len < strlen(message)) return -1;
  len = recv(sock, buf, BUFSIZE, 0);
  buf[len] = '\0';
  printf("recv:%s\n", buf);
  return 0;
}

int main(int argc, char **argv) {
  int sock = prepare_sock_c("localhost", 50000);

  if (sock < 0) return 1;
  communicate(sock);

  close(sock);
  return 0;
}
