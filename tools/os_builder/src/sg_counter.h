#ifndef ACN_OSEK_SG_COUNTER_H
#define ACN_OSEK_SG_COUNTER_H
#include <osek.h>


typedef struct {
    AlarmBaseType alarm; /* contains OSEK specified attributes */ 
    TickType countval; /* continuos incrementing counter */ 
    TickType maxallowedvalue; /* count in nano seconds */
    char* name;
} OsCounterType;

extern OsCounterType _OsCounters[];


#define MSECCOUNTER_INDEX   	(0)
#define USECCOUNTER_INDEX   	(1)


#define OS_TICK_DURATION_ns 	(1000000)
#define OS_TICK_COUNTER_IDX 	(0)
#define OS_MAX_COUNTERS    	(2)


#endif
