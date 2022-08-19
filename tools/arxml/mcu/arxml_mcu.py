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
import arxml.core.lib_conf as lib_conf
import arxml.core.lib_defs as lib_defs



# This function updates NammaAUTOSAR Mcu parameters into its container
def update_uc_info_to_container(root, uc_info):
    ctnrname = "McuNammaAutosarInfo"
    ctnrval = lib_conf.find_ecuc_container_value(ctnrname, root)
    
    # Delete node to rewrite new values
    if None != ctnrval:
        root.remove(ctnrval)
    
    # Create a new container    
    dref = "/AUTOSAR/EcucDefs/Mcu/VendorSpecific"
    ctnrval = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)
        
        
    # Parameters
    params = ET.SubElement(ctnrval, "PARAMETER-VALUES")
    refname = "/AUTOSAR/EcucDefs/Mcu/VendorSpecific/Micro"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", uc_info.micro)
    refname = "/AUTOSAR/EcucDefs/Mcu/VendorSpecific/MicroArch"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", uc_info.micro_arch)
    refname = "/AUTOSAR/EcucDefs/Mcu/VendorSpecific/MicroMaker"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", uc_info.micro_maker)
    
    


# Update ARXML with Micro Controller Info only.
def update_arxml(ar_file, uc_info):
    # Following line is added to avoid ns0 prefix added
    ET.register_namespace('', "http://autosar.org/schema/r4.0")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    ar_isp = lib_conf.find_ecuc_elements_block(root)
    if ar_isp == None:
        return
        
    # Now find if Mcu module-conf is already there in insertion-point
    modname = "Mcu"
    modconf = lib_conf.find_module_conf_values(modname, ar_isp)
    if modconf == None:
        modconf = lib_conf.insert_ecuc_module_conf(ar_isp, modname)
   
    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    # Add Uc_Info contents to CONTAINER
    update_uc_info_to_container(containers, uc_info)

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: Micro Controller Configs are saved to " + ar_file)    



# This function is highly incomplete.....
def parse_arxml(ar_file, uc_info):
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    # locate Mcu module configuration under ELEMENTS
    modconf = lib_conf.find_module_conf_values("Mcu", elems)

    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    # locate VendorSpecific configs
    ctnrname = "McuNammaAutosarInfo"
    ctnrval = lib_conf.find_ecuc_container_value(ctnrname, containers)
    params = None
    if None != ctnrval:
        params = lib.get_param_list(ctnrval)

    if None != params:
        for param in params:
            if param["tag"] == "Micro":
                uc_info.micro = param["val"]
            if param["tag"] == "MicroArch":
                uc_info.micro_arch = param["val"]
            if param["tag"] == "MicroMaker":
                uc_info.micro_maker = param["val"]
