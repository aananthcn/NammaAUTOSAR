#
# Created on Thu Sep 01 2022 7:40:43 PM
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



def update_port_gen_to_container(root, tab_gen):
    ctnrname = "PortGeneral"
    pcs_ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, root)
    
    # Delete node to rewrite new values
    if None != pcs_ctnrblk:
        root.remove(pcs_ctnrblk)
    
    # Create a new container - PortGeneral
    dref = "/AUTOSAR/EcucDefs/Port/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Create a sub-container    
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")
    subctnr1_name = "PortContainer"
    dref = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name
    cctnrblk1 = lib_conf.insert_conf_container(subctnr1, subctnr1_name, "conf", dref)

    # Parameters
    params = ET.SubElement(cctnrblk1, "PARAMETER-VALUES")

    refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortDevErrorDetect"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", tab_gen.gen_data["PortDevErrorDetect"])

    refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortVersionInfoApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", tab_gen.gen_data["PortVersionInfoApi"])

    refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortSetPinDirectionApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", tab_gen.gen_data["PortSetPinDirectionApi"])

    refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortSetPinModeApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", tab_gen.gen_data["PortSetPinModeApi"])




# This function updates NammaAUTOSAR Port parameters into its container
def update_port_info_to_container(root, tab_cfg):
    ctnrname = "PortConfigSet"
    pcs_ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, root)
    
    # Delete node to rewrite new values
    if None != pcs_ctnrblk:
        root.remove(pcs_ctnrblk)
    
    # Create a new container - PortConfigSet
    dref = "/AUTOSAR/EcucDefs/Port/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Create a sub-container    
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")
    subctnr1_name = "PortContainer"
    dref = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name
    cctnrblk1 = lib_conf.insert_conf_container(subctnr1, subctnr1_name, "conf", dref)

    # Parameters
    params = ET.SubElement(cctnrblk1, "PARAMETER-VALUES")
    refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortNumberOfPortPins"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(len(tab_cfg.pins_str)))
    
    # Create a sub-container    
    subctnr2 = ET.SubElement(cctnrblk1, "SUB-CONTAINERS")
    subctnr2_name = "PortPin"
    dref = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/"+subctnr2_name
    
    # Insert pin info as conf_container values
    for i in range(len(tab_cfg.pins_str)):
        cctnrblk2 = lib_conf.insert_conf_container(subctnr2, subctnr2_name, "conf", dref)
        params = ET.SubElement(cctnrblk2, "PARAMETER-VALUES")

        # Parameter - PortPinId
        refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortPin/PortPinId"
        lib_conf.insert_conf_param(params, refname, "numerical", "int", tab_cfg.pins_str[i].id.get())

        # Parameter - PortPinDirection
        refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortPin/PortPinDirection"
        lib_conf.insert_conf_param(params, refname, "numerical", "int", tab_cfg.pins_str[i].pindir.get())

        # Parameter - PortPinDirectionChangeable
        refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortPin/PortPinDirectionChangeable"
        lib_conf.insert_conf_param(params, refname, "numerical", "int", tab_cfg.pins_str[i].dir_changeable.get())

        # Parameter - PortPinLevelValue
        refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortPin/PortPinLevelValue"
        lib_conf.insert_conf_param(params, refname, "numerical", "int", tab_cfg.pins_str[i].pin_level.get())

        # Parameter - PortPinMode
        refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortPin/PortPinMode"
        lib_conf.insert_conf_param(params, refname, "numerical", "int", tab_cfg.pins_str[i].pin_mode.get())

        # Parameter - PortPinModeChangeable
        refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortPin/PortPinModeChangeable"
        lib_conf.insert_conf_param(params, refname, "numerical", "int", tab_cfg.pins_str[i].mode_changeable.get())

        # Parameter - PortPinInitialMode 
        refname = "/AUTOSAR/EcucDefs/Port/"+ctnrname+"/"+subctnr1_name+"/PortPin/PortPinInitialMode"
        lib_conf.insert_conf_param(params, refname, "numerical", "int", tab_cfg.pins_str[i].pin_initial_mode.get())
    
    
    


# Write ARXML with port info
def update_arxml(ar_file, port_info, port_gen):
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
    modname = "Port"
    modconf = lib_conf.find_module_conf_values(modname, ar_isp)
    if modconf == None:
        modconf = lib_conf.insert_ecuc_module_conf(ar_isp, modname)
   
    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    # Add PortConfigSet contents to CONTAINER
    update_port_info_to_container(containers, port_info)
    
    # Add PortGeneral contents to CONTAINER
    update_port_gen_to_container(containers, port_gen)

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: Port Controller Configs are saved to " + ar_file)    



# This function parses ARXML and extract the Port information
# Returns: No of port, Port dictionary
def parse_arxml(ar_file):
    if ar_file == None:
        return None, None
    port_pin_count = None
    port_pins = []
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    # locate Mcu module configuration under ELEMENTS
    modconf = lib_conf.find_module_conf_values("Port", elems)

    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    # locate PortConfigSet
    ctnrname = "PortConfigSet"
    ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, containers)
    if lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
        return None
    
    # now locate PortContainer
    port_ctnr = None
    for ecuc_ctnr in ctnrblk:
        if lib_conf.get_tag(ecuc_ctnr) == "SUB-CONTAINERS":
            ctnrblk = ecuc_ctnr
            break
    for ecuc_ctnr in ctnrblk:
        if lib_conf.get_tag(ecuc_ctnr) == "ECUC-CONTAINER-VALUE":
            ctnrblk = ecuc_ctnr
            break
    for item in ctnrblk:
        if lib_conf.get_tag(item) == "SHORT-NAME":
            if item.text == "PortContainer":
                port_ctnr = ctnrblk
                break

    # get PortContainer parameter - Number of Port Pins
    if port_ctnr == None:
        return None
    params = lib_conf.get_param_list(port_ctnr)
    if params[0]["tag"] == "PortNumberOfPortPins":
        port_pin_count = int(params[0]["val"])
        
    # Now locate SUB-CONTAINERS to parse pin configurations
    for subctnr in ctnrblk:
        if lib_conf.get_tag(subctnr) == "SUB-CONTAINERS":
            for ctnr in subctnr:
                port_info = {}
                params = lib_conf.get_param_list(ctnr)
                for par in params:
                    port_info[par["tag"]] = par["val"]
                port_pins.append(port_info)
    
    return port_pin_count, port_pins, None