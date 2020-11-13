# Makefile

CC = gcc
CFLAGS = -Wall

.PHONY: all
all: server client

client: client.o mycommun.o
	$(CC) -o $@ client.o mycommun.o

server: server.o mycommun.o
	$(CC) -o $@ server.o mycommun.o

cient.o: client.c
	$(CC) $(CFLAGS) -c client.c

server.o: server.c
	$(CC) $(CFLAGS) -c server.c

mycommun.o: mycommun.c
	$(CC) $(CFLAGS) -c mycommun.c

mycommun.o: mycommun.h

.PHONY: clean
clean:
	rm -f server client *.o
	