#
# Created on Fri Aug 19 2022 11:51:00 AM
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


def insert_ecuc_module_conf(element_node, module_name):
    # Comment block
    ci = len(list(element_node))
    element_node.insert(ci, ET.Comment("Module Configuration: "+module_name))
    
    # ECUC Module Configuration
    mod_conf = ET.SubElement(element_node, "ECUC-MODULE-CONFIGURATION-VALUES")
    shortname = ET.SubElement(mod_conf, "SHORT-NAME")
    shortname.text = module_name
    def_ref = ET.SubElement(mod_conf, "DEFINITION-REF", DEST="ECUC-MODULE-DEF")
    def_ref.text = "/AUTOSAR/EcucDefs/"+module_name
    ecu_def_edition = ET.SubElement(mod_conf, "ECUC-DEF-EDITION")
    ecu_def_edition.text = "4.2.0"
    impl_cfg_var = ET.SubElement(mod_conf, "IMPLEMENTATION-CONFIG-VARIANT")
    impl_cfg_var.text = "VARIANT-PRE-COMPILE"

    # Create CONTAINER folder for adding parameters later.
    containers = ET.SubElement(mod_conf, "CONTAINERS")

    return mod_conf



def insert_conf_container(root, name, ctnr_type, dref):
   ctnr = ET.SubElement(root, "ECUC-CONTAINER-VALUE")
   shortname = ET.SubElement(ctnr, "SHORT-NAME")
   shortname.text = name
   if ctnr_type == "conf":
      def_ref = ET.SubElement(ctnr, "DEFINITION-REF", DEST="ECUC-PARAM-CONF-CONTAINER-DEF")
   elif ctnr_type == "choice":
      def_ref = ET.SubElement(ctnr, "DEFINITION-REF", DEST="ECUC-CHOICE-CONTAINER-DEF")
   else:
      def_ref = ET.SubElement(ctnr, "DEFINITION-REF", DEST="ERROR-INVALID_TYPE")
   def_ref.text = dref
   return ctnr



def insert_conf_reference(root, dref, vref):
   rctnr = ET.SubElement(root, "ECUC-REFERENCE-VALUE")
   def_ref = ET.SubElement(rctnr, "DEFINITION-REF", DEST="ECUC-REFERENCE-DEF")
   def_ref.text = dref
   val_ref = ET.SubElement(rctnr, "VALUE-REF", DEST="ECUC-CONTAINER-VALUE")
   val_ref.text = vref
   return rctnr



def insert_conf_param(root, refname, paramtype, subtype, value):
   if paramtype == "text":
      param_blk = ET.SubElement(root, "ECUC-TEXTUAL-PARAM-VALUE")
   elif paramtype == "numerical":
      param_blk = ET.SubElement(root, "ECUC-NUMERICAL-PARAM-VALUE")
   else:
      param_blk = ET.SubElement(root, "ECUC-ERROR_UNDEFINED-PARAM-VALUE")


   if subtype == "bool":
      def_ref = ET.SubElement(param_blk, "DEFINITION-REF", DEST="ECUC-BOOLEAN-PARAM-DEF")
   elif subtype == "int":
      def_ref = ET.SubElement(param_blk, "DEFINITION-REF", DEST="ECUC-INTEGER-PARAM-DEF")
   elif subtype == "func":
      def_ref = ET.SubElement(param_blk, "DEFINITION-REF", DEST="ECUC-FUNCTION-NAME-DEF")
   elif subtype == "enum":
      def_ref = ET.SubElement(param_blk, "DEFINITION-REF", DEST="ECUC-ENUMERATION-PARAM-DEF")
   else:
      def_ref = ET.SubElement(param_blk, "DEFINITION-REF", DEST="ECUC-ERROR_UNDEFINED-PARAM-DEF")
   def_ref.text = refname

   def_ref = ET.SubElement(param_blk, "VALUE")
   def_ref.text = value



#####################################
# Search Functions
#####################################
# arg2: root is ELEMENTS block inside AR-PACKAGE named Ecuc_<arpkg>
def find_module_conf_values(shortname, root):
   modconf = None
   
   if get_tag(root) == "ELEMENTS":
      for elem in list(root):
         if get_tag(elem) == "ECUC-MODULE-CONFIGURATION-VALUES":
            for item in list(elem):
               if get_tag(item) == "SHORT-NAME":
                  if item.text == shortname:
                     modconf = elem
                     break
                  
   return modconf


# arg2: root is CONTAINERS block inside ECUC-MODULE-CONFIGURATION-VALUES
def find_ecuc_container_value(shortname, root):
   ctnrval = None
   
   if get_tag(root) == "CONTAINERS":
      for elem in list(root):
         if get_tag(elem) == "ECUC-CONTAINER-VALUE":
            for item in list(elem):
               if get_tag(item) == "SHORT-NAME":
                  if item.text == shortname:
                     ctnrval = elem
                     break
                  
   return ctnrval
