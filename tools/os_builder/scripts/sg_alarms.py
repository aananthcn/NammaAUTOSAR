from os_builder.scripts.common import print_info
from os_builder.scripts.ob_globals import AlarmParams, ANME, AAAT, AAT1, AAT2, AIAS, ATIM, ACYT, ACNT
from os_builder.scripts.ob_globals import CntrParams, CNME
from os_builder.scripts.ob_globals import TaskParams, TNMI

import colorama
from colorama import Fore, Back, Style


C_AlarmAction_Type = "\n\ntypedef enum {\n\
    AAT_ACTIVATETASK,\n\
    AAT_SETEVENT,\n\
    AAT_ALARMCALLBACK,\n\
    AAT_MAX_TYPE\n\
} AlarmActionType;\n"


AAT_PyList = {
    "OsAlarmActivateTask" : "AAT_ACTIVATETASK", # AUTOSAR
    "ACTIVATETASK" : "AAT_ACTIVATETASK",        # OSEK
    "OsAlarmSetEvent" : "AAT_SETEVENT",         # AUTOSAR
    "SETEVENT" : "AAT_SETEVENT",                # OSEK
    "OsAlarmCallback" : "AAT_ALARMCALLBACK",    # AUTOSAR
    "ALARMCALLBACK" : "AAT_ALARMCALLBACK"       # OSEK
}


C_Alarm_Type = "\n\ntypedef struct {\n\
    char* name;                     /* short name of alarm */ \n\
    AlarmType cntr_id;              /* OS Counter ID (= index of _OsCounters + 1) */ \n\
    TickType* pacntr;               /* pointer to _AppAlarmCounters */ \n\
    TickType* pcycle;               /* pointer to AppAlarmCycle */ \n\
    bool* palrm_state;              /* pointer to the state of _AppAlarmCounters */ \n\
    AlarmActionType aat;            /* Refer enum AlarmActionType */ \n\
    intptr_t aat_arg1;              /* arg1: task_name | callback_fun */\n\
    intptr_t aat_arg2;              /* arg2: event | NULL */\n\
    bool is_autostart;              /* does this alarm start at startup? */\n\
    u32 alarmtime;                  /* when does it expire? */\n\
    u32 cycletime;                  /* cyclic time - for repetition */\n\
    const AppModeType* appmodes;    /* alarm active in which modes? */\n\
    u32 n_appmodes;                 /* how may appmodes for this entry? */\n\
} AppAlarmType;\n\n"


def get_task_id(Tasks, taskName):
    retval = "TASK_ID_MAX"
    for i, task in enumerate(Tasks):
        if task[TaskParams[TNMI]] == taskName:
            retval = str(i)
            break
    return retval


def get_counter_id(Counters, cntrName):
    retval = "OS_MAX_COUNTERS"
    for i, cntr in enumerate(Counters):
        if cntr[CntrParams[CNME]] == cntrName:
            retval = str(i)
            break
    return retval


def alarm_action_type_args(aat, alarm, cf, hf, Tasks):
    aat_arg1 = str(alarm[AlarmParams[AAT1]]).replace('"','')

    if aat == "ACTIVATETASK" or aat == "OsAlarmActivateTask":
        if AlarmParams[AAT1] in alarm:
            cf.write("\t\t.aat_arg1 = (intptr_t) "+get_task_id(Tasks, aat_arg1)+",\n")
        else:
            print(Fore.RED+"Error: Task to activate for alarm: "+alarm[AlarmParams[ANME]]+" not configured!\n")
            cf.write("\t\t.aat_arg1 = (intptr_t)NULL,\n")

        # for ACTIVATETASK type, arg2 is not required
        cf.write("\t\t.aat_arg2 = (intptr_t)NULL,\n")

    elif aat == "SETEVENT" or aat == "OsAlarmSetEvent":
        if AlarmParams[AAT1] in alarm:
            cf.write("\t\t.aat_arg1 = (intptr_t) "+get_task_id(Tasks, aat_arg1)+",\n")
        else:
            print(Fore.RED+"Error: Task to activate for alarm: "+alarm[AlarmParams[ANME]]+" not configured!\n")
        if AlarmParams[AAT2] in alarm:
            cf.write("\t\t.aat_arg2 = (intptr_t) OS_EVENT("+aat_arg1+", "+alarm[AlarmParams[AAT2]]+"),\n")
        else:
            print(Fore.RED+"Error: Event to trigger for alarm: "+alarm[AlarmParams[ANME]]+" not configured!\n")
            cf.write("\t\t.aat_arg2 = (intptr_t)NULL,\n")

    elif aat == "ALARMCALLBACK" or aat == "OsAlarmCallback":
        if AlarmParams[AAT1] in alarm:
            cf.write("\t\t.aat_arg1 = (intptr_t)"+aat_arg1+",\n")
        else:
            print(Fore.RED+"Error: Callback for alarm: "+alarm[AlarmParams[ANME]]+" not configured!\n")

        # for ALARMCALLBACK type, arg2 is not required
        cf.write("\t\t.aat_arg2 = (intptr_t)NULL,\n")

        # declare call back function here. Definition will be part of "app"
        hf.write("extern void "+ aat_arg1 +"(void);\n")

    else:
        print(Fore.RED+"Error: Unknown action type for alarm: "+alarm[AlarmParams[ANME]]+"!\n")
        print("\n\n",aat, "\n\n")



