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



# Update ARXML with Micro Controller Info only.
def update_arxml(ar_file, uc_info):
    # Following line is added to avoid ns0 prefix added
    ET.register_namespace('', "http://autosar.org/schema/r4.0")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()
 
    McuDefs_InsPt = "EcucDefs"
    ar_pkg = lib.find_ar_package(McuDefs_InsPt, root)
    if ar_pkg == None:
        print("Error: couldn't find "+McuDefs_InsPt+" hence can't update MicroC info to ARXML!")
        return
    
    # Now find insertion point
    ar_isp = None
    for item in list(ar_pkg):
        if lib.get_tag(item) == "ELEMENTS":
            ar_isp = item # insertion point
            break 
    if ar_isp == None:
        print("Error: couldn't find ELEMENTS in AR-PACKAGE, hence can't update MicroC info to ARXML!")
        return
        
    # Now find if Mcu module-conf is already there in insertion-point
    modname = "Mcu"
    moddef = lib.find_module_def(modname, ar_isp)
    if moddef == None:
        container = lib.insert_module_def(ar_isp, modname)
        print("Mcu node not found!")
    else:
        for item in list(moddef):
            if lib.get_tag(item) == "CONTAINERS":
                container = item
                break
    if container == None:
        print("Error: couldn't find CONTAINER in ECUC-MODULE-DEF for "+modname)
        return

    # Add Uc_Info contents to CONTAINER
    # TODO: TBD

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: Micro Controller Configs are saved to " + ar_file)    



# This function is highly incomplete.....
def parse_arxml(filepath):
   tree = ET.parse(filepath)
   root = tree.getroot()
   modconf, cntainr = get_ecuc_tree(root)
   print("Mcu parse_arxml() is under construction!")
   for cv in cntainr:
      dref = lib.get_dref_from_container(cv)
      print(dref)