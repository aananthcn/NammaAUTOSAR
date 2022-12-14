#
# Created on Sat Dec 10 2022 11:05:32 AM
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



class EthConfigSpiConfigChildView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthCtrlConfigSpiChunkPayloadSize", "EthCtrlConfigSpiCommRetries",
               "EthCtrlConfigSpiEnableControlDataProtection", "EthCtrlConfigSpiEnableRxCSAlign",
               "EthCtrlConfigSpiEnableRxCutThrough", "EthCtrlConfigSpiEnableRxZeroAlign",
               "EthCtrlConfigSpiEnableTransmitDataHdrSequence", "EthCtrlConfigSpiEnableTxChecksum",
               "EthCtrlConfigSpiEnableTxCutThrough", "EthCtrlConfigSpiSelectTimeStamp",
               "EthCtrlConfigSpiTransmitCreditThreshold", "EthCtrlConfigSpiAccessSynchronous",
               "EthCtrlConfigSpiSequenceName", "EthCtrlConfigSpiCommTimeout"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    
    spi_sequences = None


    def __init__(self, gui, index, spi_cfg, ethspi_cfg):
        self.gui = gui
        self.configs = []

        # Create config string for AUTOSAR configs on this tab
        if not ethspi_cfg:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, ethspi_cfg))
        
        # parse Spi Sequences
        if spi_cfg:
            self.spi_sequences = ["NONE"]
            for cfg in spi_cfg:
                self.spi_sequences.append(cfg["SpiSequenceName"])


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}

        gen_dict["EthCtrlConfigSpiChunkPayloadSize"] = "64" # 64 bits
        gen_dict["EthCtrlConfigSpiCommRetries"] = "1"
        gen_dict["EthCtrlConfigSpiEnableControlDataProtection"] = "FALSE" # No encryption
        gen_dict["EthCtrlConfigSpiEnableRxCSAlign"] = "FALSE"
        gen_dict["EthCtrlConfigSpiEnableRxCutThrough"] = "FALSE"
        gen_dict["EthCtrlConfigSpiEnableRxZeroAlign"] = "FALSE"
        gen_dict["EthCtrlConfigSpiEnableTransmitDataHdrSequence"] = "FALSE" # no HW bit monitoring business
        gen_dict["EthCtrlConfigSpiEnableTxChecksum"] = "FALSE"
        gen_dict["EthCtrlConfigSpiEnableTxCutThrough"] = "FALSE"
        gen_dict["EthCtrlConfigSpiSelectTimeStamp"] = "FALSE"
        gen_dict["EthCtrlConfigSpiTransmitCreditThreshold"] = "0"
        gen_dict["EthCtrlConfigSpiAccessSynchronous"] = "FALSE"
        gen_dict["EthCtrlConfigSpiSequenceName"] = "NONE" # get from Spi Sequence
        gen_dict["EthCtrlConfigSpiCommTimeout"] = "0.1" # 100 ms

        return gen_dict



    def draw_dappas(self):
        cmbsel_payld = ("8", "16", "24", "32", "64")
        cmbsel_bool = ("FALSE", "TRUE")
        dappa.combo(self, "EthCtrlConfigSpiChunkPayloadSize",   0,  0, 1, 27, cmbsel_payld)
        dappa.spinb(self, "EthCtrlConfigSpiCommRetries",        0,  1, 1, 28, tuple(range(0,256)))
        dappa.combo(self, "EthCtrlConfigSpiEnableControlDataProtection",   0, 2, 1, 27, cmbsel_bool)
        dappa.combo(self, "EthCtrlConfigSpiEnableRxCSAlign",    0,  3, 1, 27, cmbsel_bool)
        dappa.combo(self, "EthCtrlConfigSpiEnableRxCutThrough", 0,  4, 1, 27, cmbsel_bool)
        dappa.combo(self, "EthCtrlConfigSpiEnableRxZeroAlign",  0,  5, 1, 27, cmbsel_bool)
        dappa.combo(self, "EthCtrlConfigSpiEnableTransmitDataHdrSequence", 0, 6, 1, 27, cmbsel_bool)
        dappa.combo(self, "EthCtrlConfigSpiEnableTxChecksum",   0,  7, 1, 27, cmbsel_bool)
        dappa.combo(self, "EthCtrlConfigSpiEnableTxCutThrough", 0,  8, 1, 27, cmbsel_bool)
        dappa.combo(self, "EthCtrlConfigSpiSelectTimeStamp",    0,  9, 1, 27, cmbsel_bool)
        dappa.spinb(self, "EthCtrlConfigSpiTransmitCreditThreshold", 0, 10, 1, 28, tuple(range(0,4)))
        dappa.combo(self, "EthCtrlConfigSpiAccessSynchronous",  0, 11, 1, 27, cmbsel_bool)
        ss = dappa.combo(self, "EthCtrlConfigSpiSequenceName",  0, 12, 1, 27, tuple(self.spi_sequences))
        ss.bind("<<ComboboxSelected>>", lambda evt: self.spi_selected(evt))
        if "NONE" in self.configs[0].dispvar["EthCtrlConfigSpiSequenceName"].get():
            dappa.entry(self, "EthCtrlConfigSpiCommTimeout",    0, 13, 1, 30, "readonly")
            self.configs[0].dispvar["EthCtrlConfigSpiCommTimeout"].set("0")
        else:
            dappa.entry(self, "EthCtrlConfigSpiCommTimeout",    0, 13, 1, 30, "normal")



    def draw(self, view):
        self.tab_struct = view
        self.scrollw = window.ScrollableWindow(view.frame, view.xsize, view.ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()


    def spi_selected(self, event):
        self.configs[0].get() # read from UI (backup last selection)
        # re-draw all boxes (dappas) of this row
        dappa.delete_dappas(self)
        self.draw_dappas()
