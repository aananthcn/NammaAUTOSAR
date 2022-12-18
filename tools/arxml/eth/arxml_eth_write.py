#
# Created on Sun Dec 11 2022 11:47:00 PM
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



def add_eth_ctrl_shape_parameters_to_container(ctnr, dref, shp_cfg):
    if not shp_cfg:
        print("Warning: ARXML write - EthCtrlConfigShaper is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthCtrlConfigShaperIdleSlope"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(shp_cfg["EthCtrlConfigShaperIdleSlope"]))
    refname = dref+"/EthCtrlConfigShaperMaxCredit"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(shp_cfg["EthCtrlConfigShaperMaxCredit"]))
    refname = dref+"/EthCtrlConfigShaperMinCredit"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(shp_cfg["EthCtrlConfigShaperMinCredit"]))



def add_eth_ctrl_sched_parameters_to_container(ctnr, dref, sch_cfg):
    if not sch_cfg:
        print("Warning: ARXML write - EthCtrlConfigScheduler is empty!")
        return

    # Create a sub-container for EthCtrlConfigScheduler
    subctnr = ET.SubElement(ctnr, "SUB-CONTAINERS")

    # Fill parameters EthCtrlConfigScheduler to the sub-container
    sbc_name = "EthCtrlConfigSchedulerPredecessor"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr, sbc_name, "conf", sbc_dref)

    # Insert PARAMETER block
    params = ET.SubElement(mdc_ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthCtrlConfigSchedulerPredecessorOrder"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(sch_cfg["EthCtrlConfigSchedulerPredecessorOrder"]))



def add_eth_ctrl_fifo_out_parameters_to_container(ctnr, dref, egr_cfg):
    if not egr_cfg:
        print("Warning: ARXML write - EthCtrlConfigEgressFifo is empty!")
        return

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



def add_eth_ctrl_egress_parameters_to_container(ctnr, dref, egr_cfg, sch_cfg, shp_cfg):
    # Create a sub-container for 3 items
    subctnr3 = ET.SubElement(ctnr, "SUB-CONTAINERS")

    # Fill parameters EthCtrlConfigEgressFifo to the sub-container
    sbc_name = "EthCtrlConfigEgressFifo"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr3, sbc_name, "conf", sbc_dref)
    add_eth_ctrl_fifo_out_parameters_to_container(mdc_ctnr, sbc_dref, egr_cfg)

    # Fill parameters EthCtrlConfigScheduler to the sub-container
    sbc_name = "EthCtrlConfigScheduler"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr3, sbc_name, "conf", sbc_dref)
    add_eth_ctrl_sched_parameters_to_container(mdc_ctnr, sbc_dref, sch_cfg)

    # Fill parameters EthCtrlConfigShaper to the sub-container
    sbc_name = "EthCtrlConfigShaper"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr3, sbc_name, "conf", sbc_dref)
    add_eth_ctrl_shape_parameters_to_container(mdc_ctnr, sbc_dref, shp_cfg)



def add_eth_ctrl_fifo_in_parameters_to_container(ctnr, dref, igr_cfg):
    if not igr_cfg:
        print("Warning: ARXML write - EthCtrlConfigIngressFifo is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthCtrlConfigIngressFifoBufLenByte"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(igr_cfg["EthCtrlConfigIngressFifoBufLenByte"]))
    refname = dref+"/EthCtrlConfigIngressFifoBufTotal"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(igr_cfg["EthCtrlConfigIngressFifoBufTotal"]))
    refname = dref+"/EthCtrlConfigIngressFifoIdx"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(igr_cfg["EthCtrlConfigIngressFifoIdx"]))
    refname = dref+"/EthCtrlConfigIngressFifoPriorityAssignment"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(igr_cfg["EthCtrlConfigIngressFifoPriorityAssignment"]))

	

def add_eth_ctrl_ingress_parameters_to_container(ctnr, dref, igr_cfg):
    if not igr_cfg:
        print("Warning: ARXML write - EthCtrlConfigIngress is empty!")
        return

    # Create a sub-container for 3 items
    subctnr3 = ET.SubElement(ctnr, "SUB-CONTAINERS")

    # Fill parameters EthCtrlConfigIngressFifo to the sub-container
    sbc_name = "EthCtrlConfigIngressFifo"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr3, sbc_name, "conf", sbc_dref)
    add_eth_ctrl_fifo_in_parameters_to_container(mdc_ctnr, sbc_dref, igr_cfg)



