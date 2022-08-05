#ifndef ACN_OSEK_SG_EVENTS_H
#define ACN_OSEK_SG_EVENTS_H

#include <osek.h>


/* OS_EVENT: This macro function allows users to get event mask using
   the name of the event (passed as 2nd parameter) configured in the
   OSEK-Builder.xlsx */
#define OS_EVENT(task, event)   (EVENT_MASK_##task##_##event)


/*  Event Masks for Task_B  */
#define EVENT_MASK_Task_B_event1	(0x0000000000000001)

/*  Event Masks for Task_C  */
#define EVENT_MASK_Task_C_event1	(0x0000000000000001)
#define EVENT_MASK_Task_C_event2	(0x0000000000000002)



/*  Event array for Task_B  */
extern const EventMaskType Task_B_EventMasks[];

/*  Event array for Task_C  */
extern const EventMaskType Task_C_EventMasks[];


#endif
