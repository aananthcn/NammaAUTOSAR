#
# Created on Tue Oct 25 2022 10:23:58 PM
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

# import arxml.spi.arxml_spi as arxml_spi
import utils.search as search

# Temporary work-around
import gui.mcu.uc_cgen as uc_cgen


SpiGeneralCfgType_str = "\n\ntypedef struct {\n\
    uint8 spi_level_delivered;\n\
    uint8 spi_chan_buff_allowed;\n\
    boolean spi_intr_seq_allowed;\n\
    boolean spi_hw_status_api;\n\
    boolean spi_cancel_api;\n\
    boolean spi_version_info_api;\n\
    boolean spi_dev_error_detect;\n\
    boolean spi_supp_conc_sync_tx;\n\
    uint32 spi_main_func_period_ms;\n\
} SpiGeneralCfgType;\n\
\n"


def define_ext_dev_enum_type(hf, ext_devs):
    hf.write("\ntypedef enum {\n")
    for dev in ext_devs:
        hf.write("\tSPI_EXT_DEV_"+dev.datavar['SpiHwUnit']+",\n")
    hf.write("\tSPI_EXT_DEV_MAX\n")
    hf.write("} SpiExtDevID_Type;\n\n")


SpiDataShiftEdge_str = "\ntypedef enum {\n\
    SPI_EDGE_LEADING,\n\
    SPI_EDGE_TRAILING\n\
} SpiDataShiftEdgeType;\n\
\n"

SpiLevel_str = "\ntypedef enum {\n\
    SPI_LEVEL_LOW,\n\
    SPI_LEVEL_HIGH\n\
} SpiLevelType;\n\
\n"

SpiCsSelection_str = "\ntypedef enum {\n\
    CS_VIA_PERIPHERAL_ENGINE,\n\
    CS_VIA_GPIO\n\
} SpiCsSelectionType;\n\
\n"

SpiTransferStart_str = "\ntypedef enum {\n\
    SPI_TX_START_MSB,\n\
    SPI_TX_START_LSB\n\
} SpiTransferStartType;\n\
\n"

SpiFrameFormat_str = "\ntypedef enum {\n\
    MOTOROLA_SPI,\n\
    TI_SSI,\n\
    NS_MICROWIRE\n\
} SpiFrameFormatType;\n\
\n"

SpiExternalDevice_str = "\ntypedef struct {\n\
    SpiExtDevID_Type spi_hw_unit_id;\n\
    uint32 spi_baudrate;\n\
    SpiDataShiftEdgeType spi_data_shift_edge;\n\
    SpiLevelType spi_shftclk_idle_level;\n\
    boolean spi_enable_cs;\n\
    char spi_cs_id[128];\n\
    SpiCsSelectionType spi_cs_selection;\n\
    sint16 spi_cs_dio;\n\
    SpiLevelType spi_cs_polarity;\n\
    uint32 spi_usec_clk_2_cs;\n\
    uint32 spi_usec_cs_2_clk;\n\
    uint32 spi_usec_cs_2_cs;\n\
    uint8 spi_databits;\n\
    SpiTransferStartType spi_tfr_type;\n\
    SpiFrameFormatType spi_frame_fmt;\n\
} SpiExternalDeviceType;\n\
\n"


SpiChannel_str = "\ntypedef struct {\n\
    uint16 spi_chan_id;\n\
    uint8 spi_chan_type;\n\
    uint16 spi_data_width; /* width in bits */\n\
    const uint8* spi_default_data;\n\
    uint16 spi_default_data_len;\n\
    uint16 spi_ib_num_buf;\n\
    uint32 spi_ib_buf_len;   /* length of int. src & dst buffers */\n\
    uint8* spi_ib_buf_s_ptr; /* int. src buffer (Tx buffer) ptr */\n\
    uint8* spi_ib_buf_d_ptr; /* int. dst buffer (Rx buffer) ptr */\n\
    uint16 spi_eb_max_len;\n\
    uint16* spi_eb_buf_l_ptr; /* length of ext. src & dst buffers */\n\
    uint8** spi_eb_buf_s_ptr; /* ext. src buffer (Tx buffer) ptr */\n\
    uint8** spi_eb_buf_d_ptr; /* ext. dst buffer (Rx buffer) ptr */\n\
    SpiTransferStartType spi_tx_start;\n\
} SpiChannelCfgType;\n\
\n"

