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



def add_eth_ctrl_sch_parameters_to_container(ctnr, dref, sch_cfg):
    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthCtrlConfigSchedulerPredecessorOrder"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(sch_cfg["EthCtrlConfigSchedulerPredecessorOrder"]))


def add_eth_ctrl_egress_parameters_to_container(ctnr, dref, egr_cfg, sch_cfg):
    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthCtrlConfigEgressFifoBufLenByte"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(egr_cfg["EthCtrlConfigEgressFifoBufLenByte"]))
    refname = dref+"/EthCtrlConfigEgressFifoBufTotal"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(egr_cfg["EthCtrlConfigEgressFifoBufTotal"]))
    refname = dref+"/EthCtrlConfigEgressFifoIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(egr_cfg["EthCtrlConfigEgressFifoIdx"]))
    refname = dref+"/EthCtrlConfigEgressFifoPriorityAssignment"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(egr_cfg["EthCtrlConfigEgressFifoPriorityAssignment"]))

    # Create a sub-container for EthCtrlConfigScheduler
    subctnr3 = ET.SubElement(ctnr, "SUB-CONTAINERS")

    # Fill parameters EthCtrlConfigScheduler to the sub-container
    sbc_name = "EthCtrlConfigScheduler"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr3, sbc_name, "conf", sbc_dref)

    # Create a sub-container for EthCtrlConfigScheduler
    subctnr4 = ET.SubElement(mdc_ctnr, "SUB-CONTAINERS")

    # Fill parameters EthCtrlConfigScheduler to the sub-container
    sbc_name = "EthCtrlConfigSchedulerPredecessor"
    sbc_dref = sbc_dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr4, sbc_name, "conf", sbc_dref)
    add_eth_ctrl_sch_parameters_to_container(mdc_ctnr, sbc_dref, sch_cfg)



def add_eth_ctrl_ingress_parameters_to_container(ctnr, dref, egr_cfg):
    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthCtrlConfigIngressFifoBufLenByte"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(egr_cfg["EthCtrlConfigIngressFifoBufLenByte"]))
    refname = dref+"/EthCtrlConfigIngressFifoBufTotal"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(egr_cfg["EthCtrlConfigIngressFifoBufTotal"]))
    refname = dref+"/EthCtrlConfigIngressFifoIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(egr_cfg["EthCtrlConfigIngressFifoIdx"]))
    refname = dref+"/EthCtrlConfigIngressFifoPriorityAssignment"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(egr_cfg["EthCtrlConfigIngressFifoPriorityAssignment"]))



def add_eth_ctrl_config_parameters_to_container(ctnr, dref, ecc_cfg, xgrs_cfg, sch_cfg):
    if not ecc_cfg:
        print("Warning: EthCtrlConfig is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthCtrlConfigSwBufferHandling"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(ecc_cfg["EthCtrlConfigSwBufferHandling"]))
    refname = dref+"/EthCtrlEnableMii"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(ecc_cfg["EthCtrlEnableMii"]))
    refname = dref+"/EthCtrlEnableRxInterrupt"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(ecc_cfg["EthCtrlEnableRxInterrupt"]))
    refname = dref+"/EthCtrlEnableSpiInterface"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(ecc_cfg["EthCtrlEnableSpiInterface"]))
    refname = dref+"/EthCtrlEnableTxInterrupt"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(ecc_cfg["EthCtrlEnableTxInterrupt"]))
    refname = dref+"/EthCtrlIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(ecc_cfg["EthCtrlIdx"]))
    refname = dref+"/EthCtrlMacLayerSpeed"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(ecc_cfg["EthCtrlMacLayerSpeed"]))
    refname = dref+"/EthCtrlMacLayerType"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(ecc_cfg["EthCtrlMacLayerType"]))
    refname = dref+"/EthCtrlMacLayerSubType"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(ecc_cfg["EthCtrlMacLayerSubType"]))
    refname = dref+"/EthCtrlPhyAddress"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(ecc_cfg["EthCtrlPhyAddress"]))

    # Create a sub-container for EthCtrlConfig
    subctnr2 = ET.SubElement(ctnr, "SUB-CONTAINERS")

    # Fill parameters EthCtrlConfigEgress to the sub-container
    sbc_name = "EthCtrlConfigEgress"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr2, sbc_name, "conf", sbc_dref)
    add_eth_ctrl_egress_parameters_to_container(mdc_ctnr, sbc_dref, xgrs_cfg, sch_cfg)

    # Fill parameters EthCtrlConfigIngress to the sub-container
    sbc_name = "EthCtrlConfigIngress"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr2, sbc_name, "conf", sbc_dref)
    add_eth_ctrl_ingress_parameters_to_container(mdc_ctnr, sbc_dref, xgrs_cfg)



