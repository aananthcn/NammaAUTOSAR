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



def add_spi_chan_parameters_to_container(ctnr, cdref, chan_cfg):
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refname = cdref+"/SpiChannelId"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(chan_cfg.datavar["SpiChannelId"]))
    refname = cdref+"/SpiChannelType"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(chan_cfg.datavar["SpiChannelType"]))
    refname = cdref+"/SpiDataWidth"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(chan_cfg.datavar["SpiDataWidth"]))
    refname = cdref+"/SpiDefaultData"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(chan_cfg.datavar["SpiDefaultData"]))
    refname = cdref+"/SpiEbMaxLength"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(chan_cfg.datavar["SpiEbMaxLength"]))
    refname = cdref+"/SpiIbNBuffers"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(chan_cfg.datavar["SpiIbNBuffers"]))
    refname = cdref+"/SpiTransferStart"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(chan_cfg.datavar["SpiTransferStart"]))



def add_spi_exd_parameters_to_container(ctnr, cdref, exd_cfg):
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refname = cdref+"/SpiBaudrate"
    lib_conf.insert_conf_param(params, refname, "numerical", "float", str(exd_cfg.datavar["SpiBaudrate"]))
    refname = cdref+"/SpiCsIdentifier"
    lib_conf.insert_conf_param(params, refname, "text", "string", str(exd_cfg.datavar["SpiCsIdentifier"]))
    refname = cdref+"/SpiCsPolarity"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(exd_cfg.datavar["SpiCsPolarity"]))
    refname = cdref+"/SpiCsSelection"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(exd_cfg.datavar["SpiCsSelection"]))
    refname = cdref+"/SpiDataShiftEdge"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(exd_cfg.datavar["SpiDataShiftEdge"]))
    refname = cdref+"/SpiEnableCs"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(exd_cfg.datavar["SpiEnableCs"]))
    refname = cdref+"/SpiHwUnit"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(exd_cfg.datavar["SpiHwUnit"]))
    refname = cdref+"/SpiShiftClockIdleLevel"
    lib_conf.insert_conf_param(params, refname, "numerical", "enum", str(exd_cfg.datavar["SpiShiftClockIdleLevel"]))
    refname = cdref+"/SpiTimeClk2Cs"
    lib_conf.insert_conf_param(params, refname, "numerical", "float", str(exd_cfg.datavar["SpiTimeClk2Cs"]))
    refname = cdref+"/SpiTimeCs2Clk"
    lib_conf.insert_conf_param(params, refname, "numerical", "float", str(exd_cfg.datavar["SpiTimeCs2Clk"]))
    refname = cdref+"/SpiTimeCs2Cs"
    lib_conf.insert_conf_param(params, refname, "numerical", "float", str(exd_cfg.datavar["SpiTimeCs2Cs"]))



def add_spi_job_parameters_to_container(ctnr, cdref, job_cfg):
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refname = cdref+"/SpiJobEndNotification"
    lib_conf.insert_conf_param(params, refname, "text", "func", str(job_cfg.datavar["SpiJobEndNotification"]))
    refname = cdref+"/SpiJobId"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(job_cfg.datavar["SpiJobId"]))
    refname = cdref+"/SpiJobPriority"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(job_cfg.datavar["SpiJobPriority"]))

    # sub-container 2
    subctnr2 = ET.SubElement(ctnr, "SUB-CONTAINERS")
    subctnr2_name = "SpiChannelList"
    dref2 = cdref+"/"+subctnr2_name
    cctnrblk2 = lib_conf.insert_conf_container(subctnr2, subctnr2_name, "conf", dref2)
    params = ET.SubElement(cctnrblk2, "PARAMETER-VALUES")
    refname = dref2+"/SpiChannelIndex"
    for chan in job_cfg.datavar["SpiChannelList"]:
        lib_conf.insert_conf_param(params, refname, "numerical", "int", str(chan))


def add_spi_seq_parameters_to_container(ctnr, cdref, seq_cfg):
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refname = cdref+"/SpiInterruptibleSequence"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(seq_cfg.datavar["SpiInterruptibleSequence"]))
    refname = cdref+"/SpiSeqEndNotification"
    lib_conf.insert_conf_param(params, refname, "text", "func", str(seq_cfg.datavar["SpiSeqEndNotification"]))
    refname = cdref+"/SpiSequenceId"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(seq_cfg.datavar["SpiSequenceId"]))

    # sub-container 2
    subctnr2 = ET.SubElement(ctnr, "SUB-CONTAINERS")
    subctnr2_name = "SpiJobAssignment"
    dref2 = cdref+"/"+subctnr2_name
    cctnrblk2 = lib_conf.insert_conf_container(subctnr2, subctnr2_name, "conf", dref2)
    params = ET.SubElement(cctnrblk2, "PARAMETER-VALUES")
    refname = dref2+"/SpiJob"
    for job in seq_cfg.datavar["SpiJobAssignment"]:
        lib_conf.insert_conf_param(params, refname, "numerical", "int", str(job))