SpiJob_str = "\ntypedef struct {\n\
    uint16 spi_job_id;\n\
    uint16 spi_job_priority;\n\
    void (*job_end_notification_fn)(void);\n\
    SpiExtDevID_Type spi_dev_assignment;\n\
    uint16 spi_chan_list_size;\n\
    const uint16* spi_chan_list;\n\
} SpiJobCfgType;\n\
\n"


SpiSequence_str = "\ntypedef struct {\n\
    uint16 spi_seq_id;\n\
    boolean spi_seq_interruptible;\n\
    void (*seq_end_notification_fn)(void);\n\
    uint16 spi_job_list_size;\n\
    const uint16* spi_job_list;\n\
} SpiSequenceCfgType;\n\
\n\n"


Spi_ConfigType_str = "\ntypedef struct {\n\
    const SpiGeneralCfgType general;\n\
    const SpiExternalDeviceType* devices[SPI_DRIVER_MAX_HW_UNIT];\n\
    const SpiChannelCfgType* channels[SPI_DRIVER_MAX_CHANNEL];\n\
    const SpiJobCfgType* jobs[SPI_DRIVER_MAX_JOB];\n\
    const SpiSequenceCfgType* sequences[SPI_DRIVER_MAX_SEQUENCE];\n\
} Spi_ConfigType;\n\
"



def define_custom_spi_seq_enums(hf, spi_seqs):
    hf.write("\n\n/* NammaAUTOSAR's custom enum, which will make code more readable */\n")
    hf.write("typedef enum {\n")
    for seq in spi_seqs:
        hf.write("\t"+str(seq.datavar["SpiSequenceName"]).upper()+",\n")
    hf.write("\tSEQ_ENUM_MAX\n")
    hf.write("} Spi_SequenceEnumType;\n")


def generate_headerfile(spi_src_path, spi_info):
    hf = open(spi_src_path+"/cfg/Spi_cfg.h", "w")
    hf.write("#ifndef NAMMA_AUTOSAR_SPI_CFG_H\n")
    hf.write("#define NAMMA_AUTOSAR_SPI_CFG_H\n\n")
    hf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")
    hf.write("#include <Platform_Types.h>\n\n")

    hf.write("\n#define SPI_CHAN_TYPE_IB        1")
    hf.write("\n#define SPI_CHAN_TYPE_EB        2")
    hf.write("\n#define SPI_CHAN_TYPE_IB_EB     3\n")
    
    hf.write(SpiGeneralCfgType_str)
    define_ext_dev_enum_type(hf, spi_info["SpiExternalDevice"])
    hf.write(SpiDataShiftEdge_str)
    hf.write(SpiLevel_str)
    hf.write(SpiCsSelection_str)
    hf.write(SpiTransferStart_str)
    hf.write(SpiFrameFormat_str)
    hf.write(SpiExternalDevice_str)
    hf.write(SpiChannel_str)
    hf.write(SpiJob_str)
    hf.write(SpiSequence_str)
    
    hf.write("\n#define SPI_DRIVER_MAX_CHANNEL   ("+str(spi_info["SpiDriver"][0].datavar["SpiMaxChannel"])+")\n")
    hf.write("#define SPI_DRIVER_MAX_JOB       ("+str(spi_info["SpiDriver"][0].datavar["SpiMaxJob"])+")\n")
    hf.write("#define SPI_DRIVER_MAX_SEQUENCE  ("+str(spi_info["SpiDriver"][0].datavar["SpiMaxSequence"])+")\n")
    hf.write("#define SPI_DRIVER_MAX_HW_UNIT   ("+str(spi_info["SpiDriver"][0].datavar["SpiMaxHwUnit"])+")\n")
    hf.write(Spi_ConfigType_str)
    
    # define custom enum definition for SPI Sequences
    define_custom_spi_seq_enums(hf, spi_info["SpiSequence"])

    # External Declarations
    hf.write("\n\nextern const SpiGeneralCfgType SpiGeneralCfg;\n")
    hf.write("extern const SpiExternalDeviceType SpiExternalDeviceCfg[SPI_DRIVER_MAX_HW_UNIT];\n")
    hf.write("extern const SpiChannelCfgType SpiChannelCfg[SPI_DRIVER_MAX_CHANNEL];\n")
    hf.write("extern const SpiJobCfgType SpiJobCfg[SPI_DRIVER_MAX_JOB];\n")
    hf.write("extern const SpiSequenceCfgType SpiSequenceCfg[SPI_DRIVER_MAX_SEQUENCE];\n")
    hf.write("extern const Spi_ConfigType SpiConfigs;\n")
    
    hf.write("\n\n#endif\n")
    hf.close()



