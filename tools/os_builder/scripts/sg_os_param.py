from os_builder.scripts.common import print_info
from os_builder.scripts.ob_globals import FreeOSEK_Params

import colorama
from colorama import Fore, Back, Style


def generate_code(path, OsParams):
    print_info("Generating code for FreeOSEK Parameters")

    # create stack definitions
    lfilename = path + "/" + "sg_stack.lds"
    hfilename = path + "/" + "sg_os_param.h"
    lf = open(lfilename, "w")
    hf = open(hfilename, "w")

    hf.write("#ifndef ACN_OSEK_OS_PARAM_H\n")
    hf.write("#define ACN_OSEK_OS_PARAM_H\n")
    hf.write("\n\n")

    # generate code from OsParams but limited to FreeOSEK_Params (ignore others)
    for param in FreeOSEK_Params:
        lf.write("_"+param + " = " + OsParams[param] + ";\n")
        hf.write("#define _"+param + "  \t(" + OsParams[param] + ")\n")
    
    lf.close()
    hf.write("\n\n#endif\n")
    hf.close()
