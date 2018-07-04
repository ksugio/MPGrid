CC = gcc
CFLAGS = -O2 -fPIC -DMP_PYTHON_LIB
INCLUDES = -I/usr/include/python2.6 -I../lib
LIBS = -lGL -lGLU
TARGET_D = MPGLGrid.so
TARGET_S = libMPGLGrid.a
INSTALL_DIR = ../python
OBJS = colormap.o draw.o model.o python.o scene.o text.o

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

colormap.c:	MPGLGrid.h
draw.c:	MPGLGrid.h
model.c:	MPGLGrid.h
python.c:	MPGLGrid.h
scene.c:	MPGLGrid.h
text.c:	MPGLGrid.h