def get_chan_type(spi_chan_str):
    spi_chan_type = ""
    if "IB" in spi_chan_str and "EB" in spi_chan_str:
        spi_chan_type = "SPI_CHAN_TYPE_IB_EB"
    elif "IB" in spi_chan_str:
        spi_chan_type = "SPI_CHAN_TYPE_IB"
    elif "EB" in spi_chan_str:
        spi_chan_type = "SPI_CHAN_TYPE_EB"
    else:
        spi_chan_type = "ERROR_CHAN_TYPE"
    return spi_chan_type



def gen_spi_general_configs(cf, gen_cfg):
    cf.write("\nconst SpiGeneralCfgType SpiGeneralCfg = {\n")
    cf.write("\t.spi_level_delivered     = "+str(gen_cfg["SpiLevelDelivered"])+",\n")

    cf.write("\t.spi_chan_buff_allowed   = "+get_chan_type(gen_cfg["SpiChannelBuffersAllowed"])+",\n")
    cf.write("\t.spi_intr_seq_allowed    = "+str(gen_cfg["SpiInterruptibleSeqAllowed"])+",\n")
    cf.write("\t.spi_hw_status_api       = "+str(gen_cfg["SpiHwStatusApi"])+",\n")
    cf.write("\t.spi_cancel_api          = "+str(gen_cfg["SpiCancelApi"])+",\n")
    cf.write("\t.spi_version_info_api    = "+str(gen_cfg["SpiVersionInfoApi"])+",\n")
    cf.write("\t.spi_dev_error_detect    = "+str(gen_cfg["SpiDevErrorDetect"])+",\n")
    cf.write("\t.spi_supp_conc_sync_tx   = "+str(gen_cfg["SpiSupportConcurrentSyncTransmit"])+",\n")
    cf.write("\t.spi_main_func_period_ms = "+str(int(1000*float(gen_cfg["SpiMainFunctionPeriod"])))+"\n")
    cf.write("};\n\n")



def databits_tfrtype_for_spi_device(dev, spi_info):
    databits = 32
    tfrstart = "SPI_TX_START_LSB"
    job_cfg = spi_info["SpiJob"]
    chn_cfg = spi_info["SpiChannel"]
    for job in job_cfg:
        if dev.datavar["SpiHwUnit"] != job.datavar["SpiDeviceAssignment"]:
            continue
        ch_list = job.datavar["SpiChannelList"]
        for ch in ch_list:
            ch_idx = ch["SpiChannelIndex"]
            if int(chn_cfg[int(ch_idx)].datavar["SpiDataWidth"]) < databits:
                databits = int(chn_cfg[int(ch_idx)].datavar["SpiDataWidth"])
            if chn_cfg[int(ch_idx)].datavar["SpiTransferStart"] != tfrstart:
                tfrstart = "SPI_TX_START_MSB"
    return databits, tfrstart



