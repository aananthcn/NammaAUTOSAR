#
# Created on Tue Sep 13 2022 10:00:03 PM
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




def update_dio_config_container(root, dio_cfg, dio_grp):
    ctnrname = "DioConfig"
    dcfg_ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, root)
    
    # Delete node to rewrite new values
    if None != dcfg_ctnrblk:
        root.remove(dcfg_ctnrblk)
    
    # Create a new container - DioConfig
    dref = "/AUTOSAR/EcucDefs/Dio/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)
    
    # Create a sub-container    
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")

    # Now dump all pin informations as container within sub-container
    for pin in dio_cfg:
        subctnr1_name = "DioPort"
        dref = "/AUTOSAR/EcucDefs/Dio/"+ctnrname+"/"+subctnr1_name
        cctnrblk1 = lib_conf.insert_conf_container(subctnr1, subctnr1_name, "conf", dref)

        # Parameters
        params = ET.SubElement(cctnrblk1, "PARAMETER-VALUES")
        refname = "/AUTOSAR/EcucDefs/Dio/"+ctnrname+"/"+subctnr1_name+"/DioPortId"
        lib_conf.insert_conf_param(params, refname, "numerical", "int", pin["DioPortId"])

        # DioChannel -- Create a sub-container    
        subctnr2 = ET.SubElement(cctnrblk1, "SUB-CONTAINERS")
        subctnr2_name = "DioChannel"
        dref = "/AUTOSAR/EcucDefs/Dio/"+ctnrname+"/"+subctnr1_name+"/"+subctnr2_name
        cctnrblk2 = lib_conf.insert_conf_container(subctnr2, subctnr2_name, "conf", dref)
        # Parameter
        params = ET.SubElement(cctnrblk2, "PARAMETER-VALUES")
        refname = dref+"/DioChannelId"
        lib_conf.insert_conf_param(params, refname, "numerical", "int", pin["DioChannelId"])

        # Check if Channel Group information corresponding to this DioPortId exists
        this_chgrp = []
        if len(dio_grp) > 0:
            for chgrp in dio_grp:
                if chgrp["DioPortId"] == pin["DioPortId"]:
                    this_chgrp.append(chgrp)

        # Add Channel Group information corresponding to this DioPortId
        if len(this_chgrp) > 0:
            # Create a sub-container    
            subctnr2 = ET.SubElement(cctnrblk1, "SUB-CONTAINERS")
            subctnr2_name = "DioChannelGroup"
            dref = "/AUTOSAR/EcucDefs/Dio/"+ctnrname+"/"+subctnr1_name+"/"+subctnr2_name

        for grp in this_chgrp:
            cctnrblk2 = lib_conf.insert_conf_container(subctnr2, subctnr2_name, "conf", dref)

            # Parameters - 1
            params = ET.SubElement(cctnrblk2, "PARAMETER-VALUES")
            refname = dref+"/DioChannelGroupIdentification"
            lib_conf.insert_conf_param(params, refname, "text", "enum", grp["DioChannelGroupIdentification"])
            # Parameters - 2
            params = ET.SubElement(cctnrblk2, "PARAMETER-VALUES")
            refname = dref+"/DioPortOffset"
            lib_conf.insert_conf_param(params, refname, "numerical", "int", grp["DioPortOffset"])
            # Parameters - 3
            params = ET.SubElement(cctnrblk2, "PARAMETER-VALUES")
            refname = dref+"/DioPortMask"
            lib_conf.insert_conf_param(params, refname, "numerical", "int", grp["DioPortMask"])



# This function updates NammaAUTOSAR Dio parameters into its container
def update_dio_info_to_container(root, dio_cfg, dio_grp, dio_gen):
    # DioConfig
    update_dio_config_container(root, dio_cfg, dio_grp)
    
    # DioGeneral
    ctnrname = "DioGeneral"
    dgen_ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, root)
    
    # Delete node to rewrite new values
    if None != dgen_ctnrblk:
        root.remove(dgen_ctnrblk)
    
    # Create a new container - DioGeneral
    dref = "/AUTOSAR/EcucDefs/Dio/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Parameters
    params = ET.SubElement(ctnrblk, "PARAMETER-VALUES")
    
    refname = dref+"/DioDevErrorDetect"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", dio_gen["DioDevErrorDetect"])
    refname = dref+"/DioVersionInfoApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", dio_gen["DioVersionInfoApi"])
    refname = dref+"/DioFlipChannelApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", dio_gen["DioFlipChannelApi"])
    refname = dref+"/DioMaskedWritePortApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", dio_gen["DioMaskedWritePortApi"])



