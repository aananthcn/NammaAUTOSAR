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


#EthIfGeneral
EthIfGeneralCfgType_str = "\n\ntypedef struct {\n\
        uint8   max_trcvs;\n\
        boolean dev_error_detect;\n\
        boolean en_rx_int;\n\
        boolean en_tx_int;\n\
        boolean version_info_api;\n\
        boolean version_info_api_macro;\n\
        uint8 lnk_st_ch_mn_reload;\n\
        uint16  mn_fn_period_ms;\n\
        uint16  rx_ind_itrtn;\n\
        boolean get_rst_meas_data_api;\n\
        boolean start_auto_neg;\n\
        boolean get_baud_rate;\n\
        boolean counter_state;\n\
        boolean gl_time_supp;\n\
        boolean wake_supp;\n\
        boolean trcv_wakemode_api;\n\
        uint16  swt_off_port_delay_ms;\n\
        uint16  port_startup_activ_ms;\n\
        uint16  mn_fn_state_period_ms;\n\
        boolean set_fwd_mode_api;\n\
        boolean verify_cfg_api;\n\
        boolean swt_mgmt_supp;\n\
        boolean get_ctrl_idx_lst;\n\
        boolean get_vlan_id_supp;\n\
        boolean en_weth_api;\n\
        boolean en_sig_qual_api;\n\
        uint16  sig_qual_chk_ms;\n\
        boolean en_sec_evt_report;\n\
        void *sec_evt_ref;\n\
} EthIfGeneralCfgType;\n\
\n"


# EthIfConfigSet
EthIf_FrameOwnerConfig_str = "\n\ntypedef struct {\n\
        uint16 frametype;\n\
        uint8 if_owner;\n\
} EthIf_FrameOwnerConfig;\n\
\n"


def define_ethif_frameowner_config(cf, fo_cfg):
    cf.write("\n\nconst EthIf_FrameOwnerConfig EthIfFrameOwnerCfg[ETHIF_MAX_FRAMEOWNER_CONFIGS] = {\n")
    for i, cfg in enumerate(fo_cfg):
        cf.write("\t{\n")
        cf.write("\t\t.frametype = "+cfg["EthIfFrameType"]+",\n")
        cf.write("\t\t.if_owner = "+cfg["EthIfOwner"]+"\n")
        cf.write("\t},\n")
    cf.write("};\n\n")


def define_ethif_rxi_config(cf, rxi_cfg):
    cf.write("\n\nconst ethif_fp_type EthIfRxIndicationConfig[ETHIF_MAX_RX_INDCATN_CONFIGS] = {\n")
    for i, cfg in enumerate(rxi_cfg):
        cf.write("\t"+str(cfg["EthIfRxIndicationFunction"])+",\n")
    cf.write("};\n\n")


def define_ethif_txc_config(cf, txc_cfg):
    cf.write("\n\nconst ethif_fp_type EthIfTxConfirmationConfig[ETHIF_MAX_TX_CONFIRM_CONFIGS] = {\n")
    for i, cfg in enumerate(txc_cfg):
        cf.write("\t"+str(cfg["EthIfTxConfirmationFunction"])+",\n")
    cf.write("};\n\n")


def define_ethif_lsc_config(cf, lsc_cfg):
    cf.write("\n\nconst ethif_fp_type EthIfTrcvLinkStateChgConfig[ETHIF_MAX_LNK_ST_CHG_CONFIGS] = {\n")
    for i, cfg in enumerate(lsc_cfg):
        cf.write("\t"+str(cfg["EthIfTrcvLinkStateChgFunction"])+",\n")
    cf.write("};\n\n")


EthIf_PhysController_str = "\n\ntypedef struct {\n\
        void *fifo_ref;\n\
        void *ecc_ref;\n\
        void *wecc_ref;\n\
        uint16 mn_fn_ms;\n\
        uint16 rx_ind_iter;\n\
        uint8 idx;\n\
} EthIf_PhysControllerConfig;\n\
\n"


