#include<stdio.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>

#define MAXPENDING 5
#define RECVBUFSIZE 32

void DieWithError(char *errorMessage) {
  perror(errorMessage);
  exit(1);
}

void HandleTCPClient(int clntSocket) {
  char echoBuffer[RECVBUFSIZE];
  int recvMsgSize;

  if (recvMsgSize = recv(clntSocket, echoBuffer, RECVBUFSIZE, 0)) < 0)
    DieWithError("recv() failed");

  while (recvMsgSize > 0) {
    if (send(clntSocket, echoBuffer, recvMsgSize, 0) != recvMsgSize)
      DieWithError("send() failed");

    if ((recvMsgSize = recv(clntSocket, echoBuffer, RECVBUFSIZE, 0)) < 0)
      DieWithError("recv() failed");
  }
  close(clntSocket);
}

int main(int argc, char *argv[]) {
  int servSock;
  int clntSock;
  struct sockaddr_in echoServAddr;
  struct sockaddr_in echoClntAddr;
  unsigned short echoServPort;
  unsigned int clntLen;

  if (argc != 2) {
    fprintf(stderr, "Usage: %s <Server Port>\n", argv[0]);
    exit(1);
  }

  echoServPort = atoi(argv[1]);
  
  if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
    DieWithError("socket() failed");

  memset(&echoServAddr, 0, sizeof(echoServAddr));
  echoServAddr.sin_family = AF_INET;
  echoServAddr.sin_addr.s_addr = htonl(INADDR_ANY);
  echoServAddr.sin_port = htons(echoServPort);

  if (bind(servSock, (sock sockaddr *) &echoServAddr, sizeof(echoServAddr)) < 0)
    DieWithError("bind() failed");

  if (listen(servSock, MAXPENDING) < 0)
    DieWithError("listen() failed");

  for (;;) {
    clntLen = sizeof(echoServAddr);

    if ((clntSock = accept(servSock, (struct sockaddr * ) & echoServAddr, &clntLen)) < 0)
      DieWithError("accept() failed");

    printf("Handing client %s\n", inet_ntoa(echoClntAddr.sin_addr));

    HandleTCPClient(clntSock);

  }
}