def gen_spi_device_configs(cf, spi_info):
    dev_cfg = spi_info["SpiExternalDevice"]
    cf.write("\nconst SpiExternalDeviceType SpiExternalDeviceCfg[] = {\n")
    for i, dev in enumerate(dev_cfg):
        # start of device
        cf.write("\t{\n")

        cf.write("\t\t.spi_hw_unit_id = SPI_EXT_DEV_"+dev.datavar['SpiHwUnit']+",\n")
        cf.write("\t\t.spi_baudrate = "+str(int(float(dev.datavar['SpiBaudrate'])))+", /* bps or Hz */\n")
        cf.write("\t\t.spi_data_shift_edge = SPI_EDGE_"+dev.datavar['SpiDataShiftEdge']+",\n")
        cf.write("\t\t.spi_shftclk_idle_level = SPI_LEVEL_"+dev.datavar['SpiShiftClockIdleLevel']+",\n")
        cf.write("\t\t.spi_enable_cs = "+dev.datavar['SpiEnableCs']+",\n")
        cf.write("\t\t.spi_cs_id = \""+dev.datavar['SpiCsIdentifier']+"\",\n")
        cf.write("\t\t.spi_cs_selection = "+dev.datavar['SpiCsSelection']+",\n")
        if "GPIO" in dev.datavar['SpiCsSelection']:
	        cf.write("\t\t.spi_cs_dio = "+dev.datavar['DIO']+",\n")
        else:
	        cf.write("\t\t.spi_cs_dio = -1,\n")
        cf.write("\t\t.spi_cs_polarity = SPI_LEVEL_"+dev.datavar['SpiCsPolarity']+",\n")
        cf.write("\t\t.spi_usec_clk_2_cs = "+str(int(1000000.0*float(dev.datavar['SpiTimeClk2Cs'])))+",\n")
        cf.write("\t\t.spi_usec_cs_2_clk = "+str(int(1000000.0*float(dev.datavar['SpiTimeCs2Clk'])))+",\n")
        cf.write("\t\t.spi_usec_cs_2_cs = "+str(int(1000000.0*float(dev.datavar['SpiTimeCs2Cs'])))+",\n")
        databits, tfrstart = databits_tfrtype_for_spi_device(dev, spi_info)
        cf.write("\t\t.spi_databits = "+str(databits)+",\n")
        cf.write("\t\t.spi_tfr_type = "+tfrstart+",\n")
        cf.write("\t\t.spi_frame_fmt = "+dev.datavar['SpiFrameFormat']+"\n")

        # end of device
        if i+1 == len(dev_cfg):
            cf.write("\t}\n")
        else:
            cf.write("\t},\n")
    cf.write("};\n\n")



def get_def_data_len(chn):
    data = chn.datavar['SpiDefaultData']
    # check for incorrect entry of default data
    if not data[:1].isdigit() and data != "NULL":
        print("ERROR: Default Data for SpiChannel \""+chn.datavar["SpiChannelId"]+"\" is wrong! Data:", data)
        return 0
    elif data == "NULL":
        return 0

    data_len = (len(data)+1) / 2 # +1 for rounding up in case of odd number of chars
    if "0x" == data[:2] or "0X" == data[:2]:
        data_len -= 1 # reduce the size of "0x" form len
    return int(data_len)

def get_def_data(chn):
    def_data = chn.datavar['SpiDefaultData']
    if "NULL" != def_data:
        def_data = "SpiDefaultData_"+chn.datavar['SpiChannelId']
    return def_data

def get_ib_buffer_len(chn):
    ib_buf_len = str(int(int(chn.datavar['SpiDataWidth'])*int(chn.datavar['SpiIbNBuffers'] or 0)/8))
    return ib_buf_len

def get_ib_buffer_name(chn):
    s_buf_name = "NULL"
    d_buf_name = "NULL"
    if "IB" in chn.datavar['SpiChannelType']:
        s_buf_name = "SpiIB_BufferTx_Chn_"+chn.datavar['SpiChannelId']
        d_buf_name = "SpiIB_BufferRx_Chn_"+chn.datavar['SpiChannelId']
    return s_buf_name, d_buf_name

def get_eb_buffer_len_p(chn):
    eb_buf_len_ptr = "NULL"
    if "EB" in chn.datavar['SpiChannelType']:
        eb_buf_len_ptr = "&SpiEB_BufferLen_Chn_"+chn.datavar['SpiChannelId']
    return eb_buf_len_ptr

def get_eb_buffer_p(chn):
    eb_buf_ptr_s = "NULL"
    eb_buf_ptr_d = "NULL"
    if "EB" in chn.datavar['SpiChannelType']:
        eb_buf_ptr_s = "&SpiEB_BufferTx_Chn_"+chn.datavar['SpiChannelId']
        eb_buf_ptr_d = "&SpiEB_BufferRx_Chn_"+chn.datavar['SpiChannelId']
    return eb_buf_ptr_s, eb_buf_ptr_d