def define_ethif_phys_ctrlr_config(cf, pc_cfg):
    cf.write("\n\nconst EthIf_PhysControllerConfig EthIfPhysControllerConfig[ETHIF_MAX_PHYS_CTRLR_CONFIGS] = {\n")
    for i, cfg in enumerate(pc_cfg):
        cf.write("\t{\n")
        cf.write("\t\t.idx = "+cfg["EthIfPhysControllerIdx"]+",\n")
        cf.write("\t\t.mn_fn_ms = "+str(int(1000*float(cfg["EthIfPhysCtrlRxMainFunctionPeriod"])))+",\n")
        cf.write("\t\t.rx_ind_iter = "+cfg["EthIfPhysCtrlRxIndicationIterations"]+",\n")

        if "..." in cfg["EthIfPhysCtrlRxIngressFifoRef"]:
            cf.write("\t\t.fifo_ref = NULL,\n")
        else:
            cf.write("\t\t.fifo_ref = "+cfg["EthIfPhysCtrlRxIngressFifoRef"]+",\n")

        if "..." in cfg["EthIfEthCtrlRef"]:
            cf.write("\t\t.ecc_ref = NULL,\n")
        else:
	        cf.write("\t\t.ecc_ref = "+cfg["EthIfEthCtrlRef"]+",\n")

        if "..." in cfg["EthIfWEthCtrlRef"]:
            cf.write("\t\t.wecc_ref = NULL,\n")
        else:
	        cf.write("\t\t.wecc_ref = "+cfg["EthIfWEthCtrlRef"]+",\n")

        cf.write("\t},\n")
    cf.write("};\n\n")


# Main configs for EthIf
EthIf_ConfigType_str = "\n\ntypedef struct {\n\
        const EthIfGeneralCfgType general;\n\
        const EthIf_FrameOwnerConfig *fo_cfg;\n\
        const ethif_fp_type *rxi_cfg;\n\
        const ethif_fp_type *txc_cfg;\n\
        const ethif_fp_type *lsc_cfg;\n\
} EthIf_ConfigType;\n\
\n"


EthIf_ConfigType_str_def = "\n\nconst EthIf_ConfigType EthIfConfigs = {\n\
        .general = EthIfGenConfigs,\n\
        .fo_cfg  = EthIfFrameOwnerCfg,\n\
        .rxi_cfg = EthIfRxIndicationConfig,\n\
        .txc_cfg = EthIfTxConfirmationConfig,\n\
        .lsc_cfg = EthIfTrcvLinkStateChgConfig,\n\
};\n\
\n"


def generate_ethif_general(cf, gen_cfg):
    cf.write("\n\nconst EthIfGeneralCfgType EthIfGenConfigs = {\n")
    cf.write("\t.max_trcvs = "+str(gen_cfg["EthIfMaxTrcvsTotal"])+",\n")
    cf.write("\t.dev_error_detect = "+str(gen_cfg["EthIfDevErrorDetect"])+",\n")
    cf.write("\t.en_rx_int = "+str(gen_cfg["EthIfEnableRxInterrupt"])+",\n")
    cf.write("\t.en_tx_int = "+str(gen_cfg["EthIfEnableTxInterrupt"])+",\n")
    cf.write("\t.version_info_api = "+str(gen_cfg["EthIfVersionInfoApi"])+",\n")
    cf.write("\t.version_info_api_macro = "+str(gen_cfg["EthIfVersionInfoApiMacro"])+",\n")
    cf.write("\t.lnk_st_ch_mn_reload = "+str(gen_cfg["EthIfTrcvLinkStateChgMainReload"])+",\n")
    cf.write("\t.mn_fn_period_ms = "+str(int(1000*float(gen_cfg["EthIfMainFunctionPeriod"])))+",\n")
    cf.write("\t.rx_ind_itrtn = "+str(gen_cfg["EthIfRxIndicationIterations"])+",\n")
    cf.write("\t.get_rst_meas_data_api = "+str(gen_cfg["EthIfGetAndResetMeasurementDataApi"])+",\n")
    cf.write("\t.start_auto_neg = "+str(gen_cfg["EthIfStartAutoNegotiation"])+",\n")
    cf.write("\t.get_baud_rate = "+str(gen_cfg["EthIfGetBaudRate"])+",\n")
    cf.write("\t.counter_state = "+str(gen_cfg["EthIfGetCounterState"])+",\n")
    cf.write("\t.gl_time_supp = "+str(gen_cfg["EthIfGlobalTimeSupport"])+",\n")
    cf.write("\t.wake_supp = "+str(gen_cfg["EthIfWakeUpSupport"])+",\n")
    cf.write("\t.trcv_wakemode_api = "+str(gen_cfg["EthIfGetAndResetMeasurementDataApi"])+",\n")
    cf.write("\t.swt_off_port_delay_ms = "+str(int(1000*float(gen_cfg["EthIfSwitchOffPortTimeDelay"])))+",\n")
    cf.write("\t.port_startup_activ_ms = "+str(int(1000*float(gen_cfg["EthIfPortStartupActiveTime"])))+",\n")
    cf.write("\t.mn_fn_state_period_ms = "+str(int(1000*float(gen_cfg["EthIfMainFunctionStatePeriod"])))+",\n")
    cf.write("\t.set_fwd_mode_api = "+str(gen_cfg["EthIfSetForwardingModeApi"])+",\n")
    cf.write("\t.verify_cfg_api = "+str(gen_cfg["EthIfVerifyConfigApi"])+",\n")
    cf.write("\t.swt_mgmt_supp = "+str(gen_cfg["EthIfSwitchManagementSupport"])+",\n")
    cf.write("\t.get_ctrl_idx_lst = "+str(gen_cfg["EthIfGetCtrlIdxList"])+",\n")
    cf.write("\t.get_vlan_id_supp = "+str(gen_cfg["EthIfGetVlanIdSupport"])+",\n")
    cf.write("\t.en_weth_api = "+str(gen_cfg["EthIfEnableWEthApi"])+",\n")
    cf.write("\t.en_sig_qual_api = "+str(gen_cfg["EthIfEnableSignalQualityApi"])+",\n")
    cf.write("\t.sig_qual_chk_ms = "+str(int(1000*float(gen_cfg["EthIfSignalQualityCheckPeriod"])))+",\n")
    cf.write("\t.en_sec_evt_report = "+str(gen_cfg["EthIfEnableSecurityEventReporting"])+",\n")
    if gen_cfg["EthIfSecurityEventRefs"] == "...":
        cf.write("\t.sec_evt_ref = NULL\n")
    else:
        cf.write("\t.sec_evt_ref = "+str(gen_cfg["EthIfSecurityEventRefs"])+"\n")
    cf.write("};\n")


