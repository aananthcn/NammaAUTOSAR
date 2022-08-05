#include <stddef.h>
#include "sg_ivector.h"

extern void SystemTickISR(void);

/*  Interrupt Vector Handlers */
void (*_IsrHandler[])(void) = {
	NULL,
	NULL,
	NULL,
	NULL,
	SystemTickISR,
};