def gen_spi_channel_configs(cf, chn_cfg):
    for chn in chn_cfg:
        chn.get()
        def_data = chn.datavar['SpiDefaultData']
        if def_data == "NULL":
            continue
        cf.write("\nconst uint8 SpiDefaultData_"+chn.datavar['SpiChannelId']+"[] = {\n\t")
        prefix = ""
        start = 0
        if "0x" == def_data[:2] or "0X" == def_data[:2]:
            prefix = "0x"
            start = 2
        data_len = len(def_data)
        for i in range(start, data_len, 2):
            num = prefix+def_data[i]
            if i+1 < data_len:
                num += def_data[i+1]
            cf.write(num+", ")
        cf.write("\n};\n")
    cf.write("\n")

    # define IB and EB buffers
    for chn in chn_cfg:
        ib_buf_s, ib_buf_d = get_ib_buffer_name(chn)
        eb_buf_length = get_eb_buffer_len_p(chn).split("&")[-1]
        eb_buf_s, eb_buf_d = get_eb_buffer_p(chn)
        if not ib_buf_s == "NULL":
            cf.write("static uint8 "+ib_buf_s+"["+get_ib_buffer_len(chn)+"];\n")
        if not ib_buf_d == "NULL":
            cf.write("static uint8 "+ib_buf_d+"["+get_ib_buffer_len(chn)+"];\n")
        if not eb_buf_length == "NULL":
            cf.write("static uint16 "+eb_buf_length+" = 0;\n")
        if not eb_buf_s == "NULL":
            cf.write("static uint8* "+eb_buf_s.split("&")[-1]+" = NULL;\n")
        if not eb_buf_d == "NULL":
            cf.write("static uint8* "+eb_buf_d.split("&")[-1]+" = NULL;\n")

    cf.write("\nconst SpiChannelCfgType SpiChannelCfg[] = {\n")
    for i, chn in enumerate(chn_cfg):
        # start of device
        cf.write("\t{\n")

        cf.write("\t\t.spi_chan_id = "+chn.datavar['SpiChannelId']+",\n")
        cf.write("\t\t.spi_chan_type = "+get_chan_type(chn.datavar['SpiChannelType'])+",\n")
        cf.write("\t\t.spi_data_width = "+chn.datavar['SpiDataWidth']+", /* bits */\n")
        cf.write("\t\t.spi_default_data = "+get_def_data(chn)+",\n")
        cf.write("\t\t.spi_default_data_len = "+str(get_def_data_len(chn))+",\n")
        cf.write("\t\t.spi_eb_max_len = "+str(int(chn.datavar['SpiEbMaxLength'] or 0))+",\n")
        cf.write("\t\t.spi_ib_num_buf = "+str(int(chn.datavar['SpiIbNBuffers'] or 0))+",\n")
        cf.write("\t\t.spi_ib_buf_len = "+get_ib_buffer_len(chn)+",\n")
        ib_buf_s, ib_buf_d = get_ib_buffer_name(chn)
        cf.write("\t\t.spi_ib_buf_s_ptr = "+ib_buf_s+",\n")
        cf.write("\t\t.spi_ib_buf_d_ptr = "+ib_buf_d+",\n")
        eb_buf_s, eb_buf_d = get_eb_buffer_p(chn)
        cf.write("\t\t.spi_eb_buf_s_ptr = "+eb_buf_s+",\n")
        cf.write("\t\t.spi_eb_buf_d_ptr = "+eb_buf_d+",\n")
        cf.write("\t\t.spi_eb_buf_l_ptr = "+get_eb_buffer_len_p(chn)+",\n")
        cf.write("\t\t.spi_tx_start = SPI_TX_START_"+chn.datavar['SpiTransferStart']+"\n")

        # end of device
        if i+1 == len(chn_cfg):
            cf.write("\t}\n")
        else:
            cf.write("\t},\n")
    cf.write("};\n\n")



