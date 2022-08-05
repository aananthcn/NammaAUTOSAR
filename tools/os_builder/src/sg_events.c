#include <osek.h>
#include "sg_events.h"


const EventMaskType Task_B_EventMasks[] = {
	EVENT_MASK_Task_B_event1
};

const EventMaskType Task_C_EventMasks[] = {
	EVENT_MASK_Task_C_event1,
	EVENT_MASK_Task_C_event2
};
