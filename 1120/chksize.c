# include <stdio.h>

struct money1 {
  int deposit;
  int withdraw;
};

struct money2 {
  int deposit;
  int withdraw;
  unsigned short numDeposit;
  unsigned short numWithdraw;
};

struct money3 {
  int deposit;
  unsigned short numDeposit;
  int withdraw;
  unsigned short numWithdraw;
};

struct money4 {
  int deposit;
  unsigned short numDeposit;
  unsigned short numWithdraw;
};

struct money5 {
  unsigned short A;
  unsigned short B;
  int C;
  int D;
};

struct money6 {
  unsigned short A;
  int B;
  unsigned short C;
};

struct money7 {
  unsigned short A;
  unsigned short B;
  unsigned short C;
};

struct money8 {
  int A;
  unsigned short B;
};

struct money9 {
  unsigned short A;
  int B;
};

int main(int argc, char *argv[]) {
    printf("intは%luバイト\n", sizeof(int));
    printf("unshortは%luバイト\n", sizeof(unsigned short));
    printf("money1は%luバイト\n", sizeof(struct money1));
    printf("money2は%luバイト\n", sizeof(struct money2));
    printf("money3は%luバイト\n", sizeof(struct money3));
    printf("money4は%luバイト\n", sizeof(struct money4));
    printf("money5は%luバイト\n", sizeof(struct money5));
    printf("money6は%luバイト\n", sizeof(struct money6));
    printf("money7は%luバイト\n", sizeof(struct money7));
    printf("money8は%luバイト\n", sizeof(struct money8));
    printf("money9は%luバイト\n", sizeof(struct money9));

    return 0;
}
