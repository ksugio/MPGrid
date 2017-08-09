CC = gcc
CFLAGS = -O2 -fPIC
INCLUDES = -I/usr/include/python2.6 -I/usr/local/cuda/include -I../lib
LIBS = -L/usr/local/cuda/lib64 -lOpenCL
TARGET_D = MPCLGrid.so
TARGET_S = libMPCLGrid.a
INSTALL_DIR = ../python
OBJS = grid.o python.o

all:	$(TARGET_D) $(TARGET_S)

$(TARGET_D):	$(OBJS)
		$(CC) -shared -o $@ $(OBJS) $(LIBS)

$(TARGET_S):	$(OBJS)
		ar r $@ $(OBJS)

install:	$(TARGET_D)
		cp $(TARGET_D) $(INSTALL_DIR)

clean:
		rm $(TARGET_D) $(TARGET_S) $(OBJS)

.c.o:
		$(CC) $(CFLAGS) $(INCLUDES) -c $<

grid.c:	MPCLGrid.h
python.c:	MPCLGrid.h