def add_spi_chanlist_parameters_to_container(ctnr, cdref, chlst_cfg):
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refname = cdref+"/SpiInterruptibleSequence"
    lib_conf.insert_conf_param(params, refname, "numerical", "bool", str(chlst_cfg.datavar["SpiInterruptibleSequence"]))
    refname = cdref+"/SpiSeqEndNotification"



def update_spi_driver_to_container(ctnrname, root, spi_configs):
    rctnrblk = lib_conf.find_ecuc_container_block(ctnrname, root)
    
    # Delete node to rewrite new values
    if None != rctnrblk:
        root.remove(rctnrblk)
    
    # Create a new container - SpiDriver
    dref = "/AUTOSAR/EcucDefs/Spi/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Parameters
    params = ET.SubElement(ctnrblk, "PARAMETER-VALUES")
    refname = dref+"/SpiMaxChannel"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiMaxChannel"]))
    refname = dref+"/SpiMaxJob"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiMaxJob"]))
    refname = dref+"/SpiMaxSequence"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiMaxSequence"]))

    # Create a sub-container    
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    for chan in spi_configs["SpiChannel"]:
        subctnr1_name = "SpiChannel"
        dref1 = dref+"/"+subctnr1_name
        cctnrblk1 = lib_conf.insert_conf_container(subctnr1, subctnr1_name, "conf", dref1)
        add_spi_chan_parameters_to_container(cctnrblk1, dref1, chan)

    for dev in spi_configs["SpiExternalDevice"]:
        subctnr1_name = "SpiExternalDevice"
        dref1 = dref+"/"+subctnr1_name
        cctnrblk1 = lib_conf.insert_conf_container(subctnr1, subctnr1_name, "conf", dref1)
        add_spi_exd_parameters_to_container(cctnrblk1, dref1, dev)

    for job in spi_configs["SpiJob"]:
        subctnr1_name = "SpiJob"
        dref1 = dref+"/"+subctnr1_name
        cctnrblk1 = lib_conf.insert_conf_container(subctnr1, subctnr1_name, "conf", dref1)
        add_spi_job_parameters_to_container(cctnrblk1, dref1, job)


    for seq in spi_configs["SpiSequence"]:
        subctnr1_name = "SpiSequence"
        dref1 = dref+"/"+subctnr1_name
        cctnrblk1 = lib_conf.insert_conf_container(subctnr1, subctnr1_name, "conf", dref1)
        add_spi_seq_parameters_to_container(cctnrblk1, dref1, seq)




def update_spi_general_to_container(ctnrname, root, spi_configs):
    rctnrblk = lib_conf.find_ecuc_container_block(ctnrname, root)

    # Delete node to rewrite new values
    if None != rctnrblk:
        root.remove(rctnrblk)

    # Create a new container - SpiDriver
    dref = "/AUTOSAR/EcucDefs/Spi/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Parameters
    params = ET.SubElement(ctnrblk, "PARAMETER-VALUES")
    refname = dref+"/SpiCancelApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiCancelApi"]))
    refname = dref+"/SpiChannelBuffersAllowed"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiChannelBuffersAllowed"]))
    refname = dref+"/SpiDevErrorDetect"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiDevErrorDetect"]))
    refname = dref+"/SpiHwStatusApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiHwStatusApi"]))
    refname = dref+"/SpiInterruptibleSeqAllowed"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiInterruptibleSeqAllowed"]))
    refname = dref+"/SpiLevelDelivered"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiLevelDelivered"]))
    refname = dref+"/SpiMainFunctionPeriod"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiMainFunctionPeriod"]))
    refname = dref+"/SpiSupportConcurrentSyncTransmit"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiSupportConcurrentSyncTransmit"]))
    refname = dref+"/SpiVersionInfoApi"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs[ctnrname][0].datavar["SpiVersionInfoApi"]))



def update_spi_pubinfo_to_container(ctnrname, root, spi_configs):
    rctnrblk = lib_conf.find_ecuc_container_block(ctnrname, root)

    # Delete node to rewrite new values
    if None != rctnrblk:
        root.remove(rctnrblk)

    # Create a new container - SpiDriver
    dref = "/AUTOSAR/EcucDefs/Spi/"+ctnrname
    ctnrblk = lib_conf.insert_conf_container(root, ctnrname, "conf", dref)

    # Parameters
    params = ET.SubElement(ctnrblk, "PARAMETER-VALUES")
    refname = dref+"/SpiMaxHwUnit"
    lib_conf.insert_conf_param(params, refname, "numerical", "int", str(spi_configs["SpiDriver"][0].datavar["SpiMaxHwUnit"]))



