#
# Created on Sun Oct 02 2022 10:08:31 AM
#
# The MIT License (MIT)
# Copyright (c) 2022 Aananth C N
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# OSEK Builder Global Variables (OB Globals)
# ------------------------------------------
# list of column titles in TASK tab of OSEX-Builder.xlsx
TaskParams = ["Task Name", "PRIORITY", "SCHEDULE", "ACTIVATION", "AUTOSTART",
    "RESOURCE", "EVENT", "MESSAGE", "STACK_SIZE"]
TNMI = 0
PRII = 1
SCHI = 2
ACTI = 3
ATSI = 4
RESI = 5
EVTI = 6
MSGI = 7
STSZ = 8


# list of column titles in TASK tab of OSEX-Builder.xlsx
CntrParams = ["Counter Name", "MINCYCLE", "MAXALLOWEDVALUE", "TICKSPERBASE",
     "OsCounterType"]
CNME = 0

# Column titles for Alarms
AlarmParams = ["Alarm Name", "COUNTER", "Action-Type", "arg1", "arg2", "IsAutostart",
	"ALARMTIME", "CYCLETIME", "APPMODE" ]
ANME = 0
ACNT = 1
AAAT = 2
AAT1 = 3
AAT2 = 4
AIAS = 5
ATIM = 6
ACYT = 7
AAPM = 8

# Column titles for ISRs
ISR_Params = ["ISR Name", "IRQn", "CATEGORY", "RESOURCE", "MESSAGE"]

# NammaAUTOSAR Parameters
OSEK_Params     = ["STATUS", "STARTUPHOOK", "ERRORHOOK", "SHUTDOWNHOOK", "PRETASKHOOK", "POSTTASKHOOK",
                   "USEGETSERVICEID", "USEPARAMETERACCESS", "USERESSCHEDULER"]
FreeOSEK_Params = ["OS_STACK_SIZE", "OS_CTX_SAVE_SZ", "IRQ_STACK_SIZE", "TASK_STACK_SIZE"]


if __name__ == '__main__':
	print("OSEK Builder Globals")
