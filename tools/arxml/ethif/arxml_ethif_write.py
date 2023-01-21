#
# Created on Thu Jan 19 2023 10:50:02 PM
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



def add_ethif_fo_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - EthIfFrameOwnerConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthIfFrameType"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["EthIfFrameType"]))
    refname = dref+"/EthIfOwner"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["EthIfOwner"]))



def add_ethif_rxi_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - EthIfRxIndicationConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthIfRxIndicationFunction"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(cfg["EthIfRxIndicationFunction"]))



def add_ethif_txc_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - EthIfTxConfirmationConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthIfTxConfirmationFunction"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(cfg["EthIfTxConfirmationFunction"]))



def add_ethif_tlsc_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - EthIfTrcvLinkStateChgConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthIfTrcvLinkStateChgFunction"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(cfg["EthIfTrcvLinkStateChgFunction"]))



def insert_ethif_pctrl_sub_container(ctnr, dref, cfg):
    # Insert subContainer(s) - EthIfPhysCtrlRxMainFunctionPriorityProcessing
    subctnr2 = ET.SubElement(ctnr, "SUB-CONTAINERS")
    sctnr_name = "EthIfPhysCtrlRxMainFunctionPriorityProcessing"
    cf_ctnr = lib_conf.insert_conf_container(subctnr2, sctnr_name, "conf", dref)

    # Insert PARAMETER block
    params = ET.SubElement(cf_ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthIfPhysCtrlRxMainFunctionPeriod"
    lib_conf.insert_conf_param(params, refname, "numerical", "float", str(cfg["EthIfPhysCtrlRxMainFunctionPeriod"]))
    refname = dref+"/EthIfPhysCtrlRxIndicationIterations"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["EthIfPhysCtrlRxIndicationIterations"]))
    # Insert references
    refname = dref+"/EthIfPhysCtrlRxIngressFifoRef"
    refdest = str(cfg["EthIfPhysCtrlRxIngressFifoRef"])
    lib_conf.insert_conf_reference(params, refdest, refname)



def add_ethif_pctrlr_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - EthIfPhysController is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthIfPhysControllerIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["EthIfPhysControllerIdx"]))
    # Insert references
    refname = dref+"/EthIfEthCtrlRef"
    refdest = str(cfg["EthIfEthCtrlRef"])
    lib_conf.insert_conf_reference(params, refdest, refname)
    refname = dref+"/EthIfWEthCtrlRef"
    refdest = str(cfg["EthIfWEthCtrlRef"])
    lib_conf.insert_conf_reference(params, refdest, refname)

    # # Insert subContainer(s) - EthIfPhysCtrlRxMainFunctionPriorityProcessing
    dref2 = dref+"/EthIfPhysCtrlRxMainFunctionPriorityProcessing"
    insert_ethif_pctrl_sub_container(ctnr, dref2, cfg)



def add_ethif_ctrlr_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - EthIfController is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthIfCtrlIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["EthIfCtrlIdx"]))
    refname = dref+"/EthIfVlanId"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["EthIfVlanId"]))
    refname = dref+"/EthIfCtrlMtu"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["EthIfCtrlMtu"]))
    refname = dref+"/EthIfMaxTxBufsTotal"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["EthIfMaxTxBufsTotal"]))
    # Insert references
    refname = dref+"/EthIfPhysControllerRef"
    refdest = str(cfg["EthIfPhysControllerRef"])
    lib_conf.insert_conf_reference(params, refdest, refname)
    refname = dref+"/EthIfEthTrcvRef"
    refdest = str(cfg["EthIfEthTrcvRef"])
    lib_conf.insert_conf_reference(params, refdest, refname)
    refname = dref+"/EthIfSwitchRefOrPortGroupRef/EthIfSwitchRef"
    refdest = str(cfg["EthIfSwitchRef"])
    lib_conf.insert_conf_reference(params, refdest, refname)
    refname = dref+"/EthIfSwitchRefOrPortGroupRef/EthIfSwitchPortGroupRef"
    refdest = str(cfg["EthIfSwitchPortGroupRef"])
    lib_conf.insert_conf_reference(params, refdest, refname)



def add_ethif_trcv_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - EthIfTransceiver is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthIfTransceiverIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(cfg["EthIfTransceiverIdx"]))
    # Insert references
    refname = dref+"/EthIfEthTrcvRef"
    refdest = str(cfg["EthIfEthTrcvRef"])
    lib_conf.insert_conf_reference(params, refdest, refname)
    refname = dref+"/EthIfWEthTrcvRef"
    refdest = str(cfg["EthIfWEthTrcvRef"])
    lib_conf.insert_conf_reference(params, refdest, refname)



