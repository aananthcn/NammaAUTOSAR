#include "sg_counter.h"


OsCounterType _OsCounters[] =  {
	{
		.alarm.mincycle = 1,
		.alarm.maxallowedvalue = 1000000,
		.alarm.ticksperbase = 1,
		.maxallowedvalue = 1000000,
		.name = "mSecCounter"
	},
	{
		.alarm.mincycle = 100,
		.alarm.maxallowedvalue = 1000,
		.alarm.ticksperbase = 1,
		.maxallowedvalue = 1000,
		.name = "uSecCounter"
	}
};
