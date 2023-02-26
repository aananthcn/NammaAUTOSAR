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



def add_soad_fo_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdFrameOwnerConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/SoAdFrameType"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdFrameType"]))
    refname = dref+"/SoAdOwner"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdOwner"]))



def add_soad_rxi_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdRxIndicationConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/SoAdRxIndicationFunction"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(cfg["SoAdRxIndicationFunction"]))



def add_soad_txc_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdTxConfirmationConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/SoAdTxConfirmationFunction"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(cfg["SoAdTxConfirmationFunction"]))



def add_soad_tlsc_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdTrcvLinkStateChgConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/SoAdTrcvLinkStateChgFunction"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(cfg["SoAdTrcvLinkStateChgFunction"]))



def insert_soad_pctrl_sub_container(ctnr, dref, cfg):
    # Insert subContainer(s) - SoAdPhysCtrlRxMainFunctionPriorityProcessing
    subctnr2 = ET.SubElement(ctnr, "SUB-CONTAINERS")
    sctnr_name = "SoAdPhysCtrlRxMainFunctionPriorityProcessing"
    cf_ctnr = lib_conf.insert_conf_container(subctnr2, sctnr_name, "conf", dref)

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(cf_ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(cf_ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdPhysCtrlRxMainFunctionPeriod"
    lib_conf.insert_conf_param(params, refname, "numerical", "float", str(cfg["SoAdPhysCtrlRxMainFunctionPeriod"]))
    refname = dref+"/SoAdPhysCtrlRxIndicationIterations"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdPhysCtrlRxIndicationIterations"]))
    # Insert references
    if "SoAdPhysCtrlRxIngressFifoRef" in cfg:
        refname = dref+"/SoAdPhysCtrlRxIngressFifoRef"
        refdest = str(cfg["SoAdPhysCtrlRxIngressFifoRef"])
        lib_conf.insert_conf_reference(refs, refname, refdest)



def add_soad_pctrlr_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdPhysController is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdPhysControllerIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdPhysControllerIdx"]))
    # Insert references
    refname = dref+"/SoAdEthCtrlRef"
    refdest = str(cfg["SoAdEthCtrlRef"])
    lib_conf.insert_conf_reference(refs, refname, refdest)
    refname = dref+"/SoAdWEthCtrlRef"
    refdest = str(cfg["SoAdWEthCtrlRef"])
    lib_conf.insert_conf_reference(refs, refname, refdest)

    # Insert subContainer(s) - SoAdPhysCtrlRxMainFunctionPriorityProcessing
    dref2 = dref+"/SoAdPhysCtrlRxMainFunctionPriorityProcessing"
    insert_soad_pctrl_sub_container(ctnr, dref2, cfg)



def add_soad_ctrlr_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdController is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdCtrlIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdCtrlIdx"]))
    refname = dref+"/SoAdVlanId"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdVlanId"]))
    refname = dref+"/SoAdCtrlMtu"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdCtrlMtu"]))
    refname = dref+"/SoAdMaxTxBufsTotal"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdMaxTxBufsTotal"]))
    # Insert references
    if "SoAdPhysControllerRef" in cfg:
        refname = dref+"/SoAdPhysControllerRef"
        refdest = str(cfg["SoAdPhysControllerRef"])
        lib_conf.insert_conf_reference(refs, refname, refdest)
    if "SoAdEthTrcvRef" in cfg:
        refname = dref+"/SoAdEthTrcvRef"
        refdest = str(cfg["SoAdEthTrcvRef"])
        lib_conf.insert_conf_reference(refs, refname, refdest)
    if "SoAdSwitchRef" in cfg:
        refname = dref+"/SoAdSwitchRefOrPortGroupRef/SoAdSwitchRef"
        refdest = str(cfg["SoAdSwitchRef"])
        lib_conf.insert_conf_reference(refs, refname, refdest)
    if "SoAdSwitchPortGroupRef" in cfg:
        refname = dref+"/SoAdSwitchRefOrPortGroupRef/SoAdSwitchPortGroupRef"
        refdest = str(cfg["SoAdSwitchPortGroupRef"])
        lib_conf.insert_conf_reference(refs, refname, refdest)



def add_soad_trcv_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdTransceiver is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdTransceiverIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdTransceiverIdx"]))
    # Insert references
    if "SoAdEthTrcvRef" in cfg:
        refname = dref+"/SoAdEthTrcvRef"
        refdest = str(cfg["SoAdEthTrcvRef"])
        lib_conf.insert_conf_reference(refs, refname, refdest)
    if "SoAdWEthTrcvRef" in cfg:
        refname = dref+"/SoAdWEthTrcvRef"
        refdest = str(cfg["SoAdWEthTrcvRef"])
        lib_conf.insert_conf_reference(refs, refname, refdest)



def add_soad_swt_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdSwitch is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdSwitchIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdSwitchIdx"]))
    # Insert references
    if "SoAdSwitchRef" in cfg:
        refname = dref+"/SoAdSwitchRef"
        refdest = str(cfg["SoAdSwitchRef"])
        lib_conf.insert_conf_reference(refs, refname, refdest)



def add_soad_spg_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdSwitchPortGroup is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdSwitchPortGroupIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["SoAdSwitchPortGroupIdx"]))
    refname = dref+"/SoAdSwitchPortGroupRefSemantics"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(cfg["SoAdSwitchPortGroupRefSemantics"]))

    # Insert references
    if "SoAdPortRef" in cfg:
        refname = dref+"/SoAdPortRef"
        refdest = str(cfg["SoAdPortRef"])
        lib_conf.insert_conf_reference(refs, refname, refdest)



def update_soad_configset_to_container(ctnrname, root, soad_cfg):
    # Create a new container - SoAd Driver
    dref = "/AUTOSAR/EcucDefs/SoAd/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Create a sub-container
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "SoAdFrameOwnerConfig"
    eif_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_soad_fo_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "SoAdRxIndicationConfig"
    eif_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_soad_rxi_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "SoAdTxConfirmationConfig"
    eif_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_soad_txc_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "SoAdTrcvLinkStateChgConfig"
    eif_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_soad_tlsc_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "SoAdPhysController"
    eif_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_soad_pctrlr_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "SoAdController"
    eif_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_soad_ctrlr_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "SoAdTransceiver"
    eif_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_soad_trcv_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "SoAdSwitch"
    eif_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_soad_swt_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "SoAdSwitchPortGroup"
    eif_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_soad_spg_config_params_to_container(mdc_ctnr, eif_dref, cfg)




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
    # update_soad_configset_to_container("SoAdBswModules", containers, soad_configs["SoAdBswModules"])

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: SoAd Configs are saved to " + ar_file)    
