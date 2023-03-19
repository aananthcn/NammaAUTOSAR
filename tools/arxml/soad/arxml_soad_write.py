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



def add_soad_sk_remote_addr_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdSocketRemoteAddress is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/SoAdSocketRemotePort"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketRemotePort"]))
    refname = dref+"/SoAdSocketRemoteIpAddress"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdSocketRemoteIpAddress"]))



def add_soad_skconnection_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdSocketConnection is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/SoAdSocketId"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketId"]))

    # Create a sub-container
    subctnr3 = ET.SubElement(ctnr, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "SoAdSocketRemoteAddress"
    sctnr_dref = dref+"/"+sctnr_name
    mdc_ctnr = lib_conf.insert_ecuc_container(subctnr3, sctnr_name, "conf", sctnr_dref)
    add_soad_sk_remote_addr_config_params_to_container(mdc_ctnr, sctnr_dref, cfg)



def add_soad_skt_tcp_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdSocketTcp is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdSocketTcpRetransmissionTimeout"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpRetransmissionTimeout"]))
    refname = dref+"/SoAdSocketTcpAutoConnectTimeout"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpAutoConnectTimeout"]))
    refname = dref+"/SoAdSocketTcpInitiate"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpInitiate"]))
    refname = dref+"/SoAdSocketTcpNoDelay"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpNoDelay"]))
    refname = dref+"/SoAdSocketTcpImmediateTpTxConfirmation"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpImmediateTpTxConfirmation"]))
    refname = dref+"/SoAdSocketTcpTxQuota"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpTxQuota"]))
    refname = dref+"/SoAdSocketTcpKeepAlive"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpKeepAlive"]))
    refname = dref+"/SoAdSocketTcpKeepAliveProbesMax"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpKeepAliveProbesMax"]))
    refname = dref+"/SoAdSocketTcpKeepAliveInterval"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpKeepAliveInterval"]))
    refname = dref+"/SoAdSocketTcpKeepAliveTime"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketTcpKeepAliveTime"]))

    # Insert references
    if "SoAdSocketTCPOptionFilterRef" in cfg:
        refname = dref+"/SoAdSocketTCPOptionFilterRef"
        refdest = str(cfg["SoAdSocketTCPOptionFilterRef"])
        lib_conf.insert_ecuc_reference(refs, refname, refdest)
    if "SoAdSocketTcpTlsConnectionRef" in cfg:
        refname = dref+"/SoAdSocketTcpTlsConnectionRef"
        refdest = str(cfg["SoAdSocketTcpTlsConnectionRef"])
        lib_conf.insert_ecuc_reference(refs, refname, refdest)



def add_soad_skt_udp_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdSocketUdp is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    refname = dref+"/SoAdSocketUdpListenOnly"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdSocketUdpListenOnly"]))
    refname = dref+"/SoAdSocketUdpAliveSupervisionTimeout"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketUdpAliveSupervisionTimeout"]))
    refname = dref+"/SoAdSocketnPduUdpTxBufferMin"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketnPduUdpTxBufferMin"]))
    refname = dref+"/SoAdSocketUdpTriggerTimeout"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdSocketUdpTriggerTimeout"]))
    refname = dref+"/SoAdSocketUdpStrictHeaderLenCheckEnabled"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdSocketUdpStrictHeaderLenCheckEnabled"]))
    refname = dref+"/SoAdSocketUdpChecksumEnabled"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdSocketUdpChecksumEnabled"]))



