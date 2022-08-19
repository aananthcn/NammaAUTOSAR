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


def insert_conf_module(element_node, module_name):
   mod_conf = ET.SubElement(element_node, "ECUC-MODULE-CONFIGURATION-VALUES")
   shortname = ET.SubElement(mod_conf, "SHORT-NAME")
   shortname.text = module_name
   def_ref = ET.SubElement(mod_conf, "DEFINITION-REF", DEST="ECUC-MODULE-DEF")
   def_ref.text = "/AUTOSAR/EcucDefs/"+module_name
   ecu_def_edition = ET.SubElement(mod_conf, "ECUC-DEF-EDITION")
   ecu_def_edition.text = "4.2.0"
   impl_cfg_var = ET.SubElement(mod_conf, "IMPLEMENTATION-CONFIG-VARIANT")
   impl_cfg_var.text = "VARIANT-PRE-COMPILE"

   # Create CONTAINER element and export Os object alone.
   containers = ET.SubElement(mod_conf, "CONTAINERS")

   return containers



def insert_conf_container(root, name, type, dref):
   ctnr = ET.SubElement(root, "ECUC-CONTAINER-VALUE")
   shortname = ET.SubElement(ctnr, "SHORT-NAME")
   shortname.text = name
   if type == "conf":
      def_ref = ET.SubElement(ctnr, "DEFINITION-REF", DEST="ECUC-PARAM-CONF-CONTAINER-DEF")
   elif type == "choice":
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



def insert_conf_param(root, refname, type, subtype, value):
   if type == "text":
      param_blk = ET.SubElement(root, "ECUC-TEXTUAL-PARAM-VALUE")
   elif type == "numerical":
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

