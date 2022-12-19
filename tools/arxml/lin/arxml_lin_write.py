#
# Created on Mon Dec 19 2022 12:07:12 PM
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



def add_lin_chan_config_parameters_to_container(ctnr, dref, lin_chn_cfg):
    if not lin_chn_cfg:
        print("Warning: ARXML write - LinCtrlConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/LinChannelId"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(lin_chn_cfg["LinChannelId"]))
    refname = dref+"/LinNodeType"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(lin_chn_cfg["LinNodeType"]))
    refname = dref+"/LinChannelBaudRate"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(lin_chn_cfg["LinChannelBaudRate"]))
    refname = dref+"/LinChannelWakeupSupport"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(lin_chn_cfg["LinChannelWakeupSupport"]))
    refname = dref+"/LinChannelEcuMWakeupSource"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(lin_chn_cfg["LinChannelEcuMWakeupSource"]))
    refname = dref+"/LinClockRef"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(lin_chn_cfg["LinClockRef"]))



def update_lin_globalconfig_to_container(ctnrname, root, lin_cfg):
    # Create a new container - Lin Driver
    dref = "/AUTOSAR/EcucDefs/Lin/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Create a sub-container
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "LinChannel"
    ecc_dref = dref+"/"+sctnr_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", ecc_dref)
    add_lin_chan_config_parameters_to_container(mdc_ctnr, ecc_dref, lin_cfg.datavar["LinGlobalConfig"])



def add_lin_general_parameters_to_container(ctnr, dref, gen_cfg):
    if not gen_cfg:
        print("Warning: ARXML write - LinGeneral is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    pref = dref+"/LinIndex"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(gen_cfg["LinIndex"]))
    pref = dref+"/LinDevErrorDetect"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["LinDevErrorDetect"]))
    pref = dref+"/LinVersionInfoApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["LinVersionInfoApi"]))
    pref = dref+"/LinTimeoutDuration"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(gen_cfg["LinTimeoutDuration"]))



def update_lin_general_to_container(ctnrname, root, lin_cfg):
    # Create a new container - LinGeneral
    dref = "/AUTOSAR/EcucDefs/Lin/"+ctnrname
    mdc_ctnr = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)
    add_lin_general_parameters_to_container(mdc_ctnr, dref, lin_cfg.datavar["LinGeneral"])



def print_lin_configs(lin_configs):
    for cfg in lin_configs:
        print(cfg.datavar)



# # This function updates NammaAUTOSAR Lin parameters into its container
def update_arxml(ar_file, lin_configs):
    # Following line is added to avoid ns0 prefix added
    ET.register_namespace('', "http://autosar.org/schema/r4.0")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    
    print("arxml_lin_write.py: update_arxml called!")
    # print_lin_configs(lin_configs)
    
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    ar_isp = lib_conf.find_ecuc_elements_block(root)
    if ar_isp == None:
        return

    # remove all Lin configs
    lin_modconfs = lib_conf.findall_module_configs("Lin", ar_isp)
    for conf in lin_modconfs:
        ar_isp.remove(conf)

    # insert Lin configs
    for cfg in lin_configs:
        modconf = lib_conf.insert_ecuc_module_conf(ar_isp, "Lin")

        # locate container
        containers = lib_conf.find_containers_in_modconf(modconf)
        if containers == None:
            return

        # Add Lin contents to CONTAINER
        update_lin_general_to_container("LinGeneral", containers, cfg)
        update_lin_globalconfig_to_container("LinGlobalConfig", containers, cfg)

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: Lin Configs are saved to " + ar_file)    
