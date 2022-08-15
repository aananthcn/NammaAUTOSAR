#
# Created on Mon Aug 15 2022 1:48:14 PM
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
import xml.etree.ElementTree as ET
import arxml.core.lib as lib



def update_arxml(ar_file, uc_info):
    ar_pkg = lib.find_ar_package("Ecuc", ar_file)
    if ar_pkg == None:
        print("Error: couldn't find Ecuc, hence can't update MicroC info to ARXML!")
        return
    
    # Now find insertion point
    for item in list(ar_pkg):
        if lib.get_tag(item) == "ELEMENTS":
            ar_isp = item # insertion point
            break 
    if ar_isp == None:
        print("Error: couldn't find ELEMENTS in AR-PACKAGE, hence can't update MicroC info to ARXML!")
        return
        
    # Now find if Mcu module-conf is already there in insertion-point
    modconf = lib.find_modconf("Mcu", ar_isp)
    if modconf == None:
        print("Mcu not found in "+ ar_file)
    else:
        print("Mcu found in "+ ar_file)
    print("update_arxml() is under construction!")



def parse_arxml(filepath):
   tree = ET.parse(filepath)
   root = tree.getroot()
   modconf, cntainr = get_ecuc_tree(root)
   print("Mcu parse_arxml() is under construction!")
   for cv in cntainr:
      dref = lib.get_dref_from_container(cv)
      print(dref)