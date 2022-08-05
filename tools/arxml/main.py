import os
import sys
import xml.etree.ElementTree as ET


# Let us use the System Generator functions to parse ARXML and Generate code
sys.path.insert(0, os.getcwd()+"/tools/arxml")

import arxml.os.export as imp
import arxml.os.ecuc as ecuc
import arxml.lib as lib

###############################################################################
# Main entry to ARXML gen / parse routines



def export_arxml(filepath):
   path = "/".join(filepath.split("/")[0:-1])
   if not os.path.exists(path):
      os.makedirs(path)
   
   root = ET.Element("AUTOSAR")
   root.set("xmlns", "http://autosar.org/schema/r4.0")
   root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
   root.set("xsi:schemaLocation", "http://autosar.org/schema/r4.0 autosar.xsd")
   tree = ET.ElementTree(root)
   arpkgs = ET.SubElement(root, "AR-PACKAGES")
   imp.build_ecuc_os_package(arpkgs, "Ecuc")

   ET.indent(tree, space="\t", level=0)
   tree.write(filepath, encoding="utf-8", xml_declaration=True)
   lib.finalize_arxml_doc(filepath)
   print("Info: Configs are saved to " + filepath)



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
   ecuc.parse_arxml(filepath)
   return 0



if __name__ == '__main__':
   print("main.py::__main__")