def add_eth_ctrl_spi_parameters_to_container(ctnr, dref, spi_cfg):
    if not spi_cfg:
        print("Warning: ARXML write - EthCtrlConfigSpiConfiguration is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/EthCtrlConfigSpiChunkPayloadSize"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_cfg["EthCtrlConfigSpiChunkPayloadSize"]))
    refname = dref+"/EthCtrlConfigSpiCommRetries"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_cfg["EthCtrlConfigSpiCommRetries"]))
    refname = dref+"/EthCtrlConfigSpiCommTimeout"
    lib_conf.insert_conf_param(params, refname, "numerical", "float", str(spi_cfg["EthCtrlConfigSpiCommTimeout"]))
    refname = dref+"/EthCtrlConfigSpiEnableControlDataProtection"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(spi_cfg["EthCtrlConfigSpiEnableControlDataProtection"]))
    refname = dref+"/EthCtrlConfigSpiEnableRxCSAlign"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(spi_cfg["EthCtrlConfigSpiEnableRxCSAlign"]))
    refname = dref+"/EthCtrlConfigSpiEnableRxCutThrough"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(spi_cfg["EthCtrlConfigSpiEnableRxCutThrough"]))
    refname = dref+"/EthCtrlConfigSpiEnableRxZeroAlign"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(spi_cfg["EthCtrlConfigSpiEnableRxZeroAlign"]))
    refname = dref+"/EthCtrlConfigSpiEnableTransmitDataHdrSequence"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(spi_cfg["EthCtrlConfigSpiEnableTransmitDataHdrSequence"]))
    refname = dref+"/EthCtrlConfigSpiEnableTxChecksum"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(spi_cfg["EthCtrlConfigSpiEnableTxChecksum"]))
    refname = dref+"/EthCtrlConfigSpiEnableTxCutThrough"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(spi_cfg["EthCtrlConfigSpiEnableTxCutThrough"]))
    refname = dref+"/EthCtrlConfigSpiSelectTimeStamp"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(spi_cfg["EthCtrlConfigSpiSelectTimeStamp"]))
    refname = dref+"/EthCtrlConfigSpiTransmitCreditThreshold"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_cfg["EthCtrlConfigSpiTransmitCreditThreshold"]))
    refname = dref+"/EthCtrlConfigSpiAccessSynchronous"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(spi_cfg["EthCtrlConfigSpiAccessSynchronous"]))
    refname = dref+"/EthCtrlConfigSpiSequenceName"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(spi_cfg["EthCtrlConfigSpiSequenceName"]))



def add_eth_ctrl_config_parameters_to_container(ctnr, dref, ecc_cfg, xgrs_cfg, sch_cfg, shp_cfg, spi_cfg):
    if not ecc_cfg:
        print("Warning: ARXML write - EthCtrlConfig is empty!")
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
    add_eth_ctrl_egress_parameters_to_container(mdc_ctnr, sbc_dref, xgrs_cfg, sch_cfg, shp_cfg)

    # Fill parameters EthCtrlConfigIngress to the sub-container
    sbc_name = "EthCtrlConfigIngress"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr2, sbc_name, "conf", sbc_dref)
    add_eth_ctrl_ingress_parameters_to_container(mdc_ctnr, sbc_dref, xgrs_cfg)

    if not spi_cfg:
        return
    # Fill parameters EthCtrlConfigSpiConfiguration to the sub-container
    sbc_name = "EthCtrlConfigSpiConfiguration"
    sbc_dref = dref+"/"+sbc_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr2, sbc_name, "conf", sbc_dref)
    add_eth_ctrl_spi_parameters_to_container(mdc_ctnr, sbc_dref, spi_cfg)



