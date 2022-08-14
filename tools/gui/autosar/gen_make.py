#
# Created on Sat Aug 13 2022 10:19:54 PM
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
import os


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)



def create_makefile(gui):
    cwd = os.getcwd()
    makefile = open(cwd+"/Makefile", "w")
    makefile.write("CWD := "+cwd+"\n")
    
    micro_mk = find(gui.micro+".mk", cwd)
    makefile.write("include "+micro_mk+"\n")
    microarch_mk = find(gui.micro_arch+".mk", cwd)
    makefile.write("include "+microarch_mk+"\n")
 
    os_objs_mk = find("os-objs.mk", cwd)
    makefile.write("include "+os_objs_mk+"\n")
    os_common_mk = find("os-common.mk", cwd)
    makefile.write("include "+os_common_mk+"\n")
    
    makefile.close()