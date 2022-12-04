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



class EthGeneralTab:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthIndex", "EthDevErrorDetect", "EthGetCounterValuesApi", "EthGetRxStatsApi",
               "EthGetTxErrorCounterValuesApi", "EthGetTxStatsApi", "EthGlobalTimeSupport", 
               "EthMainFunctionPeriod", "EthMaxCtrlsSupported", "EthVersionInfoApi",
               "EthCtrlOffloading"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    ctrlr_idx = 0


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
        gen_dict["EthIndex"]                        = str(index)
        gen_dict["EthDevErrorDetect"]               = "FALSE"
        gen_dict["EthMainFunctionPeriod"]           = "FALSE"
        gen_dict["EthGetCounterValuesApi"]          = "IB"
        gen_dict["EthGetRxStatsApi"]                = "FALSE"
        gen_dict["EthGetTxErrorCounterValuesApi"]   = "FALSE"
        gen_dict["EthGetTxStatsApi"]                = "FALSE"
        gen_dict["EthGlobalTimeSupport"]            = "FALSE"
        gen_dict["EthMaxCtrlsSupported"]            = str(index)
        gen_dict["EthVersionInfoApi"]               = "FALSE"
        gen_dict["EthCtrlOffloading"]               = {}
        return gen_dict



    def draw_dappas(self):
        bool_cmbsel = ("FALSE", "TRUE")

        dappa.entry(self, "EthIndex",               0, 0, 1, 23, "readonly")
        dappa.entry(self, "EthMainFunctionPeriod",  0, 1, 1, 23, "normal")
        dappa.combo(self, "EthDevErrorDetect",      0, 2, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthGetCounterValuesApi", 0, 3, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthGetRxStatsApi",       0, 4, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthGetTxErrorCounterValuesApi", 0, 5, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthGetTxStatsApi",       0, 6, 1, 20, bool_cmbsel)
        dappa.combo(self, "EthGlobalTimeSupport",   0, 7, 1, 20, bool_cmbsel)
        dappa.entry(self, "EthMaxCtrlsSupported",   0, 8, 1, 23, "readonly")
        dappa.combo(self, "EthVersionInfoApi",      0, 9, 1, 20, bool_cmbsel)
        cb = lambda id = self.ctrlr_idx : self.eth_offloading_select(id)
        dappa.button(self, "EthCtrlOffloading",     0, 10, 1, 19, "SELECT", cb)





    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)



    def update_ethernet_config(self, max_ctrlr):
        self.configs[0].dispvar["EthMaxCtrlsSupported"].set(max_ctrlr)


    def eth_offloading_select(self):
        print("clicked eth_offloading_select")
