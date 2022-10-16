#
# Created on Sun Oct 02 2022 10:09:44 AM
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
from os_builder.scripts.common import print_info
from os_builder.scripts.ob_globals import TaskParams, TNMI, RESI, PRII, ACTI

import colorama
from colorama import Fore, Back, Style


OsResMapType_str = "\n\n\n\
typedef struct {\n\
    ResourceType* res;\n\
    u16 ceil_prio;\n\
    u16 n_tasks;\n\
    const TaskType* task_ids;\n\
} OsResMapType;\n\
\n\
extern const OsResMapType _OsResList[];\n\n\n"


def generate_code(path, Tasks):
    print_info("Generating code for Resources")

    # create header file
    filename = path + "/" + "sg_resources.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_SG_RESOURCES_H\n")
    hf.write("#define ACN_OSEK_SG_RESOURCES_H\n")
    hf.write("\n#include <osek.h>")

    # create source file
    filename = path + "/" + "sg_resources.c"
    cf = open(filename, "w")
    cf.write("#include <stddef.h>\n")
    cf.write("\n")
    cf.write("#include \"sg_resources.h\"\n")
    cf.write("#include \"sg_tasks.h\"\n")

    # collect & create all individual resources
    Resources = []
    hf.write("\n\n\n#define RES(x)  RES_##x\n")
    hf.write("\ntypedef enum {\n")
    for task in Tasks:
        if TaskParams[RESI] in task and task[TaskParams[RESI]]:
            for r in task[TaskParams[RESI]]:
                if r not in Resources:
                    Resources.append(r)
                    hf.write("\tRES_"+r+",\n")
    hf.write("\tMAX_RESOURCE_ID\n} OsResourcesType;")
    hf.write(OsResMapType_str)

    # Resources in RAM
    cf.write("\n\n\n/* Resources Definitions in RAM */\n")
    for res in Resources:
        cf.write("ResourceType " + str(res) + ";\n")

    # Const Resource Structure for OS kernel
    comment = "\n\n/*  Resources lists for Tasks */\n"
    cf.write(comment)
    ResTaskList = []
    for res in Resources:
        # Parse and collect tasks associated with "res"
        TaskData = {}
        task_cnt = 0
        ceil_prio = 0
        task_lst = []
        for task in Tasks:
            if TaskParams[RESI] in task and task[TaskParams[RESI]]:
                for r in task[TaskParams[RESI]]:
                    if str(r) == str(res):
                        task_cnt += int(task[TaskParams[ACTI]])
                        if int(task[TaskParams[PRII]]) > ceil_prio:
                            ceil_prio = int(task[TaskParams[PRII]])
                        task_lst.append(task[TaskParams[TNMI]])
        TaskData["res"] = str(res)
        TaskData["n_tasks"] = task_cnt
        TaskData["ceil_prio"] = ceil_prio
        TaskData["tasks"] = task_lst
        ResTaskList.append(TaskData)

    # Create C structures with the parsed tasks
    for rt in ResTaskList:
        cf.write("const TaskType "+ rt["res"]+"_tasks[] = {\n")
        for t in rt["tasks"]:
            cf.write("\tTASK_"+t.upper()+"_ID,\n")
        cf.write("};\n\n")

    cf.write("const OsResMapType _OsResList[MAX_RESOURCE_ID] = {\n")
    for rt in ResTaskList:
        cf.write("\t{\n\t\t.res = &"+rt["res"]+",\n")
        hf.write("DeclareResource("+rt["res"]+");\n")
        cf.write("\t\t.ceil_prio = "+ str(rt["ceil_prio"])+",\n")
        cf.write("\t\t.n_tasks = "+ str(rt["n_tasks"])+",\n")
        cf.write("\t\t.task_ids = " + rt["res"]+"_tasks\n")
        cf.write("\t},\n")
    cf.write("};\n")

    hf.write("\n\n#endif\n")
    hf.close()
    cf.close()

    return ResTaskList


