
INCDIRS  += -I ${OS_BUILDER_PATH}/src 

LDFLAGS  += -g
CFLAGS   += -Werror ${INCDIRS} -g
ASFLAGS  += ${INCDIRS} -g

SG_OBJS	:= \
	${OS_BUILDER_PATH}/src/sg_counter.o \
	${OS_BUILDER_PATH}/src/sg_appmodes.o \
	${OS_BUILDER_PATH}/src/sg_events.o \
	${OS_BUILDER_PATH}/src/sg_resources.o \
	${OS_BUILDER_PATH}/src/sg_messages.o \
	${OS_BUILDER_PATH}/src/sg_fifo.o \
	${OS_BUILDER_PATH}/src/sg_alarms.o \
	${OS_BUILDER_PATH}/src/sg_tasks.o \
	${OS_BUILDER_PATH}/src/sg_ivector.o


