!include <win32.mak>

GFS_EXECS = get_fanspeed_1.exe get_fanspeed_2.exe get_fanspeed_3.exe get_fanspeed_4.exe

GFS_OBJS = get_fanspeed_1.obj get_fanspeed_2.obj get_fanspeed_3.obj get_fanspeed_4.obj

GFS_SOURCE = get_fanspeed_1.c get_fanspeed_2.c get_fanspeed_3.c get_fanspeed_4.c

#------------------------------------------------------------------------#

SFS_EXECS = set_fanspeed_1.exe set_fanspeed_2.exe set_fanspeed_3.exe set_fanspeed_4.exe

SFS_OBJS = set_fanspeed_1.obj set_fanspeed_2.obj set_fanspeed_3.obj set_fanspeed_4.obj

SFS_SOURCE = set_fanspeed_1.c set_fanspeed_2.c set_fanspeed_3.c set_fanspeed_4.c

#------------------------------------------------------------------------#

GL_EXECS = get_level_1.exe get_level_2.exe get_level_3.exe get_level_4.exe

GL_OBJS = get_level_1.obj get_level_2.obj get_level_3.obj get_level_4.obj

GL_SOURCE = get_level_1.c get_level_2.c get_level_3.c get_level_4.c

#------------------------------------------------------------------------#

USB_EXECS = usb_close.exe usb_open.exe init_bit.exe

USB_OBJS = usb_close.obj usb_open.obj init_bit.obj

USB_SOURCE = usb_close.c usb_open.c init_bit.c

#------------------------------------------------------------------------#

LNK_FILES = rtdacusb.obj ftd2xx.lib

#------------------------------------------------------------------------#

all: clean $(GFS_EXECS) $(SFS_EXECS) $(GL_EXECS) $(USB_EXECS)

#------------------------------------------------------------------------#

$(GFS_EXECS): $(GFS_OBJS) $(LNK_FILES)
	LINK get_fanspeed_1.obj $(LNK_FILES)

	LINK get_fanspeed_2.obj $(LNK_FILES)

	LINK get_fanspeed_3.obj $(LNK_FILES)

	LINK get_fanspeed_4.obj $(LNK_FILES)

#------------------------------------------------------------------------#

$(SFS_EXECS): $(SFS_OBJS) $(LNK_FILES)
	LINK set_fanspeed_1.obj $(LNK_FILES)

	LINK set_fanspeed_2.obj $(LNK_FILES)

	LINK set_fanspeed_3.obj $(LNK_FILES)

	LINK set_fanspeed_4.obj $(LNK_FILES)

#------------------------------------------------------------------------#

$(GL_EXECS): $(GL_OBJS) $(LNK_FILES)
	LINK get_level_1.obj $(LNK_FILES)

	LINK get_level_2.obj $(LNK_FILES)

	LINK get_level_3.obj $(LNK_FILES)

	LINK get_level_4.obj $(LNK_FILES)

#------------------------------------------------------------------------#

$(USB_EXECS): $(USB_OBJS) $(LNK_FILES)
	LINK usb_close.obj $(LNK_FILES)

	LINK usb_open.obj $(LNK_FILES)

	LINK init_bit.obj $(LNK_FILES)

#------------------------------------------------------------------------#

$(GFS_OBJS): $(GFS_SOURCE)
	cl /c $(GFS_SOURCE)

$(SFS_OBJS): $(SFS_SOURCE)
	cl /c $(SFS_SOURCE)

$(GL_OBJS): $(GL_SOURCE)
	cl /c $(GL_SOURCE)

$(USB_OBJS): $(USB_SOURCE)
	cl /c $(USB_SOURCE)

#------------------------------------------------------------------------#

rtdacusb.obj: rtdacusb.c
	cl /c rtdacusb.c

#------------------------------------------------------------------------#

clean:
	del *.obj $(GFS_EXECS) $(SFS_EXECS) $(GL_EXECS) $(USB_EXECS) init_bit.exe