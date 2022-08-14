#COMPILER=
#CC=${COMPILER}gcc
#LD=${COMPILER}gcc
#AS=${COMPILER}as
#OBJCOPY=${COMPILER}objcopy
#ARCH = x86

INCDIRS  += -I ${CWD}/tools/src 

LDFLAGS  += -g
CFLAGS   += -Werror ${INCDIRS} -g
ASFLAGS  += ${INCDIRS} -g

$(info compiling System Generator source files)


SG_OBJS	:= \
	${CWD}/tools/src/sg_counter.o \
	${CWD}/tools/src/sg_appmodes.o \
	${CWD}/tools/src/sg_events.o \
	${CWD}/tools/src/sg_resources.o \
	${CWD}/tools/src/sg_messages.o \
	${CWD}/tools/src/sg_fifo.o \
	${CWD}/tools/src/sg_alarms.o \
	${CWD}/tools/src/sg_tasks.o \
	${CWD}/tools/src/sg_ivector.o