def generate_sourcefile(ethif_src_path, ethif_configs):
    cf = open(ethif_src_path+"/cfg/EthIf_cfg.c", "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include <EthIf_cfg.h>\n\n\n")
    cf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")

    generate_ethif_general(cf, ethif_configs["EthIfGeneral"][0].datavar)
    define_ethif_frameowner_config(cf, ethif_configs["EthIfConfigSet"][0].datavar["EthIfFrameOwnerConfig"])
    define_ethif_rxi_config(cf, ethif_configs["EthIfConfigSet"][0].datavar["EthIfRxIndicationConfig"])
    define_ethif_txc_config(cf, ethif_configs["EthIfConfigSet"][0].datavar["EthIfTxConfirmationConfig"])
    define_ethif_lsc_config(cf, ethif_configs["EthIfConfigSet"][0].datavar["EthIfTrcvLinkStateChgConfig"])
    define_ethif_phys_ctrlr_config(cf, ethif_configs["EthIfConfigSet"][0].datavar["EthIfPhysController"])

    # print at last
    cf.write(EthIf_ConfigType_str_def)

    cf.close()



def generate_headerfile(ethif_src_path, ethif_configs):
    hf = open(ethif_src_path+"/cfg/EthIf_cfg.h", "w")
    hf.write("#ifndef NAMMA_AUTOSAR_ETHIF_CFG_H\n")
    hf.write("#define NAMMA_AUTOSAR_ETHIF_CFG_H\n\n")
    hf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")
    hf.write("#include <Platform_Types.h>\n\n")

    hf.write(EthIfGeneralCfgType_str)
    hf.write(EthIf_FrameOwnerConfig_str)
    hf.write(EthIf_PhysController_str)

    hf.write("\n\n")
    hf.write("#define ETHIF_MAX_FRAMEOWNER_CONFIGS   ("+str(len(ethif_configs["EthIfConfigSet"][0].datavar["EthIfFrameOwnerConfig"]))+")\n")
    hf.write("#define ETHIF_MAX_RX_INDCATN_CONFIGS   ("+str(len(ethif_configs["EthIfConfigSet"][0].datavar["EthIfRxIndicationConfig"]))+")\n")
    hf.write("#define ETHIF_MAX_TX_CONFIRM_CONFIGS   ("+str(len(ethif_configs["EthIfConfigSet"][0].datavar["EthIfTxConfirmationConfig"]))+")\n")
    hf.write("#define ETHIF_MAX_LNK_ST_CHG_CONFIGS   ("+str(len(ethif_configs["EthIfConfigSet"][0].datavar["EthIfTrcvLinkStateChgConfig"]))+")\n")
    hf.write("#define ETHIF_MAX_PHYS_CTRLR_CONFIGS   ("+str(len(ethif_configs["EthIfConfigSet"][0].datavar["EthIfPhysController"]))+")\n")
    
    hf.write("\n\ntypedef void (*ethif_fp_type)(void);")

    # print at last
    hf.write(EthIf_ConfigType_str)

    # External Declarations
    hf.write("\n\nextern const EthIf_ConfigType EthIfConfigs;\n")

    hf.write("\n\n#endif\n")
    hf.close()



def generate_code(gui, ethif_configs):
    cwd = os.getcwd()
    ethif_src_path = search.find_dir("EthIf", cwd+"/submodules/ECU-AL/")

    generate_headerfile(ethif_src_path, ethif_configs)
    generate_sourcefile(ethif_src_path, ethif_configs)
    uc_cgen.create_source(gui) # calling uc_cgen.create_source() is a work-around. This will be corrected later.
    
