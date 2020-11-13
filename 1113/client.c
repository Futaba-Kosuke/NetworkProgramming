#include "mycommun.h"

#define WITHDRAW 0
#define DEPOSIT 1
#define BALANCE 2
#define QUIT 9

int communicate(int sock)
{
    char choice[2];
    // char withdraw[DIGITS + 1];
    // char deposit[DIGITS + 1];
    struct money msgMoney;
    char money[DIGITS + 1];


    printf("%s\n", "何をする？");
    printf("%d: 預入\n", WITHDRAW);
    printf("%d: 引出\n", DEPOSIT);
    printf("%d: 終了\n", QUIT);
    my_scanf(choice, 1);

    switch (choice[0] - '0') {
        case WITHDRAW:
            printf("預入金額: ");
            my_scanf(money, DIGITS);
            msgMoney.withdraw = atoi(money);
            msgMoney.deposit = 0;
            break;
        case DEPOSIT:
            printf("引出金額: ");
            my_scanf(money, DIGITS);
            msgMoney.withdraw = 0;
            msgMoney.deposit = atoi(money);
            break;
        case BALANCE:
            printf("残高: ");
            my_scanf(money, DIGITS);
            msgMoney.withdraw = 0;
            msgMoney.deposit = 0;
            break;
        case QUIT:
        default:
            return 0;
    }

    char msg[BUFSIZE];
    printf("size: %lu\n", sizeof(msgMoney));
    int len = send(sock, &msgMoney, sizeof(msgMoney), 0);
    if (len < strlen(msg))
        return 1;
    len = recv(sock, msg, BUFSIZE, 0);
    if (len <= 0)
        return 2;

    msg[len] = '\0';
    printf("recv:%s\n", msg);
    return 0;
}

int main(int argc, char **argv)
{
    int sock = prepare_sock_c("127.0.0.1", 50000);
    if (sock < 0)
        return 1;
    communicate(sock);
    close(sock);
    return 0;
}