C_AlarmCtrlBlock_Type = "\n\ntypedef struct {\n\
    const AppAlarmType* alarm;\n\
    u32 len;\n\
} AppAlarmCtrlBlockType;\n\n"


def generate_code(path, Alarms, Counters, Tasks):
    print_info("Generating code for Alarms")

    # create header file
    filename = path + "/" + "sg_alarms.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_SG_ALARMS_H\n")
    hf.write("#define ACN_OSEK_SG_ALARMS_H\n")
    hf.write("#include <osek.h>\n")
    hf.write(C_AlarmAction_Type)
    hf.write(C_Alarm_Type)

    # create source file
    filename = path + "/" + "sg_alarms.c"
    cf = open(filename, "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include <stdbool.h>\n")
    cf.write("#include \"sg_alarms.h\"\n")
    cf.write("#include \"sg_appmodes.h\"\n")
    cf.write("#include \"sg_tasks.h\"\n")
    cf.write("#include \"sg_events.h\"\n")

    # define app mode structure and macros first
    cf.write("\n\n#define TRUE    true\n#define FALSE    false");
    cf.write("\n\n/*   A P P M O D E S   F O R   A L A R M S   */\n")
    new_line_for_app_alarm = False
    for alarm in Alarms:
        if "APPMODE[]" in alarm:
            max_i = len(alarm["APPMODE[]"])
            # this block is added to beautify sg_alarms.h :-)
            if not new_line_for_app_alarm:
                new_line_for_app_alarm = True
            cf.write("#define ALARM_"+alarm[AlarmParams[ANME]].upper()+"_APPMODES_MAX ("+str(max_i)+")\n")
            cf.write("const AppModeType Alarm_"+alarm[AlarmParams[ANME]]+"_AppModes[] = {\n")
            i = 0
            for m in alarm["APPMODE[]"]:
                i += 1
                cf.write("\t"+m)
                if i != max_i:
                    cf.write(",\n")
                else:
                    cf.write("\n")
            cf.write("};\n\n")
            hf.write("extern const AppModeType Alarm_"+alarm[AlarmParams[ANME]]+"_AppModes[];\n")

    # compute how many times each counters are used in alarms
    CounterSizeList = {}
    for alarm in Alarms:
        if alarm[AlarmParams[ACNT]] not in CounterSizeList:
            CounterSizeList[alarm[AlarmParams[ACNT]]] = 1
        else:
            CounterSizeList[alarm[AlarmParams[ACNT]]] += 1
    hf.write(C_AlarmCtrlBlock_Type);
    hf.write("\n#define MAX_APP_ALARMS  ("+str(len(CounterSizeList))+")\n")
    hf.write("extern const AppAlarmCtrlBlockType _AppAlarms[MAX_APP_ALARMS];\n")
    hf.write("#define MAX_APP_ALARM_COUNTERS    ("+str(len(Alarms))+")\n")
    hf.write("extern TickType _AppAlarmCounters[MAX_APP_ALARM_COUNTERS];\n")
    hf.write("extern TickType _AppAlarmCycles[MAX_APP_ALARM_COUNTERS];\n")
    hf.write("extern bool _AppAlarmStates[MAX_APP_ALARM_COUNTERS];\n")
    if new_line_for_app_alarm:
        hf.write("\n\n") # beautify sg_alarms.h

    # define the alarms configured in OSEK builder or oil file
    cf.write("\n/*   A L A R M S   D E F I N I T I O N S   */\n")
    cf.write("TickType _AppAlarmCounters[MAX_APP_ALARM_COUNTERS];\n")
    cf.write("TickType _AppAlarmCycles[MAX_APP_ALARM_COUNTERS];\n")
    cf.write("bool _AppAlarmStates[MAX_APP_ALARM_COUNTERS];\n")
    for i, cntr in enumerate(Counters):
        cf.write("const AppAlarmType AppAlarms_"+cntr[CntrParams[CNME]]+"[] = {\n")
        print_count = 0
        for j, alarm in enumerate(Alarms):
            if cntr[CntrParams[CNME]] != alarm[AlarmParams[ACNT]]:
                continue
            cf.write("\t{\n")
            cf.write("\t\t.name = \""+alarm[AlarmParams[ANME]]+"\",\n")
            cf.write("\t\t.cntr_id = "+str(i)+",\n")
            cf.write("\t\t.pacntr = &_AppAlarmCounters["+str(j)+"],\n")
            cf.write("\t\t.pcycle = &_AppAlarmCycles["+str(j)+"],\n")
            cf.write("\t\t.palrm_state = &_AppAlarmStates["+str(j)+"],\n")
            alarmActionType = alarm[AlarmParams[AAAT]]
            cf.write("\t\t.aat = "+AAT_PyList[alarmActionType]+",\n")

            alarm_action_type_args(alarmActionType, alarm, cf, hf, Tasks)

            cf.write("\t\t.is_autostart = "+alarm[AlarmParams[AIAS]]+",\n")
            if AlarmParams[ATIM] in alarm:
                cf.write("\t\t.alarmtime = "+str(alarm[AlarmParams[ATIM]])+",\n")
            else:
                cf.write("\t\t.alarmtime = 0,\n")
            if AlarmParams[ACYT] in alarm:
                cf.write("\t\t.cycletime = "+str(alarm[AlarmParams[ACYT]])+",\n")
            else:
                cf.write("\t\t.cycletime = 0,\n")

            if "APPMODE[]" in alarm:
                cf.write("\t\t.n_appmodes = ALARM_"+alarm[AlarmParams[ANME]].upper()+"_APPMODES_MAX,\n")
                cf.write("\t\t.appmodes = (const AppModeType *) &Alarm_"+alarm[AlarmParams[ANME]]+"_AppModes\n")
            else:
                cf.write("\t\t.n_appmodes = 0,\n")
                cf.write("\t\t.appmodes = NULL\n")

            cf.write("\t}")

            # if this is the last element in this list, then don't print a comma
            print_count += 1
            if print_count < CounterSizeList[alarm[AlarmParams[ACNT]]]:
                cf.write(",\n")
            else:
                cf.write("\n")
        # for alarms loop
        cf.write("};\n\n")


    # define _AppAlarms[];
    cf.write("\nconst AppAlarmCtrlBlockType _AppAlarms[] = {\n")
    for cntr in Counters:
        cf.write("\t{\n")
        cf.write("\t\t.alarm = (const AppAlarmType *) &AppAlarms_"+cntr[CntrParams[CNME]]+",\n")
        cf.write("\t\t.len = "+str(CounterSizeList[cntr[CntrParams[CNME]]])+"\n")
        cf.write("\t},\n")
    cf.write("};\n\n")

    # define AlarmID to CounterID mapping
    hf.write("\nextern const AlarmType _AlarmID2CounterID_map[];")
    cf.write("\nconst AlarmType _AlarmID2CounterID_map[] = {\n\t")
    for alarm in Alarms:
        cf.write(get_counter_id(Counters, alarm[AlarmParams[ACNT]])+", ")
    cf.write("\n};\n")

    hf.write("\n\n#endif\n")
    hf.close()
    cf.close()
