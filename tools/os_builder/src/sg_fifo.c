#include <stddef.h>
#include "sg_fifo.h"

/* Allocate Buffers in RAM */
#define READY_TASKS_1_SIZE (2)
OsTaskType* ReadyTasks_1[READY_TASKS_1_SIZE];
#define READY_TASKS_2_SIZE (1)
OsTaskType* ReadyTasks_2[READY_TASKS_2_SIZE];
#define READY_TASKS_3_SIZE (1)
OsTaskType* ReadyTasks_3[READY_TASKS_3_SIZE];
#define READY_TASKS_4_SIZE (3)
OsTaskType* ReadyTasks_4[READY_TASKS_4_SIZE];

OsTaskType* RunningTasks[1];


/* Allocate FIFO queues in RAM */
OsFifoType ReadyFifo_1 = {
	.task = ReadyTasks_1,
	.size = READY_TASKS_1_SIZE,
	.head = 0,
	.tail = 0,
#ifdef DEBUG
	.name = "ReadyFifo_1",
#endif
	.full = false
};


OsFifoType ReadyFifo_2 = {
	.task = ReadyTasks_2,
	.size = READY_TASKS_2_SIZE,
	.head = 0,
	.tail = 0,
#ifdef DEBUG
	.name = "ReadyFifo_2",
#endif
	.full = false
};


OsFifoType ReadyFifo_3 = {
	.task = ReadyTasks_3,
	.size = READY_TASKS_3_SIZE,
	.head = 0,
	.tail = 0,
#ifdef DEBUG
	.name = "ReadyFifo_3",
#endif
	.full = false
};


OsFifoType ReadyFifo_4 = {
	.task = ReadyTasks_4,
	.size = READY_TASKS_4_SIZE,
	.head = 0,
	.tail = 0,
#ifdef DEBUG
	.name = "ReadyFifo_4",
#endif
	.full = false
};



/* Prioritized OSEK FIFO queues in Flash */
const OsFifoType* ReadyQueue[] = {
	NULL,
	&ReadyFifo_1,
	&ReadyFifo_2,
	&ReadyFifo_3,
	&ReadyFifo_4
};

