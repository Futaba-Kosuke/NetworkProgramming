#include "mycommun.h"

int communicate (int sock) {
    char msg[BUFSIZE];
    int len;
    struct money msgMoney = {0, 0};

    len = myrecv_bytes(sock, (char *) &msgMoney, sizeof(msgMoney));
    if (len < sizeof(msgMoney)) return 2;

    int balance = 1000000;

    balance += msgMoney.deposit;
    balance -= msgMoney.withdraw;

    sprintf(msg, "%d", balance);
    len = send(sock, msg, strlen(msg), 0);

    if (len < strlen(msg)) return 2;
    
    return 0;

}

int main (int argc, char **argv) {
    int sock = prepare_sock_s(50000);
    if (sock < 0)
        return 1;
    listen(sock, 5);
    while (1) {
        struct sockaddr_in cinfo;
        unsigned int cinfo_len = sizeof(cinfo);
        int sock_c = accept(sock, (struct sockaddr *)&cinfo, &cinfo_len);
        communicate(sock_c);
        close(sock_c);
    }
    communicate(sock);
    close(sock);
    return 0;
}