def gen_spi_job_configs(cf, job_cfg):
    for job in job_cfg:
        cf.write("\nconst uint16 SpiChannelList_"+job.datavar['SpiJobId']+"[] = {\n\t")
        ch_list = job.datavar['SpiChannelList']
        for ch in ch_list:
            cf.write(ch["SpiChannelIndex"]+", ")
        cf.write("\n};\n")


    cf.write("\nconst SpiJobCfgType SpiJobCfg[] = {\n")
    for i, job in enumerate(job_cfg):
        # start of device
        cf.write("\t{\n")

        cf.write("\t\t.spi_job_id = "+job.datavar['SpiJobId']+",\n")
        cf.write("\t\t.spi_job_priority = "+job.datavar['SpiJobPriority']+",\n")
        cf.write("\t\t.job_end_notification_fn = "+job.datavar['SpiJobEndNotification']+",\n")
        cf.write("\t\t.spi_dev_assignment = SPI_EXT_DEV_"+job.datavar['SpiDeviceAssignment']+",\n")
        cf.write("\t\t.spi_chan_list_size = "+str(len(job.datavar['SpiChannelList']))+",\n")
        cf.write("\t\t.spi_chan_list = SpiChannelList_"+job.datavar['SpiJobId']+",\n")

        # end of device
        if i+1 == len(job_cfg):
            cf.write("\t}\n")
        else:
            cf.write("\t},\n")
    cf.write("};\n\n")



def gen_spi_seq_configs(cf, seq_cfg):
    for seq in seq_cfg:
        cf.write("\nconst uint16 SpiJobAssignment_"+seq.datavar['SpiSequenceId']+"[] = {\n\t")
        job_list = seq.datavar['SpiJobAssignment']
        for job in job_list:
            cf.write(job+", ")
        cf.write("\n};\n")


    cf.write("\nconst SpiSequenceCfgType SpiSequenceCfg[] = {\n")
    for i, seq in enumerate(seq_cfg):
        # start of device
        cf.write("\t{\n")

        cf.write("\t\t.spi_seq_id = "+seq.datavar['SpiSequenceId']+",\n")
        cf.write("\t\t.spi_seq_interruptible = "+seq.datavar['SpiInterruptibleSequence']+",\n")
        cf.write("\t\t.seq_end_notification_fn = "+seq.datavar['SpiSeqEndNotification']+",\n")
        cf.write("\t\t.spi_job_list_size = "+str(len(seq.datavar['SpiJobAssignment']))+",\n")
        cf.write("\t\t.spi_job_list = SpiJobAssignment_"+seq.datavar['SpiSequenceId']+",\n")

        # end of device
        if i+1 == len(seq_cfg):
            cf.write("\t}\n")
        else:
            cf.write("\t},\n")
    cf.write("};\n\n")



def gen_spi_cfg_configs(cf):
    cf.write("\nconst Spi_ConfigType SpiConfigs = {\n")
    cf.write("\t.general   = SpiGeneralCfg,\n")
    cf.write("\t.devices   = SpiExternalDeviceCfg,\n")
    cf.write("\t.channels  = SpiChannelCfg,\n")
    cf.write("\t.jobs      = SpiJobCfg,\n")
    cf.write("\t.sequences = SpiSequenceCfg\n")
    cf.write("};\n\n")



def generate_sourcefile(spi_src_path, spi_info):
    cf = open(spi_src_path+"/cfg/Spi_cfg.c", "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include <Spi_cfg.h>\n\n\n")
    cf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")

    gen_spi_general_configs(cf, spi_info["SpiGeneral"][0].datavar)
    gen_spi_device_configs(cf, spi_info)
    gen_spi_channel_configs(cf, spi_info["SpiChannel"])
    gen_spi_job_configs(cf, spi_info["SpiJob"])
    gen_spi_seq_configs(cf, spi_info["SpiSequence"])
    gen_spi_cfg_configs(cf)


    cf.close()



def generate_code(gui, spi_configs):
    cwd = os.getcwd()
    spi_src_path = search.find_dir("Spi", cwd+"/submodules/MCAL/")
    generate_headerfile(spi_src_path, spi_configs)
    generate_sourcefile(spi_src_path, spi_configs)
    uc_cgen.create_source(gui)
    
