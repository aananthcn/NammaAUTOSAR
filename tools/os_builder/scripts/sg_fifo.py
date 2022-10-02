#
# Created on Sun Oct 02 2022 10:09:20 AM
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
from os_builder.scripts.ob_globals import TaskParams, TNMI, PRII, ACTI

import colorama
from colorama import Fore, Back, Style


def populate_queue(f, qstr, maxPrio, fifoInfo):
    f.write("const OsFifoType* "+qstr+"Queue[] = {\n")
    for prio in range(maxPrio+1):
        if str(prio) in fifoInfo:
            f.write("\t&"+qstr+"Fifo_"+str(prio))
        else:
            f.write("\tNULL")
        if prio != maxPrio:
            f.write(",\n")
        else:
            f.write("\n")
    f.write("};\n\n")


def compute_qsize_from_ceil_prio(prio, ResTaskList):
    qsize = 0
    for rt in ResTaskList:
        if rt["ceil_prio"] == prio:
            qsize += rt["n_tasks"]
    return qsize


def generate_code(path, Tasks, ResTaskList):
    print_info("Generating code for OS FIFO queue generation")
    maxPrio = 0
    fifoInfo = {}
    for task in Tasks:
        prio = int(task[TaskParams[PRII]])
        if  prio > maxPrio:
            maxPrio = prio
        if str(task[TaskParams[PRII]]) not in fifoInfo:
            fifoInfo[task[TaskParams[PRII]]] = int(task[TaskParams[ACTI]])
        else:
            fifoInfo[task[TaskParams[PRII]]] += int(task[TaskParams[ACTI]])


    # create header file
    filename = path + "/" + "sg_fifo.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_SG_FIFO_H\n")
    hf.write("#define ACN_OSEK_SG_FIFO_H\n")
    hf.write("\n#include <os_fifo.h>\n")
    hf.write("\n\n#define SG_FIFO_QUEUE_MAX_LEN   ("+str(maxPrio+1)+")\n\n")

    # print queue declarations
    hf.write("extern const OsFifoType* ReadyQueue[];\n")


    # create source file
    filename = path + "/" + "sg_fifo.c"
    cf = open(filename, "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include \"sg_fifo.h\"\n")
    cf.write("\n/* Allocate Buffers in RAM */\n")

    # 1st level declarations and definitions
    for prio in range(maxPrio+1):
        qsize = cp_qsize = 0
        if str(prio) in fifoInfo:
            qsize = fifoInfo[str(prio)]
            # here the tasks that will be running at elevated priority is added.
            cp_qsize = compute_qsize_from_ceil_prio(prio, ResTaskList)

        # remove redundant counts (from ceil_prio calc.) in qsize
        if cp_qsize > qsize:
            qsize = cp_qsize
        
        # print queue definitions
        if qsize > 0:
            cf.write("#define READY_TASKS_"+str(prio)+"_SIZE ("+str(qsize)+")\n")
            cf.write("OsTaskType* ReadyTasks_"+str(prio)+"[READY_TASKS_"+str(prio)+"_SIZE];\n")
    cf.write("\nOsTaskType* RunningTasks[1];\n")


    # 2nd level - define FIFOs
    cf.write("\n\n/* Allocate FIFO queues in RAM */")
    for prio in range(maxPrio+1):
        qsize = 0
        if str(prio) in fifoInfo:
            qsize = fifoInfo[str(prio)]
        if qsize == 0:
            continue
        cf.write("\nOsFifoType ReadyFifo_"+str(prio)+" = {\n")
        cf.write("\t.task = ReadyTasks_"+str(prio)+",\n")
        cf.write("\t.size = READY_TASKS_"+str(prio)+"_SIZE,\n")
        cf.write("\t.head = 0,\n")
        cf.write("\t.tail = 0,\n")
        cf.write("#ifdef DEBUG\n")
        cf.write("\t.name = \"ReadyFifo_"+str(prio)+"\",\n")
        cf.write("#endif\n")
        cf.write("\t.full = false\n")
        cf.write("};\n")
        cf.write("\n")

    # RunningFifo is a special case, as there can be max 1 task running at any
    # given point of time. Hence Queue is not generated for RunningFifo

    # populate waiting queue
    cf.write("\n\n/* Prioritized OSEK FIFO queues in Flash */\n")
    populate_queue(cf, "Ready", maxPrio, fifoInfo)


    hf.write("\n\n#endif\n")
    hf.close()
    cf.close()
