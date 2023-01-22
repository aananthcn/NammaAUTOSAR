#
# Created on Sun Jan 22 2023 9:59:17 AM
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
import os

# import arxml.lin.arxml_lin as arxml_lin
import utils.search as search

# import gui.ethif.ethif_ctrlcfg as ethif_cc

# Temporary work-around
import gui.mcu.uc_cgen as uc_cgen


EthIfGeneralCfgType_str = "\n\ntypedef struct {\n\
    uint16  swt_off_port_time_delay;\n\
    uint16  port_startup_activ_time;\n\
    uint8   index;\n\
    boolean dev_error_detect;\n\
    boolean get_cntr_val_api;\n\
    boolean get_rx_stats_api;\n\
    boolean get_tx_stats_api;\n\
    boolean get_tx_erctv_api; /* EthIfGetTxErrorCounterValuesApi */\n\
    boolean get_gbl_time_api;\n\
    uint8   max_ctrl_suportd;\n\
    boolean version_info_api;\n\
} EthIfGeneralCfgType;\n\
\n"

EthIfCtrlOffloadingType_str = "\ntypedef struct {\n\
    boolean en_cksum_ipv4;\n\
    boolean en_cksum_icmp;\n\
    boolean en_cksum_tcp;\n\
    boolean en_cksum_udp;\n\
} EthIfCtrlOffloadingType;\n\
\n"

EthIfCtrlMacLayerSpeed_str = "\ntypedef enum {\n\
    ETH_MAC_LAYER_SPEED_10M,\n\
    ETH_MAC_LAYER_SPEED_100M,\n\
    ETH_MAC_LAYER_SPEED_1G,\n\
    ETH_MAC_LAYER_SPEED_2500M,\n\
    ETH_MAC_LAYER_SPEED_10G\n\
} EthIfCtrlMacLayerSpeed;\n\
\n"

EthIfCtrlMacLayerType_str = "\ntypedef enum {\n\
    ETH_MAC_LAYER_TYPE_XMII,\n\
    ETH_MAC_LAYER_TYPE_XGMII,\n\
    ETH_MAC_LAYER_TYPE_XXGMII\n\
} EthIfCtrlMacLayerType;\n\
\n"

EthIfCtrlMacLayerSubType_str = "\ntypedef enum {\n\
    REDUCED,\n\
    REVERSED,\n\
    SERIAL,\n\
    STANDARD,\n\
    UNIVERSAL_SERIAL\n\
} EthIfCtrlMacLayerSubType;\n\
\n"


def generate_ethif_ctrl_dev_type_enum(hf):
    dev_list = list(ethif_cc.get_supported_spi_ethif_devs())
    hf.write("\ntypedef enum {\n")
    for dev in dev_list:
        hf.write("\tETH_DEV_"+str(dev).upper()+",\n")
    hf.write("\tMAX_ETH_DEV\n")
    hf.write("} EthIfControllerDevType;\n\n")

EthIfCtrlConfigType_str = "\ntypedef struct {\n\
    boolean                 buf_handlg;\n\
    boolean                 enable_mii;\n\
    boolean                 enable_spi;\n\
    boolean                 en_rx_intr;\n\
    boolean                 en_tx_intr;\n\
    uint8                   ctrl_index;\n\
    EthIfCtrlMacLayerSpeed    mac_lr_spd;\n\
    EthIfCtrlMacLayerType     mac_lr_typ;\n\
    EthIfCtrlMacLayerSubType  mac_sb_typ;\n\
    uint8                   mac_addres[6];\n\
    EthIfControllerDevType    spi_device;\n\
} EthIfCtrlConfigType;\n\
\n"


EthIf_ConfigFifoType_str = "\ntypedef struct {\n\
    const uint16    buff_len;\n\
    const uint16    buf_totl;\n\
    const uint16    fifo_idx;\n\
    const uint8     fifoprio;\n\
} EthIf_ConfigFifoType;\n\
\n"


EthIf_ConfigSchedulerType_str = "\ntypedef struct {\n\
    const uint32 predes_order;\n\
} EthIf_ConfigSchedulerType;\n\
\n"


EthIf_ConfigShaperType_str = "\ntypedef struct {\n\
    const uint32 idle_slope;\n\
    const uint32 max_credit;\n\
    const uint32 min_credit;\n\
} EthIf_ConfigShaperType;\n\
\n"


