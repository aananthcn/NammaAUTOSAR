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
   elif subtype == "float":
      def_ref = ET.SubElement(param_blk, "DEFINITION-REF", DEST="ECUC-FLOAT-PARAM-DEF")
   elif subtype == "string":
      def_ref = ET.SubElement(param_blk, "DEFINITION-REF", DEST="ECUC-STRING-PARAM-DEF")
   else:
      def_ref = ET.SubElement(param_blk, "DEFINITION-REF", DEST="ECUC-ERROR_UNDEFINED-PARAM-DEF")
   def_ref.text = refname

   def_ref = ET.SubElement(param_blk, "VALUE")
   def_ref.text = value



#####################################
# Search Functions
#####################################
def find_ecuc_elements_block(root):
    ecuc_arpkg_name = get_ecuc_arpkg_name()
    ar_pkg = find_ar_package(ecuc_arpkg_name, root)
    if ar_pkg == None:
        print("Error: find_ecuc_elements_block() couldn't find "+ecuc_arpkg_name+"!")
        return

    # Now find insertion point. Our insert point is ELEMENTS block inside AR-PACKAGE named EcucDefs (in ver R20-11)
    ar_elems = None
    for item in list(ar_pkg):
        if get_tag(item) == "ELEMENTS":
            ar_elems = item # insertion point
            break 
    if ar_elems == None:
        print("Error: couldn't find ELEMENTS in AR-PACKAGE, hence can't update MicroC info to ARXML!")

    return ar_elems
    


# arg2: root is ELEMENTS block inside AR-PACKAGE named Ecuc_<arpkg>
def find_module_conf_values(shortname, root):
   modconf = None

   if shortname == None:
      print("Error: Invalid argument to find_module_conf_values()")
      return

   if get_tag(root) == "ELEMENTS":
      for elem in list(root):
         if get_tag(elem) == "ECUC-MODULE-CONFIGURATION-VALUES":
            for item in list(elem):
               if get_tag(item) == "SHORT-NAME":
                  if item.text == shortname:
                     modconf = elem
                     break

   return modconf


def find_containers_in_modconf(root):
    containers = None
    if root == None:
       print("Error: Invalid argument to find_containers_in_modconf()")
       return

    for item in list(root):
        if get_tag(item) == "CONTAINERS":
            containers = item
    if containers == None:
        print("Error: couldn't find CONTAINERS in Mcu Mod. Conf., hence can't update MicroC info to ARXML!")

    return containers



# arg2: root is CONTAINERS block inside ECUC-MODULE-CONFIGURATION-VALUES
def find_ecuc_container_block(shortname, root):
   ctnrval = None

   if shortname == None:
      print("Error: Invalid argument to find_ecuc_container_block()")
      return

   if get_tag(root) == "CONTAINERS":
      for elem in list(root):
         if get_tag(elem) == "ECUC-CONTAINER-VALUE":
            for item in list(elem):
               if get_tag(item) == "SHORT-NAME":
                  if item.text == shortname:
                     ctnrval = elem
                     break

   return ctnrval


def findall_subcontainers_with_name(shortname, root):
   ctnrnode = []

   if shortname == None:
      print("Error: Invalid argument to find_subcontainer_with_name()")
      return

   for child in list(root):
      if get_tag(child) == "SUB-CONTAINERS":
         for ecu_ctnr in list(child):
            if get_tag(ecu_ctnr) == "ECUC-CONTAINER-VALUE":
               for item in list(ecu_ctnr):
                  if get_tag(item) == "SHORT-NAME":
                     if item.text == shortname:
                        ctnrnode.append(ecu_ctnr)

   # if there is no ECUC-CONTAINER with name == "shortname", return None
   if len(ctnrnode) == 0:
      ctnrnode = None

   return ctnrnode


def findall_containers_with_name(shortname, root):
   ctnrnode = []

   if shortname == None:
      print("Error: Invalid argument to findall_containers_with_name()")
      return

   for child in list(root):
      if get_tag(child) == "ECUC-CONTAINER-VALUE":
         for item in list(child):
            if get_tag(item) == "SHORT-NAME":
               if item.text == shortname:
                  ctnrnode.append(child)
                  break # done, move to the next container
               else:
                  break # wrong container, so don't spend time here

   # if there is no ECUC-CONTAINER with name == "shortname", return None
   if len(ctnrnode) == 0:
      ctnrnode = None

   return ctnrnode