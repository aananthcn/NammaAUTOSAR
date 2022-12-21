#
# Created on Tue Dec 20 2022 7:05:48 AM
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
import os

# import arxml.lin.arxml_lin as arxml_lin
import utils.search as search

# Temporary work-around
import gui.mcu.uc_cgen as uc_cgen


EthGeneralCfgType_str = "\n\ntypedef struct {\n\
    uint16  mainfn_period_ms;\n\
    uint8   index;\n\
    boolean dev_error_detect;\n\
    boolean get_cntr_val_api;\n\
    boolean get_rx_stats_api;\n\
    boolean get_tx_stats_api;\n\
    boolean get_tx_erctv_api; /* EthGetTxErrorCounterValuesApi */\n\
    boolean get_gbl_time_api;\n\
    uint8   max_ctrl_suportd;\n\
    boolean version_info_api;\n\
} EthGeneralCfgType;\n\
\n"

EthCtrlOffloadingType_str = "\ntypedef struct {\n\
    boolean en_cksum_ipv4;\n\
    boolean en_cksum_icmp;\n\
    boolean en_cksum_tcp;\n\
    boolean en_cksum_udp;\n\
} EthCtrlOffloadingType;\n\
\n"

EthCtrlMacLayerSpeed_str = "\ntypedef enum {\n\
    ETH_MAC_LAYER_SPEED_10M,\n\
    ETH_MAC_LAYER_SPEED_100M,\n\
    ETH_MAC_LAYER_SPEED_1G,\n\
    ETH_MAC_LAYER_SPEED_2500M,\n\
    ETH_MAC_LAYER_SPEED_10G\n\
} EthCtrlMacLayerSpeed;\n\
\n"

EthCtrlMacLayerType_str = "\ntypedef enum {\n\
    ETH_MAC_LAYER_TYPE_XMII,\n\
    ETH_MAC_LAYER_TYPE_XGMII,\n\
    ETH_MAC_LAYER_TYPE_XXGMII\n\
} EthCtrlMacLayerType;\n\
\n"

EthCtrlMacLayerSubType_str = "\ntypedef enum {\n\
    REDUCED,\n\
    REVERSED,\n\
    SERIAL,\n\
    STANDARD,\n\
    UNIVERSAL_SERIAL\n\
} EthCtrlMacLayerSubType;\n\
\n"

EthCtrlConfigType_str = "\ntypedef struct {\n\
    boolean                 buf_handlg;\n\
    boolean                 enable_mii;\n\
    boolean                 enable_spi;\n\
    boolean                 en_rx_intr;\n\
    boolean                 en_tx_intr;\n\
    uint8                   ctrl_index;\n\
    EthCtrlMacLayerSpeed    mac_lr_spd;\n\
    EthCtrlMacLayerType     mac_lr_typ;\n\
    EthCtrlMacLayerSubType  mac_sb_typ;\n\
    uint8                   mac_addres[6];\n\
} EthCtrlConfigType;\n\
\n"


Eth_ConfigFifoType_str = "\ntypedef struct {\n\
    const uint16    buff_len;\n\
    const uint16    buf_totl;\n\
    const uint16    fifo_idx;\n\
    const uint8     fifoprio;\n\
} Eth_ConfigFifoType;\n\
\n"


Eth_ConfigSchedulerType_str = "\ntypedef struct {\n\
    const uint32 predes_order;\n\
} Eth_ConfigSchedulerType;\n\
\n"


Eth_ConfigShaperType_str = "\ntypedef struct {\n\
    const uint32 idle_slope;\n\
    const uint32 max_credit;\n\
    const uint32 min_credit;\n\
} Eth_ConfigShaperType;\n\
\n"


Eth_ConfigSpiCfgType_str = "\ntypedef struct {\n\
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
    const uint8                 tx_crdthrsh; /* Credit Threshold */\n\
    const boolean               spi_syncacc; /* Accesss Synchronous */\n\
    const Spi_SequenceEnumType  spisequence;\n\
} Eth_ConfigSpiCfgType;\n\
\n"


Eth_ConfigType_str = "\ntypedef struct {\n\
    const EthGeneralCfgType         general;\n\
    const EthCtrlOffloadingType     offload;\n\
    const EthCtrlConfigType         ctrlcfg;\n\
    const Eth_ConfigFifoType        fifo_ig;\n\
    const Eth_ConfigFifoType        fifo_eg;\n\
    const Eth_ConfigSchedulerType   sched_c;\n\
    const Eth_ConfigShaperType      shape_c;\n\
    const Eth_ConfigSpiCfgType      spi_cfg;\n\
} Eth_ConfigType;\n\
\n\n"



