#
# Created on Sun Oct 02 2022 10:09:50 AM
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
from os_builder.scripts.ob_globals import FreeOSEK_Params

import colorama
from colorama import Fore, Back, Style


def generate_code(path, OsParams):
    print_info("Generating code for NammaAUTOSAR Parameters")

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