def add_soad_skprotocol_config_params_to_container(ctnr, dref, cfg, choice):
    if not cfg:
        print("Warning: ARXML write - SoAdSocketProtocol choice is empty!")
        return

    # Create a sub-container
    subctnr2 = ET.SubElement(ctnr, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    if choice == "TCP":
        sctnr_name = "SoAdSocketTcp"
    else:
        sctnr_name = "SoAdSocketUdp"
    sctnr_dref = dref+"/"+sctnr_name
    mdc_ctnr = lib_conf.insert_ecuc_container(subctnr2, sctnr_name, "conf", sctnr_dref)
    if choice == "TCP":
        add_soad_skt_tcp_params_to_container(mdc_ctnr, sctnr_dref, cfg)
    else:
        add_soad_skt_udp_params_to_container(mdc_ctnr, sctnr_dref, cfg)



def add_soad_skconngrp_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdSocketConnectionGroup is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdPduHeaderEnable"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdPduHeaderEnable"]))
    refname = dref+"/SoAdSocketPathMTUEnable"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketPathMTUEnable"]))
    refname = dref+"/SoAdSocketAutomaticSoConSetup"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketAutomaticSoConSetup"]))
    refname = dref+"/SoAdSocketIpAddrAssignmentChgNotification"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketIpAddrAssignmentChgNotification"]))
    refname = dref+"/SoAdSocketLocalPort"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketLocalPort"]))
    refname = dref+"/SoAdSocketSoConModeChgBswMNotification"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketSoConModeChgBswMNotification"]))
    refname = dref+"/SoAdSocketSoConModeChgNotification"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketSoConModeChgNotification"]))
    refname = dref+"/SoAdSocketTpRxBufferMin"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketTpRxBufferMin"]))
    refname = dref+"/SoAdSocketFramePriority"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketFramePriority"]))
    refname = dref+"/SoAdSocketMsgAcceptanceFilterEnabled"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketMsgAcceptanceFilterEnabled"]))
    refname = dref+"/SoAdSocketFlowLabel"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketFlowLabel"]))
    refname = dref+"/SoAdSocketDifferentiatedServicesField"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdSocketDifferentiatedServicesField"]))

    # Insert references
    if "SoAdSocketLocalAddressRef" in cfg:
        refname = dref+"/SoAdSocketLocalAddressRef"
        refdest = str(cfg["SoAdSocketLocalAddressRef"])
        lib_conf.insert_ecuc_reference(refs, refname, refdest)
    if "SoAdSocketSoConModeChgNotifUpperLayerRef" in cfg:
        refname = dref+"/SoAdSocketSoConModeChgNotifUpperLayerRef"
        refdest = str(cfg["SoAdSocketSoConModeChgNotifUpperLayerRef"])
        lib_conf.insert_ecuc_reference(refs, refname, refdest)

    # Create a sub-container
    subctnr2 = ET.SubElement(ctnr, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "SoAdSocketProtocol"
    sctnr_dref = dref+"/"+sctnr_name
    mdc_ctnr = lib_conf.insert_ecuc_container(subctnr2, sctnr_name, "choice", sctnr_dref)
    choice = cfg["SoAdSocketProtocolChoice"]
    add_soad_skprotocol_config_params_to_container(mdc_ctnr, sctnr_dref, cfg[sctnr_name], choice)

    sctnr_name = "SoAdSocketConnection"
    sctnr_dref = dref+"/"+sctnr_name
    for ch_cfg in cfg[sctnr_name]:
        mdc_ctnr = lib_conf.insert_ecuc_container(subctnr2, sctnr_name, "conf", sctnr_dref)
        add_soad_skconnection_config_params_to_container(mdc_ctnr, sctnr_dref, ch_cfg)



def add_soad_routingrp_config_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdRoutingGroup is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdRoutingGroupId"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdRoutingGroupId"]))
    refname = dref+"/SoAdRoutingGroupIsEnabledAtInit"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdRoutingGroupIsEnabledAtInit"]))
    refname = dref+"/SoAdRoutingGroupTxTriggerable"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdRoutingGroupTxTriggerable"]))



def add_soad_pduroute_dest_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdPduRouteDest is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdTxPduHeaderId"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdTxPduHeaderId"]))
    refname = dref+"/SoAdTxUdpTriggerMode"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdTxUdpTriggerMode"]))
    refname = dref+"/SoAdTxUdpTriggerTimeout"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdTxUdpTriggerTimeout"]))

    # Insert references
    if "SoAdTxSocketConnOrSocketConnBundleRef" in cfg:
        refname = dref+"/SoAdTxSocketConnOrSocketConnBundleRef"
        refdest = str(cfg["SoAdTxSocketConnOrSocketConnBundleRef"])
        lib_conf.insert_ecuc_reference(refs, refname, refdest)

    if "SoAdTxRoutingGroupRef" in cfg:
        refname = dref+"/SoAdTxRoutingGroupRef"
        refdest = str(cfg["SoAdTxRoutingGroupRef"])
        lib_conf.insert_ecuc_reference(refs, refname, refdest)