def update_eth_configset_to_container(ctnrname, root, eth_cfg):
    # Create a new container - Eth Driver
    dref = "/AUTOSAR/EcucDefs/Eth/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Create a sub-container
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "EthCtrlConfig"
    ecc_dref = dref+"/"+sctnr_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", ecc_dref)
    add_eth_ctrl_config_parameters_to_container(mdc_ctnr, ecc_dref, eth_cfg.datavar[sctnr_name],
                        eth_cfg.datavar["EthCtrlConfigXgressFifo"], eth_cfg.datavar["EthCtrlConfigScheduler"],
                        eth_cfg.datavar["EthCtrlConfigShaper"], eth_cfg.datavar["EthCtrlConfigSpiConfiguration"])


def add_eth_general_parameters_to_container(ctnr, dref, gen_cfg):
    if not gen_cfg:
        print("Warning: ARXML write - EthGeneral is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    pref = dref+"/EthIndex"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(gen_cfg["EthIndex"]))
    pref = dref+"/EthDevErrorDetect"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthDevErrorDetect"]))
    pref = dref+"/EthMainFunctionPeriod"
    lib_conf.insert_conf_param(params, pref, "numerical", "float", str(gen_cfg["EthMainFunctionPeriod"]))
    pref = dref+"/EthGetCounterValuesApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthGetCounterValuesApi"]))
    pref = dref+"/EthGetRxStatsApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthGetRxStatsApi"]))
    pref = dref+"/EthGetTxErrorCounterValuesApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthGetTxErrorCounterValuesApi"]))
    pref = dref+"/EthGetTxStatsApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthGetTxStatsApi"]))
    pref = dref+"/EthGlobalTimeSupport"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthGlobalTimeSupport"]))
    pref = dref+"/EthMaxCtrlsSupported"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(gen_cfg["EthMaxCtrlsSupported"]))
    pref = dref+"/EthVersionInfoApi"
    lib_conf.insert_conf_param(params, pref, "numerical", "bool", str(gen_cfg["EthVersionInfoApi"]))



def add_eth_ctrl_offload_parameters_to_container(ctnr, dref, ofl_cfg):
    if not ofl_cfg:
        print("Warning: ARXML write - EthCtrlOffloading is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    pref = dref+"/EthCtrlEnableOffloadChecksumIPv4"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(ofl_cfg["EthCtrlEnableOffloadChecksumIPv4"]))
    pref = dref+"/EthCtrlEnableOffloadChecksumICMP"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(ofl_cfg["EthCtrlEnableOffloadChecksumICMP"]))
    pref = dref+"/EthCtrlEnableOffloadChecksumTCP"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(ofl_cfg["EthCtrlEnableOffloadChecksumTCP"]))
    pref = dref+"/EthCtrlEnableOffloadChecksumUDP"
    lib_conf.insert_conf_param(params, pref, "numerical", "int", str(ofl_cfg["EthCtrlEnableOffloadChecksumUDP"]))



def update_eth_general_to_container(ctnrname, root, eth_cfg):
    # Create a new container - EthGeneral
    dref = "/AUTOSAR/EcucDefs/Eth/"+ctnrname
    mdc_ctnr = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)
    add_eth_general_parameters_to_container(mdc_ctnr, dref, eth_cfg.datavar["EthGeneral"])

    # Create a sub-container
    subctnr1 = ET.SubElement(mdc_ctnr, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "EthCtrlOffloading"
    dref = dref+"/"+sctnr_name
    mdc_ctnr = lib_conf.insert_conf_container(subctnr1, sctnr_name, "conf", dref)
    add_eth_ctrl_offload_parameters_to_container(mdc_ctnr, dref, eth_cfg.datavar[sctnr_name])



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

    # remove all Eth configs
    eth_modconfs = lib_conf.findall_module_configs("Eth", ar_isp)
    for conf in eth_modconfs:
        print(conf)
        ar_isp.remove(conf)

    # insert Eth configs
    for cfg in eth_configs:
        modconf = lib_conf.insert_ecuc_module_conf(ar_isp, "Eth")

        # locate container
        containers = lib_conf.find_containers_in_modconf(modconf)
        if containers == None:
            return

        # Add Eth contents to CONTAINER
        update_eth_configset_to_container("EthConfigSet", containers, cfg)
        update_eth_general_to_container("EthGeneral", containers, cfg)

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: Eth Configs are saved to " + ar_file)    