EthIf_ConfigSpiCfgType_str = "\ntypedef struct {\n\
    const uint8                 pay_ld_size;\n\
    const uint8                 com_retries;\n\
    const uint32                ctimeout_ms; /* Comm. Timeout */\n\
    const boolean               ctrldatprot;\n\
    const boolean               rx_cs_align;\n\
    const boolean               rx_cut_thru;\n\
    const boolean               rx_zero_aln;\n\
    const boolean               txd_hdr_seq;\n\
    const boolean               tx_en_cksum;\n\
    const boolean               tx_cut_thru;\n\
    const boolean               spi_timstmp;\n\
    const uint8                 tx_crdthrsh; /* Credit Threshold */\n\
    const boolean               spi_syncacc; /* Accesss Synchronous */\n\
    const Spi_SequenceEnumType  spisequence;\n\
} EthIf_ConfigSpiCfgType;\n\
\n"


EthIf_ConfigType_str = "\ntypedef struct {\n\
    const EthIfGeneralCfgType         general;\n\
    const EthIfCtrlOffloadingType     offload;\n\
    const EthIfCtrlConfigType         ctrlcfg;\n\
    const EthIf_ConfigFifoType        fifo_ig;\n\
    const EthIf_ConfigFifoType        fifo_eg;\n\
    const EthIf_ConfigSchedulerType   sched_c;\n\
    const EthIf_ConfigShaperType      shape_c;\n\
    const EthIf_ConfigSpiCfgType      spi_cfg;\n\
} EthIf_ConfigType;\n\
\n\n"



def print_mac_address_as_hex_bytes(cf, cfg):
    cf.write("\t\t\t.mac_addres = {")
    mac_addr_octets = cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlPhyAddress"].split(":")
    for i, octet in enumerate(mac_addr_octets):
        cf.write("0x"+octet)
        if i < 5:
            cf.write(", ")
    cf.write("},\n")


