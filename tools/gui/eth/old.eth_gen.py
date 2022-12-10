#
# Created on Mon Nov 28 2022 10:04:37 PM
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
import tkinter as tk
from tkinter import ttk

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box



class EthGeneralChildView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthIndex", "EthDevErrorDetect", "EthGetCounterValuesApi", "EthGetRxStatsApi",
               "EthGetTxErrorCounterValuesApi", "EthGetTxStatsApi", "EthGlobalTimeSupport", 
               "EthMainFunctionPeriod", "EthMaxCtrlsSupported", "EthVersionInfoApi",
               "EthCtrlEnableOffloadChecksumIPv4", "EthCtrlEnableOffloadChecksumICMP",
               "EthCtrlEnableOffloadChecksumTCP", "EthCtrlEnableOffloadChecksumUDP",
               "EthCtrlConfigSwBufferHandling", "EthCtrlEnableMii", "EthCtrlEnableRxInterrupt",
               "EthCtrlEnableSpiInterface", "EthCtrlEnableTxInterrupt", "EthCtrlIdx",
               "EthCtrlMacLayerSpeed", "EthCtrlMacLayerType", "EthCtrlMacLayerSubType",
               "EthCtrlPhyAddress",
               "EthCtrlConfigEgressFifoBufLenByte", "EthCtrlConfigEgressFifoBufTotal",
               "EthCtrlConfigEgressFifoIdx", "EthCtrlConfigEgressFifoPriorityAssignment",
               "EthCtrlConfigSchedulerPredecessorOrder",
               "EthCtrlConfigShaperIdleSlope", "EthCtrlConfigShaperMaxCredit", 
               "EthCtrlConfigShaperMinCredit",
               "EthCtrlConfigIngressFifoBufLenByte", "EthCtrlConfigIngressFifoBufTotal",
               "EthCtrlConfigIngressFifoIdx", "EthCtrlConfigIngressFifoPriorityAssignment"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    active_dialog = None
    ctrlr_idx = 0
    header_row = 0
    dappas_per_row = 0
    
    group_objs = []


    def __init__(self, gui, ar_cfg, idx):
        self.gui = gui
        self.configs = []
        self.ctrlr_idx = idx

        # Create config string for AUTOSAR configs on this tab
        self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs(idx)))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self, index):
        gen_dict = {}

        # # EthCtrlConfig group
        # gen_dict["EthIndex"]                        = str(index)
        # gen_dict["EthDevErrorDetect"]               = "FALSE"
        # gen_dict["EthMainFunctionPeriod"]           = "FALSE"
        # gen_dict["EthGetCounterValuesApi"]          = "FALSE"
        # gen_dict["EthGetRxStatsApi"]                = "FALSE"
        # gen_dict["EthGetTxErrorCounterValuesApi"]   = "FALSE"
        # gen_dict["EthGetTxStatsApi"]                = "FALSE"
        # gen_dict["EthGlobalTimeSupport"]            = "FALSE"
        # gen_dict["EthMaxCtrlsSupported"]            = str(index)
        # gen_dict["EthVersionInfoApi"]               = "FALSE"
        
        # # Checksum OffLoad
        # gen_dict["EthCtrlEnableOffloadChecksumIPv4"]   = "FALSE"
        # gen_dict["EthCtrlEnableOffloadChecksumICMP"]   = "FALSE"
        # gen_dict["EthCtrlEnableOffloadChecksumTCP"]    = "FALSE"
        # gen_dict["EthCtrlEnableOffloadChecksumUDP"]    = "FALSE"

        # # EthCtrlConfig group
        # gen_dict["EthCtrlConfigSwBufferHandling"]   = "FALSE"
        # gen_dict["EthCtrlEnableMii"]                = "FALSE"
        # gen_dict["EthCtrlEnableRxInterrupt"]        = "FALSE"
        # gen_dict["EthCtrlEnableSpiInterface"]       = "FALSE"
        # gen_dict["EthCtrlEnableTxInterrupt"]        = "FALSE"
        # gen_dict["EthCtrlIdx"]                      = str(index)
        # gen_dict["EthCtrlMacLayerSpeed"]            = "ETH_MAC_LAYER_SPEED_10M"
        # gen_dict["EthCtrlMacLayerType"]             = "ETH_MAC_LAYER_TYPE_XMII"
        # gen_dict["EthCtrlMacLayerSubType"]          = "STANDARD"
        # gen_dict["EthCtrlPhyAddress"]               = "00:00:5e:00:53:af"

        # # EthCtrlConfigXgressFifo group
        # gen_dict["EthCtrlConfigEgressFifoBufLenByte"]          = "128"
        # gen_dict["EthCtrlConfigEgressFifoBufTotal"]            = "100"
        # gen_dict["EthCtrlConfigEgressFifoIdx"]                 = str(index)
        # gen_dict["EthCtrlConfigEgressFifoPriorityAssignment"]  = "7"
        # gen_dict["EthCtrlConfigIngressFifoBufLenByte"]         = "128"
        # gen_dict["EthCtrlConfigIngressFifoBufTotal"]           = "100"
        # gen_dict["EthCtrlConfigIngressFifoIdx"]                = str(index)
        # gen_dict["EthCtrlConfigIngressFifoPriorityAssignment"] = "7"

        # # EthCtrlConfigSchedulerPredecessor group
        # gen_dict["EthCtrlConfigSchedulerPredecessorOrder"] = "0"
        
        # EthCtrlConfigShaper group
        gen_dict["EthCtrlConfigShaperIdleSlope"] = "1"
        gen_dict["EthCtrlConfigShaperMaxCredit"] = "1"
        gen_dict["EthCtrlConfigShaperMinCredit"] = "1"
        
        return gen_dict



    def draw_dappas(self, i):
        bool_cmbsel = ("FALSE", "TRUE")

        # # EthGeneral group
        # group = dappa.group(self, "EthGeneral", row=0, col=0)
        # dappa.entryg(group, self, "EthIndex",               i, 1, 1, 23, "readonly")
        # dappa.entryg(group, self, "EthMainFunctionPeriod",  i, 2, 1, 23, "normal")
        # dappa.combog(group, self, "EthDevErrorDetect",      i, 3, 1, 20, bool_cmbsel)
        # dappa.combog(group, self, "EthGetCounterValuesApi", i, 4, 1, 20, bool_cmbsel)
        # dappa.combog(group, self, "EthGetRxStatsApi",       i, 5, 1, 20, bool_cmbsel)
        # dappa.combog(group, self, "EthGetTxErrorCounterValuesApi", i, 6, 1, 20, bool_cmbsel)
        # dappa.combog(group, self, "EthGetTxStatsApi",       i, 7, 1, 20, bool_cmbsel)
        # dappa.combog(group, self, "EthGlobalTimeSupport",   i, 8, 1, 20, bool_cmbsel)
        # dappa.entryg(group, self, "EthMaxCtrlsSupported",   i, 9, 1, 23, "readonly")
        # dappa.combog(group, self, "EthVersionInfoApi",      i, 10, 1, 20, bool_cmbsel)

        # # EthCtrlOffloading group
        # group = dappa.group(self, "EthCtrlOffloading", row=1, col=0)
        # dappa.combog(group, self, "EthCtrlEnableOffloadChecksumIPv4",  i, 1, 1, 15, bool_cmbsel)
        # dappa.combog(group, self, "EthCtrlEnableOffloadChecksumICMP",  i, 2, 1, 15, bool_cmbsel)
        # dappa.combog(group, self, "EthCtrlEnableOffloadChecksumTCP",   i, 3, 1, 15, bool_cmbsel)
        # dappa.combog(group, self, "EthCtrlEnableOffloadChecksumUDP",   i, 4, 1, 15, bool_cmbsel)
        # return

        # # EthCtrlConfig group
        # group = dappa.group(self, "EthCtrlConfig", row=0, col=1)
        # dappa.combog(group, self, "EthCtrlConfigSwBufferHandling",  i, 1, 1, 30, bool_cmbsel)
        # dappa.combog(group, self, "EthCtrlEnableMii",               i, 2, 1, 30, bool_cmbsel)
        # dappa.combog(group, self, "EthCtrlEnableRxInterrupt",       i, 3, 1, 30, bool_cmbsel)
        # dappa.combog(group, self, "EthCtrlEnableSpiInterface",      i, 4, 1, 30, bool_cmbsel)
        # dappa.combog(group, self, "EthCtrlEnableTxInterrupt",       i, 5, 1, 30, bool_cmbsel)
        # dappa.entryg(group, self, "EthCtrlIdx",                     i, 6, 1, 33, "readonly")
        # speed_cmbsel = ("ETH_MAC_LAYER_SPEED_10M", "ETH_MAC_LAYER_SPEED_100M", "ETH_MAC_LAYER_SPEED_1G", "ETH_MAC_LAYER_SPEED_2500M", "ETH_MAC_LAYER_SPEED_10G")
        # dappa.combog(group, self, "EthCtrlMacLayerSpeed",           i, 7, 1, 30, speed_cmbsel)
        # mactype_cmbsel = ("ETH_MAC_LAYER_TYPE_XMII", "ETH_MAC_LAYER_TYPE_XGMII", "ETH_MAC_LAYER_TYPE_XXGMII")
        # dappa.combog(group, self, "EthCtrlMacLayerType",            i, 8, 1, 30, mactype_cmbsel)
        # macsubtype_cmbsel = ("REDUCED", "REVERSED", "SERIAL", "STANDARD", "UNIVERSAL_SERIAL")
        # dappa.combog(group, self, "EthCtrlMacLayerSubType",         i, 9, 1, 30, macsubtype_cmbsel)
        # dappa.entryg(group, self, "EthCtrlPhyAddress",              i, 10, 1, 33, "normal")

        # # EthCtrlConfigXgressFifo group
        # group = dappa.group(self, "EthCtrlConfigXgressFifo", row=0, col=2)
        # dappa.spinbg(group, self, "EthCtrlConfigEgressFifoBufLenByte",  i, 1, 1, 20, tuple(range(0,65536)))
        # dappa.spinbg(group, self, "EthCtrlConfigEgressFifoBufTotal",    i, 2, 1, 20, tuple(range(0,65536)))
        # dappa.entryg(group, self, "EthCtrlConfigEgressFifoIdx",         i, 3, 1, 22, "readonly")
        # dappa.spinbg(group, self, "EthCtrlConfigEgressFifoPriorityAssignment", i, 4, 1, 20, tuple(range(0,256)))
        # dappa.spinbg(group, self, "EthCtrlConfigIngressFifoBufLenByte", i, 4, 1, 20, tuple(range(0,65536)))
        # dappa.spinbg(group, self, "EthCtrlConfigIngressFifoBufTotal",   i, 5, 1, 20, tuple(range(0,65536)))
        # dappa.entryg(group, self, "EthCtrlConfigIngressFifoIdx",        i, 6, 1, 22, "readonly")
        # dappa.spinbg(group, self, "EthCtrlConfigIngressFifoPriorityAssignment", i, 7, 1, 20, tuple(range(0,256)))

        # # EthCtrlConfigSchedulerPredecessor group
        # group = dappa.group(self, "EthCtrlConfigSchedulerPredecessor", row=1, col=2)
        # dappa.entryg(group, self, "EthCtrlConfigSchedulerPredecessorOrder", i, 1, 1, 22, "normal")
 
        # EthCtrlConfigShaper group
        group = dappa.group(self, "EthCtrlConfigShaper", row=1, col=1)
        dappa.entryg(group, self, "EthCtrlConfigShaperIdleSlope", i, 1, 1, 22, "normal")
        dappa.entryg(group, self, "EthCtrlConfigShaperMaxCredit", i, 2, 1, 22, "normal")
        dappa.entryg(group, self, "EthCtrlConfigShaperMinCredit", i, 3, 1, 22, "normal")


    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)

        self.draw_dappas(0)

        # Support scrollable view
        self.scrollw.scroll()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)


    # idx: Controller Index
    # max_ctrlr: Total controllers configured
    def update_ethernet_config(self, idx, max_ctrlr):
        self.configs[idx].dispvar["EthMaxCtrlsSupported"].set(max_ctrlr)

