CC = gcc
CFLAGS = -O2 -fPIC -fopenmp
INCLUDES = -I../lib
LIBS = -L../lib -lMPGrid -lz -lm

all:	etc

etc:	etc.c
	$(CC) $(CFLAGS) $(INCLUDES) etc.c $(LIBS) -o $@ 

clean:
	rm etc