def update_eth_driver_to_container(ctnrname, root, eth_configs):
    rctnrblk = lib_conf.find_ecuc_container_block(ctnrname, root)
    
    # Delete node to rewrite new values
    if None != rctnrblk:
        root.remove(rctnrblk)
    
    # # pull data from UI
    # eth_configs[ctnrname][0].get()

    # Create a new container - Eth Driver
    dref = "/AUTOSAR/EcucDefs/Eth/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # # Parameters
    # params = ET.SubElement(ctnrblk, "PARAMETER-VALUES")
    # refname = dref+"/SpiMaxChannel"
    # lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiMaxChannel"]))
    # refname = dref+"/SpiMaxJob"
    # lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiMaxJob"]))
    # refname = dref+"/SpiMaxSequence"
    # lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiMaxSequence"]))

    # Create a sub-container
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "EthCtrlConfig"
    for cfg in eth_configs:
        ecc_dref = dref+"/"+sctnr_name
        mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", ecc_dref)
        add_eth_ctrl_config_parameters_to_container(mdc_ctnr, ecc_dref, cfg.datavar[sctnr_name],
                            cfg.datavar["EthCtrlConfigXgressFifo"], cfg.datavar["EthCtrlConfigScheduler"])



def update_eth_general_to_container(ctnrname, root, eth_configs):
    rctnrblk = lib_conf.find_ecuc_container_block(ctnrname, root)

    # Delete node to rewrite new values
    if None != rctnrblk:
        root.remove(rctnrblk)

    # # pull data from UI
    # eth_configs[ctnrname][0].get()

    # Create a new container - SpiDriver
    dref = "/AUTOSAR/EcucDefs/Eth/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    return
    # Parameters
    params = ET.SubElement(ctnrblk, "PARAMETER-VALUES")
    refname = dref+"/SpiCancelApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiCancelApi"]))
    refname = dref+"/SpiChannelBuffersAllowed"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiChannelBuffersAllowed"]))
    refname = dref+"/SpiDevErrorDetect"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiDevErrorDetect"]))
    refname = dref+"/SpiHwStatusApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiHwStatusApi"]))
    refname = dref+"/SpiInterruptibleSeqAllowed"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiInterruptibleSeqAllowed"]))
    refname = dref+"/SpiLevelDelivered"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiLevelDelivered"]))
    refname = dref+"/SpiMainFunctionPeriod"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiMainFunctionPeriod"]))
    refname = dref+"/SpiSupportConcurrentSyncTransmit"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiSupportConcurrentSyncTransmit"]))
    refname = dref+"/SpiVersionInfoApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(eth_configs[ctnrname][0].datavar["SpiVersionInfoApi"]))



def print_eth_configs(eth_configs):
    for cfg in eth_configs:
        print(cfg.datavar)



# # This function updates NammaAUTOSAR Eth parameters into its container
def update_arxml(ar_file, eth_configs):
    # Following line is added to avoid ns0 prefix added
    ET.register_namespace('', "http://autosar.org/schema/r4.0")
    ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
    
    print("arxml_eth_write.py: update_arxml called!")
    print_eth_configs(eth_configs)
    
    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    ar_isp = lib_conf.find_ecuc_elements_block(root)
    if ar_isp == None:
        return
        
    # Now find if Mcu module-conf is already there in insertion-point
    modname = "Eth"
    modconf = lib_conf.find_module_conf_values(modname, ar_isp)
    if modconf == None:
        modconf = lib_conf.insert_ecuc_module_conf(ar_isp, modname)
   
    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    # Add Eth contents to CONTAINER
    update_eth_driver_to_container("EthConfigSet", containers, eth_configs)
    update_eth_general_to_container("EthGeneral", containers, eth_configs)

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: Eth Configs are saved to " + ar_file)    