def generate_sourcefile(ethif_src_path, ethif_configs):
    cf = open(ethif_src_path+"/cfg/EthIf_cfg.c", "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include <EthIf_cfg.h>\n\n\n")
    cf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")

    cf.write("\n\nconst EthIf_ConfigType EthIfConfigs[ETH_DRIVER_MAX_CHANNEL] = {\n")
    for i, cfg in enumerate(ethif_configs):
        # print(cfg.datavar)
        cf.write("\t{\n")
        cf.write("\t\t/* EthIf channel - "+str(i)+" */\n")
        cf.write("\t\t.general = {\n")
        cf.write("\t\t\t.index = "+ cfg.datavar["EthIfGeneral"]["EthIfIndex"] +",\n")
        period_ms = int(float(cfg.datavar["EthIfGeneral"]["EthIfMainFunctionPeriod"])*1000)
        cf.write("\t\t\t.mainfn_period_ms = "+ str(period_ms) +",\n")
        cf.write("\t\t\t.dev_error_detect = "+ cfg.datavar["EthIfGeneral"]["EthIfDevErrorDetect"] +",\n")
        cf.write("\t\t\t.get_cntr_val_api = "+ cfg.datavar["EthIfGeneral"]["EthIfGetCounterValuesApi"] +",\n")
        cf.write("\t\t\t.get_rx_stats_api = "+ cfg.datavar["EthIfGeneral"]["EthIfGetRxStatsApi"] +",\n")
        cf.write("\t\t\t.get_tx_stats_api = "+ cfg.datavar["EthIfGeneral"]["EthIfGetTxStatsApi"] +",\n")
        cf.write("\t\t\t.get_tx_erctv_api = "+ cfg.datavar["EthIfGeneral"]["EthIfGetTxErrorCounterValuesApi"] +",\n")
        cf.write("\t\t\t.get_gbl_time_api = "+ cfg.datavar["EthIfGeneral"]["EthIfGlobalTimeSupport"] +",\n")
        cf.write("\t\t\t.max_ctrl_suportd = "+ cfg.datavar["EthIfGeneral"]["EthIfMaxCtrlsSupported"] +",\n")
        cf.write("\t\t\t.version_info_api = "+ cfg.datavar["EthIfGeneral"]["EthIfVersionInfoApi"] +"\n")
        cf.write("\t\t},\n")
        cf.write("\t\t.offload = {\n")
        cf.write("\t\t\t.en_cksum_ipv4 = "+ cfg.datavar["EthIfCtrlOffloading"]["EthIfCtrlEnableOffloadChecksumIPv4"] +",\n")
        cf.write("\t\t\t.en_cksum_icmp = "+ cfg.datavar["EthIfCtrlOffloading"]["EthIfCtrlEnableOffloadChecksumICMP"] +",\n")
        cf.write("\t\t\t.en_cksum_tcp = "+ cfg.datavar["EthIfCtrlOffloading"]["EthIfCtrlEnableOffloadChecksumTCP"] +",\n")
        cf.write("\t\t\t.en_cksum_udp = "+ cfg.datavar["EthIfCtrlOffloading"]["EthIfCtrlEnableOffloadChecksumUDP"] +"\n")
        cf.write("\t\t},\n")
        cf.write("\t\t.ctrlcfg = {\n")
        cf.write("\t\t\t.buf_handlg = "+ cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlConfigSwBufferHandling"] +",\n")
        cf.write("\t\t\t.enable_mii = "+ cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlEnableMii"] +",\n")
        cf.write("\t\t\t.enable_spi = "+ cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlEnableSpiInterface"] +",\n")
        cf.write("\t\t\t.spi_device = ETH_DEV_"+ cfg.datavar["EthIfCtrlConfig"]["EthIfSpiCtrlDevice"] +",\n")
        cf.write("\t\t\t.en_rx_intr = "+ cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlEnableRxInterrupt"] +",\n")
        cf.write("\t\t\t.en_tx_intr = "+ cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlEnableTxInterrupt"] +",\n")
        cf.write("\t\t\t.ctrl_index = "+ cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlIdx"] +",\n")
        cf.write("\t\t\t.mac_lr_spd = "+ cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlMacLayerSpeed"] +",\n")
        cf.write("\t\t\t.mac_lr_typ = "+ cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlMacLayerType"] +",\n")
        cf.write("\t\t\t.mac_sb_typ = "+ cfg.datavar["EthIfCtrlConfig"]["EthIfCtrlMacLayerSubType"] +",\n")
        print_mac_address_as_hex_bytes(cf, cfg)
        cf.write("\t\t},\n")
        cf.write("\t\t.fifo_ig = {\n")
        cf.write("\t\t\t.buff_len = "+ cfg.datavar["EthIfCtrlConfigXgressFifo"]["EthIfCtrlConfigIngressFifoBufLenByte"] +",\n")
        cf.write("\t\t\t.buf_totl = "+ cfg.datavar["EthIfCtrlConfigXgressFifo"]["EthIfCtrlConfigIngressFifoBufTotal"] +",\n")
        cf.write("\t\t\t.fifo_idx = "+ cfg.datavar["EthIfCtrlConfigXgressFifo"]["EthIfCtrlConfigIngressFifoIdx"] +",\n")
        cf.write("\t\t\t.fifoprio = "+ cfg.datavar["EthIfCtrlConfigXgressFifo"]["EthIfCtrlConfigIngressFifoPriorityAssignment"] +"\n")
        cf.write("\t\t},\n")
        cf.write("\t\t.fifo_eg = {\n")
        cf.write("\t\t\t.buff_len = "+ cfg.datavar["EthIfCtrlConfigXgressFifo"]["EthIfCtrlConfigEgressFifoBufLenByte"] +",\n")
        cf.write("\t\t\t.buf_totl = "+ cfg.datavar["EthIfCtrlConfigXgressFifo"]["EthIfCtrlConfigEgressFifoBufTotal"] +",\n")
        cf.write("\t\t\t.fifo_idx = "+ cfg.datavar["EthIfCtrlConfigXgressFifo"]["EthIfCtrlConfigEgressFifoIdx"] +",\n")
        cf.write("\t\t\t.fifoprio = "+ cfg.datavar["EthIfCtrlConfigXgressFifo"]["EthIfCtrlConfigEgressFifoPriorityAssignment"] +"\n")
        cf.write("\t\t},\n")
        cf.write("\t\t.sched_c = {\n")
        cf.write("\t\t\t.predes_order = "+ cfg.datavar["EthIfCtrlConfigScheduler"]["EthIfCtrlConfigSchedulerPredecessorOrder"] +"\n")
        cf.write("\t\t},\n")
        cf.write("\t\t.shape_c = {\n")
        cf.write("\t\t\t.idle_slope = "+ cfg.datavar["EthIfCtrlConfigShaper"]["EthIfCtrlConfigShaperIdleSlope"] +",\n")
        cf.write("\t\t\t.max_credit = "+ cfg.datavar["EthIfCtrlConfigShaper"]["EthIfCtrlConfigShaperMaxCredit"] +",\n")
        cf.write("\t\t\t.min_credit = "+ cfg.datavar["EthIfCtrlConfigShaper"]["EthIfCtrlConfigShaperMinCredit"] +"\n")
        cf.write("\t\t},\n")
        cf.write("\t\t.spi_cfg = {\n")
        cf.write("\t\t\t.pay_ld_size = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiChunkPayloadSize"] +",\n")
        cf.write("\t\t\t.com_retries = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiCommRetries"] +",\n")
        com_timout_ms = int(float(cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiCommTimeout"])*1000)
        cf.write("\t\t\t.ctimeout_ms = "+ str(com_timout_ms) +",\n")
        cf.write("\t\t\t.ctrldatprot = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiEnableControlDataProtection"] +",\n")
        cf.write("\t\t\t.rx_cs_align = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiEnableRxCSAlign"] +",\n")
        cf.write("\t\t\t.rx_cut_thru = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiEnableRxCutThrough"] +",\n")
        cf.write("\t\t\t.rx_zero_aln = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiEnableRxZeroAlign"] +",\n")
        cf.write("\t\t\t.txd_hdr_seq = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiEnableTransmitDataHdrSequence"] +",\n")
        cf.write("\t\t\t.tx_en_cksum = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiEnableTxChecksum"] +",\n")
        cf.write("\t\t\t.tx_cut_thru = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiEnableTxCutThrough"] +",\n")
        cf.write("\t\t\t.spi_timstmp = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiSelectTimeStamp"] +",\n")
        cf.write("\t\t\t.tx_crdthrsh = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiTransmitCreditThreshold"] +",\n")
        cf.write("\t\t\t.spi_syncacc = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiAccessSynchronous"] +",\n")
        cf.write("\t\t\t.spisequence = "+ cfg.datavar["EthIfCtrlConfigSpiConfiguration"]["EthIfCtrlConfigSpiSequenceName"] +"\n")
        cf.write("\t\t}\n")
        cf.write("\t},\n")
    cf.write("};\n")

    cf.close()



