#
# Created on Sun Feb 26 2023 10:41:18 PM
#
# The MIT License (MIT)
# Copyright (c) 2023 Aananth C N
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



def update_soad_bswmodules_to_container(ctnrname, root, soad_cfg):
    for obj in soad_cfg:
        cfg = obj.datavar
        # Create a new container - SoAdBswModules
        dref = "/AUTOSAR/EcucDefs/SoAd/"+ctnrname
        ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

        # Insert PARAMETER & REFERENCE block
        params = ET.SubElement(ctnrblk, "PARAMETER-VALUES")
        refs = ET.SubElement(ctnrblk, "REFERENCE-VALUES")

        # Insert parameters
        refname = dref+"/SoAdIf"
        lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(cfg["SoAdIf"]))
        refname = dref+"/SoAdIfTriggerTransmit"
        lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(cfg["SoAdIfTriggerTransmit"]))
        refname = dref+"/SoAdIfTxConfirmation"
        lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(cfg["SoAdIfTxConfirmation"]))
        refname = dref+"/SoAdLocalIpAddrAssigmentChg"
        lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(cfg["SoAdLocalIpAddrAssigmentChg"]))
        refname = dref+"/SoAdSoConModeChg"
        lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(cfg["SoAdSoConModeChg"]))
        refname = dref+"/SoAdTp"
        lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(cfg["SoAdTp"]))
        refname = dref+"/SoAdUseCallerInfix"
        lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(cfg["SoAdUseCallerInfix"]))
        refname = dref+"/SoAdUseTypeInfix"
        lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(cfg["SoAdUseTypeInfix"]))

        if "SoAdBswModuleRef" in cfg:
            refname = dref+"/SoAdBswModuleRef"
            refdest = str(cfg["SoAdBswModuleRef"])
            lib_conf.insert_conf_reference(refs, refname, refdest)



def add_soad_general_parameters_to_container(ctnr, dref, gen_cfg):
    if not gen_cfg:
        print("Warning: ARXML write - SoAdGeneral is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    pref = dref+"/SoAdDevErrorDetect"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdDevErrorDetect"]))
    pref = dref+"/SoAdVersionInfoApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdVersionInfoApi"]))
    pref = dref+"/SoAdIPv6AddressEnabled"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdIPv6AddressEnabled"]))
    pref = dref+"/SoAdMainFunctionPeriod"
    lib_conf.insert_conf_param(params, pref, "numerical", "float", str(gen_cfg["SoAdMainFunctionPeriod"]))
    pref = dref+"/SoAdSoConMax"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(gen_cfg["SoAdSoConMax"]))
    pref = dref+"/SoAdRoutingGroupMax"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(gen_cfg["SoAdRoutingGroupMax"]))
    pref = dref+"/SoAdGetAndResetMeasurementDataApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdGetAndResetMeasurementDataApi"]))
    pref = dref+"/SoAdEnableSecurityEventReporting"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdEnableSecurityEventReporting"]))
    pref = dref+"/SoAdSecurityEventRefs"
    lib_conf.insert_conf_param(params, pref, "text", "string", str(gen_cfg["SoAdSecurityEventRefs"]))



def update_soad_general_to_container(ctnrname, root, soad_cfg):
    # Create a new container - SoAdGeneral
    dref = "/AUTOSAR/EcucDefs/SoAd/"+ctnrname
    mdc_ctnr = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)
    add_soad_general_parameters_to_container(mdc_ctnr, dref, soad_cfg.datavar)

    # Create a sub-container
    subctnr1 = ET.SubElement(mdc_ctnr, "SUB-CONTAINERS")



def print_soad_configs(soad_configs):
    print("\n\nWrite Operation:")
    print("\nSoAdGeneral:")
    for cfg in soad_configs["SoAdGeneral"]:
        print(cfg.datavar)

    print("\nSoAdBswModules:")
    for cfg in soad_configs["SoAdBswModules"]:
        print(cfg.datavar)

    print("\nSoAdConfig:")
    for cfg in soad_configs["SoAdConfig"]:
        print(cfg.datavar)



# # This function updates NammaAUTOSAR SoAd parameters into its container
def update_arxml(ar_file, soad_configs):
    # Following line is added to avoid ns0 prefix added
    ET.register_namespace('', "http://autosar.org/schema/r4.0")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    
    print_soad_configs(soad_configs)
    
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block, i.e., insert point
    ar_isp = lib_conf.find_ecuc_elements_block(root)

	# remove SoAd configs
    soad_modconfs = lib_conf.find_module_configs("SoAd", ar_isp)
    if soad_modconfs:
        ar_isp.remove(soad_modconfs)

    # insert SoAd configs
    modconf = lib_conf.insert_ecuc_module_conf(ar_isp, "SoAd")

    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    # Add SoAd contents to CONTAINER
    update_soad_general_to_container("SoAdGeneral", containers, soad_configs["SoAdGeneral"][0])
    update_soad_bswmodules_to_container("SoAdBswModules", containers, soad_configs["SoAdBswModules"])

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: SoAd Configs are saved to " + ar_file)    
