#include <stddef.h>

#include "sg_resources.h"
#include "sg_tasks.h"



/* Resources Definitions in RAM */
ResourceType RES_MUTEX1;


/*  Resources lists for Tasks */
const TaskType RES_MUTEX1_tasks[] = {
	TASK_TASK_A_ID,
	TASK_TASK_D_ID,
};

const OsResMapType _OsResList[MAX_RESOURCE_ID] = {
	{
		.res = &RES_MUTEX1,
		.ceil_prio = 4,
		.n_tasks = 3,
		.task_ids = RES_MUTEX1_tasks
	},
};