# Write ARXML with dio info
def update_arxml(ar_file, dio_cfg, dio_grp, dio_gen):
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
    modname = "Dio"
    modconf = lib_conf.find_module_conf_values(modname, ar_isp)
    if modconf == None:
        modconf = lib_conf.insert_ecuc_module_conf(ar_isp, modname)
   
    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    # Add Dio Tab contents to CONTAINER
    update_dio_info_to_container(containers, dio_cfg, dio_grp, dio_gen)

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: Dio Configs are saved to " + ar_file)    



def parse_arxml_dioconfig(containers):
    dio_n_pins = None
    dio_configs = []
    dio_groups = []
    
    # locate DioConfig
    ctnrname = "DioConfig"
    ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, containers)
    if lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
        return None
    
    # now locate DioPort
    dio_cfg_ctnr = ctnrblk
    dio_sub_ctnr = None
    dioport_ctnr = None
    for ecuc_ctnr in ctnrblk:
        if lib_conf.get_tag(ecuc_ctnr) == "SUB-CONTAINERS":
            dio_sub_ctnr = ecuc_ctnr
            for ecuc_ctnr in dio_sub_ctnr:
                if lib_conf.get_tag(ecuc_ctnr) == "ECUC-CONTAINER-VALUE":
                    ctnrblk = ecuc_ctnr
                    for item in ctnrblk:
                        if lib_conf.get_tag(item) == "SHORT-NAME":
                            if item.text == "DioPort":
                                dio_n_pins = len(dio_sub_ctnr) # we have found the right SUB-CONTAINER!!
                                dioport_ctnr = ctnrblk
                                # Note: breaking based on assumption that there will be only one port ;-)
                                break
                                # this will be extended as dioport_ctnr[] list later, as I don't know if the
                                # current ARXML format that I understand is correct.

    # get the 'DioPortId' of this DioPort
    dio_port_id_cfg = {}
    params = lib_conf.get_param_list(dioport_ctnr)
    for par in params:
        dio_port_id_cfg[par["tag"]] = par["val"]
    
    # parse dio config from subcontainer
    nodes = lib_conf.findall_subcontainers_with_name("DioChannel", dioport_ctnr)
    if nodes != None:
        for node in nodes:
            params = lib_conf.get_param_list(node)
            cfg = {}
            for par in params:
                cfg[par["tag"]] = par["val"]
            cfg["DioPortId"] = dio_port_id_cfg["DioPortId"]
            dio_configs.append(cfg)
    
    # parse dio group from subcontainer
    nodes = lib_conf.findall_subcontainers_with_name("DioChannelGroup", dioport_ctnr)
    if nodes != None:
        for node in nodes:
            params = lib_conf.get_param_list(node)
            cfg = {}
            for par in params:
                cfg[par["tag"]] = par["val"]
            cfg["DioPortId"] = dio_port_id_cfg["DioPortId"]
            dio_groups.append(cfg)
    

    return dio_n_pins, dio_configs, dio_groups



# This function parses ARXML and extract the Dio information
# Returns: No of dio_configs, Dio pin dictionary
def parse_arxml(ar_file):
    if ar_file == None:
        return None, None, None
    dio_n_pins = None
    dio_configs = []
    dio_general = {}
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    # locate Mcu module configuration under ELEMENTS
    modconf = lib_conf.find_module_conf_values("Dio", elems)

    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return
    
    dio_n_pins, dio_configs, dio_groups = parse_arxml_dioconfig(containers)

    # locate & parse DioGeneral
    ctnrname = "DioGeneral"
    ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, containers)
    if lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
        return None
    params = lib_conf.get_param_list(ctnrblk)
    for par in params:
        dio_general[par["tag"]] = par["val"]
    
    return dio_n_pins, dio_configs, dio_groups, dio_general

