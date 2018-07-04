CC = gcc
CFLAGS = -O2 -fPIC -DMP_PYTHON_LIB
INCLUDES = -I/usr/include/python2.6
LIBS = -lz
TARGET_D = MPGrid.so
TARGET_S = libMPGrid.a
INSTALL_DIR = ../python
OBJS = grid.o rand.o python.o

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

grid.c:	MPGrid.h
rand.c:	MPGrid.h
python.c:	MPGrid.h