def generate_sourcefile(eth_src_path, eth_configs):
    cf = open(eth_src_path+"/cfg/Eth_cfg.c", "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include <Eth_cfg.h>\n\n\n")
    cf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")

    cf.write("\n\nconst Eth_ConfigType EthConfigs[ETH_DRIVER_MAX_CHANNEL] = {\n")
    for i, cfg in enumerate(eth_configs):
        # print(cfg.datavar)
        cf.write("\t{\n")
        cf.write("\t\t/* Eth channel - "+str(i)+" */\n")
        cf.write("\t\t.general = {\n")
        cf.write("\t\t\t.index = "+ cfg.datavar["EthGeneral"]["EthIndex"] +",\n")
        period_ms = int(float(cfg.datavar["EthGeneral"]["EthMainFunctionPeriod"])*1000)
        cf.write("\t\t\t.mainfn_period_ms = "+ str(period_ms) +",\n")
        cf.write("\t\t\t.dev_error_detect = "+ cfg.datavar["EthGeneral"]["EthDevErrorDetect"] +",\n")
        cf.write("\t\t\t.get_cntr_val_api = "+ cfg.datavar["EthGeneral"]["EthGetCounterValuesApi"] +",\n")
        cf.write("\t\t\t.get_rx_stats_api = "+ cfg.datavar["EthGeneral"]["EthGetRxStatsApi"] +",\n")
        cf.write("\t\t\t.get_tx_stats_api = "+ cfg.datavar["EthGeneral"]["EthGetTxStatsApi"] +",\n")
        cf.write("\t\t\t.get_tx_erctv_api = "+ cfg.datavar["EthGeneral"]["EthGetTxErrorCounterValuesApi"] +",\n")
        cf.write("\t\t\t.get_gbl_time_api = "+ cfg.datavar["EthGeneral"]["EthGlobalTimeSupport"] +",\n")
        cf.write("\t\t\t.max_ctrl_suportd = "+ cfg.datavar["EthGeneral"]["EthMaxCtrlsSupported"] +",\n")
        cf.write("\t\t\t.version_info_api = "+ cfg.datavar["EthGeneral"]["EthVersionInfoApi"] +"\n")
        cf.write("\t\t},\n")
        cf.write("\t\t.offload = {\n")
        cf.write("\t\t\t.en_cksum_ipv4 = "+ cfg.datavar["EthCtrlOffloading"]["EthCtrlEnableOffloadChecksumIPv4"] +",\n")
        cf.write("\t\t\t.en_cksum_icmp = "+ cfg.datavar["EthCtrlOffloading"]["EthCtrlEnableOffloadChecksumICMP"] +",\n")
        cf.write("\t\t\t.en_cksum_tcp = "+ cfg.datavar["EthCtrlOffloading"]["EthCtrlEnableOffloadChecksumTCP"] +",\n")
        cf.write("\t\t\t.en_cksum_udp = "+ cfg.datavar["EthCtrlOffloading"]["EthCtrlEnableOffloadChecksumUDP"] +"\n")
        cf.write("\t\t}\n")
        cf.write("\t},\n")
    cf.write("};\n")

    cf.close()



def generate_headerfile(eth_src_path, eth_configs):
    hf = open(eth_src_path+"/cfg/Eth_cfg.h", "w")
    hf.write("#ifndef NAMMA_AUTOSAR_ETH_CFG_H\n")
    hf.write("#define NAMMA_AUTOSAR_ETH_CFG_H\n\n")
    hf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")
    hf.write("#include <Platform_Types.h>\n\n")
    hf.write("#include <Spi_cfg.h>\n\n")

    hf.write(EthGeneralCfgType_str)
    hf.write(EthCtrlOffloadingType_str)

    hf.write(EthCtrlMacLayerSpeed_str)
    hf.write(EthCtrlMacLayerType_str)
    hf.write(EthCtrlMacLayerSubType_str)
    hf.write(EthCtrlConfigType_str)
    
    hf.write(Eth_ConfigFifoType_str)
    hf.write(Eth_ConfigSchedulerType_str)
    hf.write(Eth_ConfigShaperType_str)
    hf.write(Eth_ConfigSpiCfgType_str)

    hf.write(Eth_ConfigType_str)

    # Macros
    hf.write("#define ETH_DRIVER_MAX_CHANNEL    ("+str(len(eth_configs))+")\n")
    
    # External Declarations
    hf.write("\n\nextern const Eth_ConfigType EthConfigs[ETH_DRIVER_MAX_CHANNEL];\n")

    hf.write("\n\n#endif\n")
    hf.close()



def generate_code(gui, eth_configs):
    cwd = os.getcwd()
    eth_src_path = search.find_dir("Eth", cwd+"/submodules/MCAL/")
    generate_headerfile(eth_src_path, eth_configs)
    generate_sourcefile(eth_src_path, eth_configs)
    uc_cgen.create_source(gui) # calling uc_cgen.create_source() is a work-around. This will be corrected later.
    
