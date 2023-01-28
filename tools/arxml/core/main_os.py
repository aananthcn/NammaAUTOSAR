#
# Created on Mon Aug 15 2022 1:49:28 PM
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
import sys
import xml.etree.ElementTree as ET


# Let us use the System Generator functions to parse ARXML and Generate code
sys.path.insert(0, os.getcwd()+"/tools/arxml")

import arxml.os.export_os as exp_os
import arxml.os.arxml_os as arxml_os
import arxml.core.lib as lib
import arxml.core.lib_conf as lib_conf
import arxml.core.lib_defs as lib_defs

import arxml.mcu.arxml_mcu as arxml_mcu



###############################################################################
# Main entry to ARXML gen / parse routines

def update_arxml(ar_file):
   # Following line is added to avoid ns0 prefix added
   ET.register_namespace('', "http://autosar.org/schema/r4.0")
   ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

   # print_ethif_configs(ethif_configs)

   # Read ARXML File
   tree = ET.parse(ar_file)
   root = tree.getroot()

   # locate ELEMENTS block, i.e., insert point
   ar_isp = lib_conf.find_ecuc_elements_block(root)

   # remove Os configs
   ethif_modconfs = lib_conf.find_module_configs("Os", ar_isp)
   if ethif_modconfs:
      ar_isp.remove(ethif_modconfs)

   # insert Os configs
   modconf = lib_conf.insert_ecuc_module_conf(ar_isp, "Os")

   # locate container
   containers = lib_conf.find_containers_in_modconf(modconf)
   if containers == None:
      print("Error: Os configs not updated due to internal error!!")
      return

   # Add Os contents to CONTAINER
   exp_os.export_appmodes_to_container(containers)
   exp_os.export_osos_to_container(containers) # sg.OS_Cfgs go in here
   exp_os.export_events_to_container(containers) # All events extracted from tasks go in here
   exp_os.export_counters_to_container(containers)
   exp_os.export_resources_to_container(containers)
   exp_os.export_tasks_to_container(containers)
   exp_os.export_alarms_to_container(containers)
   exp_os.export_isrs_to_container(containers)


   # Save ARXML contents to file
   ET.indent(tree, space="\t", level=0)
   tree.write(ar_file, encoding="utf-8", xml_declaration=True)
   lib.finalize_arxml_doc(ar_file)
   print("Info: Os Configs are updated to " + ar_file)



def export_os_cfgs_2_arxml(filepath, gui):
   # if file exists, then update the Os section only
   if os.path.isfile(filepath):
      update_arxml(filepath)
      return

   # file doesn't exist, check if path exists
   path = "/".join(filepath.split("/")[0:-1])
   if not os.path.exists(path):
      os.makedirs(path)
   
   root = ET.Element("AUTOSAR")
   lib.set_arxml_namespace(root)
   tree = ET.ElementTree(root)
   arpkgs = ET.SubElement(root, "AR-PACKAGES")
   
   # generate proper name for AR-PACKAGE
   arxml_pkgn = lib.setget_ecuc_arpkg_name(filepath)
   
   # Insert Ecuc_<name> AR-PACKAGE
   ci = len(list(root))
   arpkgs.insert(ci, ET.Comment("AR-Package: AUTOSAR"))
   arpkg = ET.SubElement(arpkgs, "AR-PACKAGE")
   shortname = ET.SubElement(arpkg, "SHORT-NAME")
   shortname.text = arxml_pkgn
   arpkg_elements = ET.SubElement(arpkg, "ELEMENTS")

   # for OS. This will be changed slowly in future - Aananth (17 Aug 2022 8:18 PM)
   exp_os.build_ecuc_os_package(arpkg_elements)

   ET.indent(tree, space="\t", level=0)
   tree.write(filepath, encoding="utf-8", xml_declaration=True)
   lib.finalize_arxml_doc(filepath)
   #print("Info: Configs are saved to " + filepath)
   
   arxml_mcu.update_arxml(filepath, gui.uc_info)



def import_arxml(filepath):
   # Check if file exists
   if not os.path.exists(filepath):
       print("Error: file \""+ filepath + "\" doesn't exist!")
       return -1
   # Check if it is a valid ARXML file
   with open(filepath) as f:
      lines = f.readlines()
      f.close()
      if not lines or "xml" not in lines[0]:
         print("Error: file \""+ filepath + "\" is not a valid ARXML file!")
         return -1
   arxml_os.parse_arxml(filepath)
   return 0



if __name__ == '__main__':
   print("main.py::__main__")