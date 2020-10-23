#include "./mycommun.h"

#define PORT 50000
#define BUFSIZE 512

int communicate(int sock) {
  int len;
  char buf[BUFSIZE];

  len = recv(sock, buf, BUFSIZE, 0);

  printf("%s\n", buf);

  if (len <= 0) return -2;

  buf[len] = '\n';
  len = send(sock, buf, strlen(buf), 0);

  return 0;
}

int main(int argc, char **argv) {
  int sock = prepare_sock_s(PORT);

  if (sock < 0) return 1;
  
  listen(sock, 5);

  while (1) {
    struct sockaddr_in cinfo;
    unsigned int len_cinfo = sizeof(cinfo);
    int sock_c = accept(sock, (struct sockaddr *)&cinfo, &len_cinfo);

    communicate(sock_c);
    
    close(sock_c);
  }

  close(sock);
  return 0;
}
