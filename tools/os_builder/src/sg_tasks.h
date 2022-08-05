#ifndef ACN_OSEK_SG_TASKS_H
#define ACN_OSEK_SG_TASKS_H

#include <osek.h>
#include <osek_com.h>


enum eTaskType {
	TASK_TASK_A_ID,
	TASK_TASK_B_ID,
	TASK_TASK_C_ID,
	TASK_TASK_D_ID,
	TASK_ID_MAX
};


#define TASK_A_APPMODE_MAX	(3)
#define TASK_A_RESOURCE_MAX	(1)
#define TASK_A_EVENT_MAX	(0)
#define TASK_A_MESSAGE_MAX	(0)

#define TASK_B_APPMODE_MAX	(0)
#define TASK_B_RESOURCE_MAX	(0)
#define TASK_B_EVENT_MAX	(1)
#define TASK_B_MESSAGE_MAX	(0)

#define TASK_C_APPMODE_MAX	(1)
#define TASK_C_RESOURCE_MAX	(0)
#define TASK_C_EVENT_MAX	(2)
#define TASK_C_MESSAGE_MAX	(0)

#define TASK_D_APPMODE_MAX	(0)
#define TASK_D_RESOURCE_MAX	(1)
#define TASK_D_EVENT_MAX	(0)
#define TASK_D_MESSAGE_MAX	(0)



typedef void (*TaskFuncType)(void);

typedef struct {
    TaskType id;
    TaskFuncType handler;
    u32 priority;
    SchType sch_type;
    u32 activations;
    bool autostart;
    const AppModeType** appmodes;
    u32 n_appmodes;
    MessageType** msglist;
    u32 n_msglist;
    const EventMaskType** evtmsks;
    u32 n_evtmsks;
    u32 stack_size;
} OsTaskType;

extern const OsTaskType _OsTaskList[];


#define OS_TASK(task)    (OSEK_Task_##task)

DeclareTask(Task_A);
DeclareTask(Task_B);
DeclareTask(Task_C);
DeclareTask(Task_D);

#define OS_MAX_TASK_PRIORITY  (4)


#endif