# # This function updates NammaAUTOSAR Spi parameters into its container
# def update_spi_info_to_container(root, spi_configs):
#     # for key in spi_configs:
#     #     print("#################### ", key, " ############################")
#     #     print("## datavar")
#     #     for item in spi_configs[key]:
#     #         print("\t", item.datavar)
#     #     print("## dispvar")
#     #     for item in spi_configs[key]:
#     #         print("\t", item.get())



# Write ARXML with dio info
def update_arxml(ar_file, spi_configs):
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
    modname = "Spi"
    modconf = lib_conf.find_module_conf_values(modname, ar_isp)
    if modconf == None:
        modconf = lib_conf.insert_ecuc_module_conf(ar_isp, modname)
   
    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    # Add Spi Tab contents to CONTAINER
    update_spi_driver_to_container("SpiDriver", containers, spi_configs)
    update_spi_general_to_container("SpiGeneral", containers, spi_configs)
    update_spi_pubinfo_to_container("SpiPublishedInformation", containers, spi_configs)

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: Spi Configs are saved to " + ar_file)    



# def parse_arxml_dioconfig(containers):
#     spi_n_pins = None
#     spi_configs = []
#     spi_groups = []
    
#     # locate SpiConfig
#     ctnrname = "SpiConfig"
#     ctnrblk = lib_conf.find_ecuc_container_block(ctnrname, containers)
#     if lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
#         return None
    
#     # now locate SpiPort
#     spi_cfg_ctnr = ctnrblk
#     spi_sub_ctnr = None
#     dioport_ctnr = None
#     for ecuc_ctnr in ctnrblk:
#         if lib_conf.get_tag(ecuc_ctnr) == "SUB-CONTAINERS":
#             spi_sub_ctnr = ecuc_ctnr
#             for ecuc_ctnr in spi_sub_ctnr:
#                 if lib_conf.get_tag(ecuc_ctnr) == "ECUC-CONTAINER-VALUE":
#                     ctnrblk = ecuc_ctnr
#                     for item in ctnrblk:
#                         if lib_conf.get_tag(item) == "SHORT-NAME":
#                             if item.text == "SpiPort":
#                                 spi_n_pins = len(spi_sub_ctnr) # we have found the right SUB-CONTAINER!!
#                                 dioport_ctnr = ctnrblk
#                                 # Note: breaking based on assumption that there will be only one port ;-)
#                                 break
#                                 # this will be extended as dioport_ctnr[] list later, as I don't know if the
#                                 # current ARXML format that I understand is correct.

#     # get the 'SpiPortId' of this SpiPort
#     spi_port_id_cfg = {}
#     params = lib_conf.get_param_list(dioport_ctnr)
#     for par in params:
#         spi_port_id_cfg[par["tag"]] = par["val"]
    
#     # parse dio config from subcontainer
#     nodes = lib_conf.findall_subcontainers_with_name("SpiChannel", dioport_ctnr)
#     if nodes != None:
#         for node in nodes:
#             params = lib_conf.get_param_list(node)
#             cfg = {}
#             for par in params:
#                 cfg[par["tag"]] = par["val"]
#             cfg["SpiPortId"] = spi_port_id_cfg["SpiPortId"]
#             spi_configs.append(cfg)
    
#     # parse dio group from subcontainer
#     nodes = lib_conf.findall_subcontainers_with_name("SpiChannelGroup", dioport_ctnr)
#     if nodes != None:
#         for node in nodes:
#             params = lib_conf.get_param_list(node)
#             cfg = {}
#             for par in params:
#                 cfg[par["tag"]] = par["val"]
#             cfg["SpiPortId"] = spi_port_id_cfg["SpiPortId"]
#             spi_groups.append(cfg)
    

#     return spi_n_pins, spi_configs, spi_groups



def parse_spi_general(cname, containers):
    spi_general = {}
    ctnrblk = lib_conf.find_ecuc_container_block(cname, containers)
    if not ctnrblk or lib_conf.get_tag(ctnrblk) != "ECUC-CONTAINER-VALUE":
        return None
    params = lib_conf.get_param_list(ctnrblk)
    for par in params:
        spi_general[par["tag"]] = par["val"]
    
    return spi_general


# This function parses ARXML and extract the Spi information
# Returns: No of spi_configs, Spi pin dictionary
def parse_arxml(ar_file):
    if ar_file == None:
        return None

    # empty dictionary
    spi_configs = {}

    # Read ARXML File
    tree = ET.parse(ar_file)
    root = tree.getroot()

    # locate ELEMENTS block
    elems = lib_conf.find_ecuc_elements_block(root)
    if elems == None:
        return

    # locate Mcu module configuration under ELEMENTS
    modconf = lib_conf.find_module_conf_values("Spi", elems)

    # locate container
    containers = lib_conf.find_containers_in_modconf(modconf)
    if containers == None:
        return

    spi_general = parse_spi_general("SpiGeneral", containers)
    print("parse_arxml->SpiGeneral", spi_general)
    
    # return spi_n_pins, spi_configs, spi_groups, spi_general