def update_ethif_configset_to_container(ctnrname, root, ethif_cfg):
    # Create a new container - EthIf Driver
    dref = "/AUTOSAR/EcucDefs/EthIf/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Create a sub-container
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "EthIfFrameOwnerConfig"
    eif_dref = dref+"/"+sctnr_name
    for cfg in ethif_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_ethif_fo_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "EthIfRxIndicationConfig"
    eif_dref = dref+"/"+sctnr_name
    for cfg in ethif_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_ethif_rxi_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "EthIfTxConfirmationConfig"
    eif_dref = dref+"/"+sctnr_name
    for cfg in ethif_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_ethif_txc_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "EthIfTrcvLinkStateChgConfig"
    eif_dref = dref+"/"+sctnr_name
    for cfg in ethif_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_ethif_tlsc_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "EthIfPhysController"
    eif_dref = dref+"/"+sctnr_name
    for cfg in ethif_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_ethif_pctrlr_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "EthIfController"
    eif_dref = dref+"/"+sctnr_name
    for cfg in ethif_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_ethif_ctrlr_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "EthIfTransceiver"
    eif_dref = dref+"/"+sctnr_name
    for cfg in ethif_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        add_ethif_trcv_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "EthIfSwitch"
    eif_dref = dref+"/"+sctnr_name
    for cfg in ethif_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        # add_ethif_fo_config_params_to_container(mdc_ctnr, eif_dref, cfg)

    sctnr_name = "EthIfSwitchPortGroup"
    eif_dref = dref+"/"+sctnr_name
    for cfg in ethif_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", eif_dref)
        # add_ethif_fo_config_params_to_container(mdc_ctnr, eif_dref, cfg)




def add_ethif_general_parameters_to_container(ctnr, dref, gen_cfg):
    if not gen_cfg:
        print("Warning: ARXML write - EthIfGeneral is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    pref = dref+"/EthIfMaxTrcvsTotal"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(gen_cfg["EthIfMaxTrcvsTotal"]))
    pref = dref+"/EthIfDevErrorDetect"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfDevErrorDetect"]))
    pref = dref+"/EthIfEnableRxInterrupt"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfEnableRxInterrupt"]))
    pref = dref+"/EthIfEnableTxInterrupt"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfEnableTxInterrupt"]))
    pref = dref+"/EthIfVersionInfoApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfVersionInfoApi"]))
    pref = dref+"/EthIfVersionInfoApiMacro"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfVersionInfoApiMacro"]))
    pref = dref+"/EthIfTrcvLinkStateChgMainReload"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(gen_cfg["EthIfTrcvLinkStateChgMainReload"]))
    pref = dref+"/EthIfMainFunctionPeriod"
    lib_conf.insert_conf_param(params, pref, "numerical", "float", str(gen_cfg["EthIfMainFunctionPeriod"]))
    pref = dref+"/EthIfPublicCddHeaderFile"
    for obj in gen_cfg["EthIfPublicCddHeaderFile"]:
        lib_conf.insert_conf_param(params, pref, "text", "string", obj["Headerfile"])
    pref = dref+"/EthIfRxIndicationIterations"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(gen_cfg["EthIfRxIndicationIterations"]))
    pref = dref+"/EthIfGetAndResetMeasurementDataApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfGetAndResetMeasurementDataApi"]))
    pref = dref+"/EthIfStartAutoNegotiation"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfStartAutoNegotiation"]))
    pref = dref+"/EthIfGetBaudRate"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfGetBaudRate"]))
    pref = dref+"/EthIfGetCounterState"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfGetCounterState"]))
    pref = dref+"/EthIfGlobalTimeSupport"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfGlobalTimeSupport"]))
    pref = dref+"/EthIfWakeUpSupport"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfWakeUpSupport"]))
    pref = dref+"/EthIfGetTransceiverWakeupModeApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthIfGetTransceiverWakeupModeApi"]))



def update_ethif_general_to_container(ctnrname, root, ethif_cfg):
    # Create a new container - EthIfGeneral
    dref = "/AUTOSAR/EcucDefs/EthIf/"+ctnrname
    mdc_ctnr = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)
    add_ethif_general_parameters_to_container(mdc_ctnr, dref, ethif_cfg.datavar)

    # Create a sub-container
    subctnr1 = ET.SubElement(mdc_ctnr, "SUB-CONTAINERS")



def print_ethif_configs(ethif_configs):
    print("\nEthIfGeneral:")
    for cfg in ethif_configs["EthIfGeneral"]:
        print(cfg.datavar)

    print("\nEthIfConfigSet:")
    for cfg in ethif_configs["EthIfConfigSet"]:
        print(cfg.datavar)



# # This function updates NammaAUTOSAR EthIf parameters into its container
def update_arxml(ar_file, ethif_configs):
    # Following line is added to avoid ns0 prefix added
    ET.register_namespace('', "http://autosar.org/schema/r4.0")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    
    print("arxml_ethif_write.py: update_arxml called!")
    print_ethif_configs(ethif_configs)
    
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block, i.e., insert point
    ar_isp = lib_conf.find_ecuc_elements_block(root)

	# remove EthIf configs
    ethif_modconfs = lib_conf.find_module_configs("EthIf", ar_isp)
    if ethif_modconfs:
        ar_isp.remove(ethif_modconfs)

    # insert EthIf configs
    modconf = lib_conf.insert_ecuc_module_conf(ar_isp, "EthIf")

    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    # Add EthIf contents to CONTAINER
    update_ethif_configset_to_container("EthIfConfigSet", containers, ethif_configs["EthIfConfigSet"])
    update_ethif_general_to_container("EthIfGeneral", containers, ethif_configs["EthIfGeneral"][0])

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: EthIf Configs are saved to " + ar_file)    
