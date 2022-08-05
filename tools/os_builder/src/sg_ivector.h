#ifndef ACN_OSEK_IVECTOR_H
#define ACN_OSEK_IVECTOR_H

#include <osek.h>
#include <osek_com.h>


#define NUMBER_OF_IVECTORS 	(1)
#define MAX_IVECTOR_NUMBER  	(4)
#define MIN_IVECTOR_NUMBER  	(4)


extern void (*_IsrHandler[])(void);


#endif