def generate_headerfile(ethif_src_path, ethif_configs):
    hf = open(ethif_src_path+"/cfg/EthIf_cfg.h", "w")
    hf.write("#ifndef NAMMA_AUTOSAR_ETHIF_CFG_H\n")
    hf.write("#define NAMMA_AUTOSAR_ETHIF_CFG_H\n\n")
    hf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")
    hf.write("#include <Platform_Types.h>\n\n")
    # hf.write("#include <Spi_cfg.h>\n\n")

    # hf.write(EthIfGeneralCfgType_str)
    # hf.write(EthIfCtrlOffloadingType_str)

    # hf.write(EthIfCtrlMacLayerSpeed_str)
    # hf.write(EthIfCtrlMacLayerType_str)
    # hf.write(EthIfCtrlMacLayerSubType_str)

    # generate_ethif_ctrl_dev_type_enum(hf)
    # hf.write(EthIfCtrlConfigType_str)
    
    # hf.write(EthIf_ConfigFifoType_str)
    # hf.write(EthIf_ConfigSchedulerType_str)
    # hf.write(EthIf_ConfigShaperType_str)
    # hf.write(EthIf_ConfigSpiCfgType_str)

    # hf.write(EthIf_ConfigType_str)

    # # Macros
    # hf.write("#define ETH_DRIVER_MAX_CHANNEL    ("+str(len(ethif_configs))+")\n")
    
    # External Declarations
    hf.write("\n\nextern const EthIf_ConfigType EthIfConfigs;\n")

    hf.write("\n\n#endif\n")
    hf.close()



def generate_code(gui, ethif_configs):
    cwd = os.getcwd()
    ethif_src_path = search.find_dir("EthIf", cwd+"/submodules/ECU-AL/")

    generate_headerfile(ethif_src_path, ethif_configs)
    # generate_sourcefile(ethif_src_path, ethif_configs)
    # generate_macphy_files(ethif_src_path, ethif_configs)
    # uc_cgen.create_source(gui) # calling uc_cgen.create_source() is a work-around. This will be corrected later.
    
