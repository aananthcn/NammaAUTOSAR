#
# Created on Sun Oct 02 2022 10:09:37 AM
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
from os_builder.scripts.ob_globals import TaskParams, TNMI, MSGI

import colorama
from colorama import Fore, Back, Style


def generate_code(path, Tasks):
    # create header file
    filename = path + "/" + "sg_messages.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_SG_MESSAGES_H\n")
    hf.write("#define ACN_OSEK_SG_MESSAGES_H\n")
    hf.write("\n#include <osek.h>")
    hf.write("\n#include <osek_com.h>\n\n")

    # create source file
    filename = path + "/" + "sg_messages.c"
    cf = open(filename, "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include \"sg_messages.h\"\n")

    # collect & create all individual messages
    comment = "\n\n/*  Messages described in OIL file */\n"
    cf.write(comment)
    hf.write(comment)
    messages = []
    for task in Tasks:
        if TaskParams[MSGI] in task:
            for m in task[TaskParams[MSGI]]:
                if m not in messages:
                    messages.append(m)
                    cf.write("MessageType "+m+";\n")
                    hf.write("extern MessageType "+m+";\n")

    # print tasks message list
    comment = "\n\n/*  Messages lists for Tasks */\n"
    cf.write(comment)
    hf.write(comment)
    for task in Tasks:
        if TaskParams[MSGI] in task:
            hf.write("extern MessageType* "+task[TaskParams[TNMI]]+"_Messages[];\n")
            cf.write("MessageType* "+task[TaskParams[TNMI]]+"_Messages[] = {\n")
            max_i = len(task[TaskParams[MSGI]])
            i = 0
            for m in task[TaskParams[MSGI]]:
                i += 1
                cf.write("\t&"+m)
                if i != max_i:
                    cf.write(",\n")
                else:
                    cf.write("\n")
            cf.write("};\n\n")

    hf.write("\n\n#endif\n")
    hf.close()
    cf.close()