def add_soad_pduroute_params_to_container(ctnr, dref, cfg):
    if not cfg:
        print("Warning: ARXML write - SoAdPduRoute is empty!")
        return

    # Insert PARAMETER & REFERENCE block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")
    refs = ET.SubElement(ctnr, "REFERENCE-VALUES")

    # Insert parameters
    refname = dref+"/SoAdTxPduId"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "int", str(cfg["SoAdTxPduId"]))
    refname = dref+"/SoAdTxUpperLayerType"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdTxUpperLayerType"]))
    refname = dref+"/SoAdTxPduCollectionSemantics"
    lib_conf.insert_ecuc_param(params, refname, "numerical", "enum", str(cfg["SoAdTxPduCollectionSemantics"]))

    # Insert references
    if "SoAdTxPduRef" in cfg:
        refname = dref+"/SoAdTxPduRef"
        refdest = str(cfg["SoAdTxPduRef"])
        lib_conf.insert_ecuc_reference(refs, refname, refdest)

    # Create a sub-container
    subctnr2 = ET.SubElement(ctnr, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "SoAdPduRouteDest"
    sctnr_dref = dref+"/"+sctnr_name
    for ch_cfg in cfg[sctnr_name]:
        mdc_ctnr = lib_conf.insert_ecuc_container(subctnr2, sctnr_name, "conf", sctnr_dref)
        add_soad_pduroute_dest_params_to_container(mdc_ctnr, sctnr_dref, ch_cfg)



def update_soad_configs_to_container(ctnrname, root, soad_cfg):
    # Create a new container - SoAd Driver
    dref = "/AUTOSAR/EcucDefs/SoAd/"+ctnrname
    ctnrblk = lib_conf.insert_ecuc_container(root, ctnrname, "conf", dref)

    # Create a sub-container
    subctnr1 = ET.SubElement(ctnrblk, "SUB-CONTAINERS")

    # Create ECUC Module Configs under above Sub-container
    sctnr_name = "SoAdPduRoute"
    sctnr_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_ecuc_container(subctnr1, sctnr_name, "conf", sctnr_dref)
        add_soad_pduroute_params_to_container(mdc_ctnr, sctnr_dref, cfg)

    sctnr_name = "SoAdRoutingGroup"
    sctnr_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_ecuc_container(subctnr1, sctnr_name, "conf", sctnr_dref)
        add_soad_routingrp_config_params_to_container(mdc_ctnr, sctnr_dref, cfg)

    sctnr_name = "SoAdSocketConnectionGroup"
    sctnr_dref = dref+"/"+sctnr_name
    for i, cfg in enumerate(soad_cfg[0].datavar[sctnr_name]):
        mdc_ctnr = lib_conf.insert_ecuc_container(subctnr1, sctnr_name, "conf", sctnr_dref)
        add_soad_skconngrp_config_params_to_container(mdc_ctnr, sctnr_dref, cfg)

    return # TODO: remove this after development

    sctnr_name = "SoAdSocketRoute"
    sctnr_dref = dref+"/"+sctnr_name
    for cfg in soad_cfg[0].datavar[sctnr_name]:
        mdc_ctnr = lib_conf.insert_ecuc_container(subctnr1, sctnr_name, "conf", sctnr_dref)
        add_soad_tlsc_config_params_to_container(mdc_ctnr, sctnr_dref, cfg)



def update_soad_bswmodules_to_container(ctnrname, root, soad_cfg):
    for obj in soad_cfg:
        cfg = obj.datavar
        # Create a new container - SoAdBswModules
        dref = "/AUTOSAR/EcucDefs/SoAd/"+ctnrname
        ctnrblk = lib_conf.insert_ecuc_container(root, ctnrname, "conf", dref)

        # Insert PARAMETER & REFERENCE block
        params = ET.SubElement(ctnrblk, "PARAMETER-VALUES")
        refs = ET.SubElement(ctnrblk, "REFERENCE-VALUES")

        # Insert parameters
        refname = dref+"/SoAdIf"
        lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdIf"]))
        refname = dref+"/SoAdIfTriggerTransmit"
        lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdIfTriggerTransmit"]))
        refname = dref+"/SoAdIfTxConfirmation"
        lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdIfTxConfirmation"]))
        refname = dref+"/SoAdLocalIpAddrAssigmentChg"
        lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdLocalIpAddrAssigmentChg"]))
        refname = dref+"/SoAdSoConModeChg"
        lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdSoConModeChg"]))
        refname = dref+"/SoAdTp"
        lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdTp"]))
        refname = dref+"/SoAdUseCallerInfix"
        lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdUseCallerInfix"]))
        refname = dref+"/SoAdUseTypeInfix"
        lib_conf.insert_ecuc_param(params, refname, "numerical", "bool", str(cfg["SoAdUseTypeInfix"]))

        if "SoAdBswModuleRef" in cfg:
            refname = dref+"/SoAdBswModuleRef"
            refdest = str(cfg["SoAdBswModuleRef"])
            lib_conf.insert_ecuc_reference(refs, refname, refdest)



def add_soad_general_parameters_to_container(ctnr, dref, gen_cfg):
    if not gen_cfg:
        print("Warning: ARXML write - SoAdGeneral is empty!")
        return

    # Insert PARAMETER block
    params = ET.SubElement(ctnr, "PARAMETER-VALUES")

    # Insert parameters
    pref = dref+"/SoAdDevErrorDetect"
    lib_conf.insert_ecuc_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdDevErrorDetect"]))
    pref = dref+"/SoAdVersionInfoApi"
    lib_conf.insert_ecuc_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdVersionInfoApi"]))
    pref = dref+"/SoAdIPv6AddressEnabled"
    lib_conf.insert_ecuc_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdIPv6AddressEnabled"]))
    pref = dref+"/SoAdMainFunctionPeriod"
    lib_conf.insert_ecuc_param(params, pref, "numerical", "float", str(gen_cfg["SoAdMainFunctionPeriod"]))
    pref = dref+"/SoAdSoConMax"
    lib_conf.insert_ecuc_param(params, pref, "numerical", "int", str(gen_cfg["SoAdSoConMax"]))
    pref = dref+"/SoAdRoutingGroupMax"
    lib_conf.insert_ecuc_param(params, pref, "numerical", "int", str(gen_cfg["SoAdRoutingGroupMax"]))
    pref = dref+"/SoAdGetAndResetMeasurementDataApi"
    lib_conf.insert_ecuc_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdGetAndResetMeasurementDataApi"]))
    pref = dref+"/SoAdEnableSecurityEventReporting"
    lib_conf.insert_ecuc_param(params, pref, "numerical", "bool", str(gen_cfg["SoAdEnableSecurityEventReporting"]))
    pref = dref+"/SoAdSecurityEventRefs"
    lib_conf.insert_ecuc_param(params, pref, "text", "string", str(gen_cfg["SoAdSecurityEventRefs"]))



def update_soad_general_to_container(ctnrname, root, soad_cfg):
    # Create a new container - SoAdGeneral
    dref = "/AUTOSAR/EcucDefs/SoAd/"+ctnrname
    mdc_ctnr = lib_conf.insert_ecuc_container(root, ctnrname, "conf", dref)
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
    update_soad_configs_to_container("SoAdConfig", containers, soad_configs["SoAdConfig"])

    # Save ARXML contents to file
    ET.indent(tree, space="\t", level=0)
    tree.write(ar_file, encoding="utf-8", xml_declaration=True)
    lib.finalize_arxml_doc(ar_file)
    print("Info: SoAd Configs are saved to " + ar_file)    
