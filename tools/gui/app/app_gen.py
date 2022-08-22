#
# Created on Mon Aug 22 2022 8:03:11 PM
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
import utils.search as search
import os


def create_source(app_name):
    cwd = os.getcwd()
    f = open(cwd+"/Makefile", "r")
    makefile = f.readlines()
    f.close()
    
    app_path = search.find_dir(app_name, cwd)
    app_path_def = app_name.upper()+"_PATH := "+app_path+"\n"
    mk_file = search.find_file_ext("mk", app_path)
    mk_file_inc ="include "+mk_file+"\n"
    
    def_insert = False
    mk_insert = False
    
    for i, line in enumerate(makefile):
        if line[0] == "#" and "Definitions" in line and not def_insert:
            makefile.insert(i+1, app_path_def)
            def_insert = True
        if line[0] == "#" and "Inclusions" in line and not mk_insert:
            makefile.insert(i+1, mk_file_inc)
            mk_insert = True

    f = open(cwd+"/Makefile", "w")
    makefile = "".join(makefile)
    f.write(makefile)
    f.close()