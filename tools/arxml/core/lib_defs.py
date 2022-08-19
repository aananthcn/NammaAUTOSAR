#
# Created on Fri Aug 19 2022 11:51:28 AM
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

from arxml.core.lib import *


def insert_module_ref(root, mod_name):
   ecu_def_cltn = None
   mrefs = None

   # Module references are inside Ecuc def. collection, hence locate that first
   for item in list(root):
      if get_tag(item) == "ECUC-DEFINITION-COLLECTION":
         ecu_def_cltn = item
         break

   # Insert Ecuc Def. Collection node if it doesn't exist.
   if ecu_def_cltn == None:
      ecu_def_cltn = ET.SubElement(root, "ECUC-DEFINITION-COLLECTION")
      ecu_def_cltn.set("UUID", "ECUC:ECUC-DEFINITION-COLLECTION")
      shortname = ET.SubElement(ecu_def_cltn, "SHORT-NAME")
      shortname.text = "AUTOSARParameterDefinition"
      mrefs = ET.SubElement(ecu_def_cltn, "MODULE-REFS")

   # for new file, mrefs will be initialized in above line. Else search it
   if mrefs == None:
      for item in list(ecu_def_cltn):
         if get_tag(item) == "MODULE-REFS":
            mrefs = item
            break   

   # Check if the module ref is already present in definition collection
   mref = find_module_ref(mod_name, ecu_def_cltn)
   if mref != None:
      print("Module reference for "+mod_name+" is already present in ECUC-DEFINITION-COLLECTION!")
      return

   # Insert mod_name to MODULE-REFS node
   mref =  ET.SubElement(mrefs, "MODULE-REF")
   mref.set("DEST", "ECUC-MODULE-DEF")
   mref.text = "/AUTOSAR/EcucDefs/"+mod_name



def insert_admin_data(root, version):
   adm_data = ET.SubElement(root, "ADMIN-DATA")
   doc_revs = ET.SubElement(adm_data, "DOC-REVISIONS")
   doc_rev = ET.SubElement(doc_revs, "DOC-REVISION")
   rev_label = ET.SubElement(doc_rev, "REVISION-LABEL")
   rev_label.text = version
   issued_by = ET.SubElement(doc_rev, "ISSUED-BY")
   issued_by.text = "AUTOSAR"



def insert_module_def(root, module_name):
   # First add a module reference
   insert_module_ref(root, module_name)

   # Then add module definitions node
   mod_def = ET.SubElement(root, "ECUC-MODULE-DEF")
   mod_def.set("UUID", "ECUC:"+module_name)
   shortname = ET.SubElement(mod_def, "SHORT-NAME")
   shortname.text = module_name
   insert_admin_data(mod_def, "4.6.0")
   item = ET.SubElement(mod_def, "LOWER-MULTIPLICITY")
   item.text = "0"
   item = ET.SubElement(mod_def, "UPPER-MULTIPLICITY")
   item.text = "1"
   item = ET.SubElement(mod_def, "POST-BUILD-VARIANT-SUPPORT")
   item.text = "false"
   cfg_vars = ET.SubElement(mod_def, "SUPPORTED-CONFIG-VARIANTS")
   cfg_var = ET.SubElement(cfg_vars, "SUPPORTED-CONFIG-VARIANT")
   cfg_var.text = "VARIANT-PRE-COMPILE"

   # Create CONTAINER element and export module (Os, Mcu, ...) objects.
   containers = ET.SubElement(mod_def, "CONTAINERS")

   return containers



def insert_param_container_def(root, name):
   if get_tag(root) != "CONTAINERS":
      print("Error: insert_param_container_def's root argument is not \"CONTAINERS\"")
      return
	   
   ci = len(list(root))
   root.insert(ci, ET.Comment("Container Definition: "+name))
   
   ctnr = ET.SubElement(root, "ECUC-PARAM-CONF-CONTAINER-DEF")
   ctnr.set("UUID", "ECUC:"+name)
   shortname = ET.SubElement(ctnr, "SHORT-NAME")
   shortname.text = name
   item      = ET.SubElement(ctnr, "LOWER-MULTIPLICITY")
   item.text = "0"
   item      = ET.SubElement(ctnr, "UPPER-MULTIPLICITY")
   item.text = "1"
   params    = ET.SubElement(ctnr, "PARAMETERS")
   refs      = ET.SubElement(ctnr, "REFERENCES")




#####################################
# Search Functions
#####################################
# arg2: root is ELEMENTS block inside AR-PACKAGE named EcucDefs (in ver R20-11)
def find_module_def(shortname, root):
   modconf = None
   
   if get_tag(root) == "ELEMENTS":
      for elem in list(root):
         if get_tag(elem) == "ECUC-MODULE-DEF":
            for item in list(elem):
               if get_tag(item) == "SHORT-NAME":
                  if item.text == shortname:
                     modconf = elem
                     break
                  
   return modconf



# arg2: root is ECUC-DEFINITION-COLLECTION block (in ver R20-11)
def find_module_ref(shortname, root):
   modref = None

   if get_tag(root) == "ECUC-DEFINITION-COLLECTION":
      for item in list(root):
         if get_tag(item) == "MODULE-REFS":
            for ref in list(item):
               if shortname in ref.text:
                  modref = ref
                  break

   return modref



# arg2: root is CONTAINERS block within ECUC_MODULE_DEF
def find_param_container_def(shortname, root):
   ctnrdef = None

   if get_tag(root) == "CONTAINERS":
      for item in list(root):
         if get_tag(item) == "ECUC-PARAM-CONF-CONTAINER-DEF":
            for cdef in list(item):
               if shortname in cdef.text:
                  ctnrdef = cdef
                  break

   return ctnrdef