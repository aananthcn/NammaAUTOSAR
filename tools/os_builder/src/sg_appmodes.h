#ifndef ACN_OSEK_SG_APPMODES_H
#define ACN_OSEK_SG_APPMODES_H

#include <osek.h>
#include <osek_com.h>


enum eAppModeType {
	OSDEFAULTAPPMODE,
	MANUFACT_MODE,
	HW_TEST_MODE,
	OS_MODES_MAX
};

extern const AppModeType Task_A_AppModes[];
extern const AppModeType Task_C_AppModes[];


#endif
