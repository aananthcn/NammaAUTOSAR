from os_builder.scripts.common import print_info
from os_builder.scripts.ob_globals import TaskParams, TNMI

import colorama
from colorama import Fore, Back, Style


def print_appmode_enum(hf, am):
    hf.write("\n\nenum eAppModeType {\n")
    for m in am:
        hf.write("\t"+m+",\n")
    hf.write("\tOS_MODES_MAX\n")
    hf.write("};\n\n")


def generate_code(path, AppModes, Tasks):
    # create header file
    filename = path + "/" + "sg_appmodes.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_SG_APPMODES_H\n")
    hf.write("#define ACN_OSEK_SG_APPMODES_H\n")
    hf.write("\n#include <osek.h>\n")
    hf.write("#include <osek_com.h>\n")
    print_appmode_enum(hf, AppModes)

    # create source file
    filename = path + "/" + "sg_appmodes.c"
    cf = open(filename, "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include \"sg_appmodes.h\"\n\n")
    cf.write("\n/*  Task AppModes */\n")
    for task in Tasks:
        if "AUTOSTART_APPMODE" in task:
            cf.write("const AppModeType "+task[TaskParams[TNMI]]+"_AppModes[] = {\n")
            max_i = len(task["AUTOSTART_APPMODE"])
            i = 0
            for m in task["AUTOSTART_APPMODE"]:
                i += 1
                cf.write("\t"+m)
                if i != max_i:
                    cf.write(",\n")
                else:
                    cf.write("\n")
            cf.write("};\n\n")
            hf.write("extern const AppModeType "+task[TaskParams[TNMI]]+"_AppModes[];\n")
        #else:
        #    cf.write("const AppModeType* "+task[TaskParams[TNMI]]+"_AppModes = NULL;\n\n")
        #    hf.write("extern const AppModeType* "+task[TaskParams[TNMI]]+"_AppModes;\n")

    cf.close()
    hf.write("\n\n#endif\n")
    hf.close()
