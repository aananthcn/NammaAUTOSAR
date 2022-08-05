from os_builder.scripts.common import print_info
from os_builder.scripts.ob_globals import ISR_Params

import colorama
from colorama import Fore, Back, Style


def generate_code(path, IsrData):
    # create header file
    filename = path + "/" + "sg_ivector.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_IVECTOR_H\n")
    hf.write("#define ACN_OSEK_IVECTOR_H\n")
    hf.write("\n#include <osek.h>\n")
    hf.write("#include <osek_com.h>\n")

    # create source file
    filename = path + "/" + "sg_ivector.c"
    cf = open(filename, "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include \"sg_ivector.h\"\n\n")
    
    # compute min & max interrupt vector number configured
    ivec_max = 0
    ivec_min = 9999999999999
    for isr in IsrData:
        if int(isr[ISR_Params[1]]) > ivec_max:
            ivec_max = int(isr[ISR_Params[1]])
        if int(isr[ISR_Params[1]]) < ivec_min:
            ivec_min = int(isr[ISR_Params[1]])
    
    hf.write("\n\n#define NUMBER_OF_IVECTORS \t("+str(len(IsrData))+")\n")
    hf.write("#define MAX_IVECTOR_NUMBER  \t("+str(ivec_max)+")\n")
    hf.write("#define MIN_IVECTOR_NUMBER  \t("+str(ivec_min)+")\n\n")
   
    # ISR handler declaration loop 
    for isr in IsrData:
        cf.write("extern void "+isr[ISR_Params[0]]+"(void);\n")
        
    # ISR handler array definition loop
    cf.write("\n/*  Interrupt Vector Handlers */\n")
    cf.write("void (*_IsrHandler[])(void) = {\n")
    for i in range(ivec_max+1):
        for isr in IsrData:
            match_found = False    
            if int(isr[ISR_Params[1]]) == i:
                cf.write("\t"+isr[ISR_Params[0]]+",\n")
                match_found = True
                break
        if not match_found:
            cf.write("\tNULL,\n")
    cf.write("};\n")
    hf.write("\nextern void (*_IsrHandler[])(void);\n")
    
    
    cf.close()
    hf.write("\n\n#endif\n")
    hf.close()
