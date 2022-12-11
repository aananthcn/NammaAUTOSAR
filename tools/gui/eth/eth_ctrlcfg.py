#
# Created on Fri Dec 09 2022 7:51:11 PM
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



class EthCtrlConfigChildView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthCtrlConfigSwBufferHandling", "EthCtrlEnableMii", "EthCtrlEnableRxInterrupt", 
               "EthCtrlEnableSpiInterface", "EthCtrlEnableTxInterrupt", "EthCtrlIdx", "EthCtrlMacLayerSpeed",
               "EthCtrlMacLayerType", "EthCtrlMacLayerSubType", "EthCtrlPhyAddress"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)


    def __init__(self, gui, index, ecc_cfg):
        self.gui = gui
        self.configs = []

        # Create config string for AUTOSAR configs on this tab
        if not ecc_cfg:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs(index)))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, ecc_cfg))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self, index):
        gen_dict = {}
        
        gen_dict["EthCtrlConfigSwBufferHandling"]   = "FALSE"
        gen_dict["EthCtrlEnableMii"]                = "FALSE"
        gen_dict["EthCtrlEnableRxInterrupt"]        = "FALSE"
        gen_dict["EthCtrlEnableSpiInterface"]       = "FALSE"
        gen_dict["EthCtrlEnableTxInterrupt"]        = "FALSE"
        gen_dict["EthCtrlIdx"]                      = str(index)
        gen_dict["EthCtrlMacLayerSpeed"]            = "ETH_MAC_LAYER_SPEED_10M"
        gen_dict["EthCtrlMacLayerType"]             = "ETH_MAC_LAYER_TYPE_XMII"
        gen_dict["EthCtrlMacLayerSubType"]          = "STANDARD"
        gen_dict["EthCtrlPhyAddress"]               = "00:00:5e:00:53:"+format(index, '02x')
        
        return gen_dict



    def draw_dappas(self):
        bool_cmbsel = ("FALSE", "TRUE")

        dappa.combo(self, "EthCtrlConfigSwBufferHandling",  0, 0, 1, 30, bool_cmbsel)
        dappa.combo(self, "EthCtrlEnableMii",               0, 1, 1, 30, bool_cmbsel)
        dappa.combo(self, "EthCtrlEnableRxInterrupt",       0, 2, 1, 30, bool_cmbsel)
        dappa.combo(self, "EthCtrlEnableSpiInterface",      0, 3, 1, 30, bool_cmbsel)
        dappa.combo(self, "EthCtrlEnableTxInterrupt",       0, 4, 1, 30, bool_cmbsel)
        dappa.entry(self, "EthCtrlIdx",                     0, 5, 1, 33, "readonly")
        speed_cmbsel = ("ETH_MAC_LAYER_SPEED_10M", "ETH_MAC_LAYER_SPEED_100M", "ETH_MAC_LAYER_SPEED_1G", "ETH_MAC_LAYER_SPEED_2500M", "ETH_MAC_LAYER_SPEED_10G")
        dappa.combo(self, "EthCtrlMacLayerSpeed",           0, 6, 1, 30, speed_cmbsel)
        mactype_cmbsel = ("ETH_MAC_LAYER_TYPE_XMII", "ETH_MAC_LAYER_TYPE_XGMII", "ETH_MAC_LAYER_TYPE_XXGMII")
        dappa.combo(self, "EthCtrlMacLayerType",            0, 7, 1, 30, mactype_cmbsel)
        macsubtype_cmbsel = ("REDUCED", "REVERSED", "SERIAL", "STANDARD", "UNIVERSAL_SERIAL")
        dappa.combo(self, "EthCtrlMacLayerSubType",         0, 8, 1, 30, macsubtype_cmbsel)
        dappa.entry(self, "EthCtrlPhyAddress",              0, 9, 1, 28, "larger")



    def draw(self, view):
        self.tab_struct = view
        self.scrollw = window.ScrollableWindow(view.frame, view.xsize, view.ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()
