#
# Created on Wed Oct 05 2022 8:04:30 PM
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



class SpiGeneralTab:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SpiLevelDelivered", "SpiChannelBuffersAllowed", "SpiInterruptibleSeqAllowed",
               "SpiHwStatusApi", "SpiCancelApi", "SpiVersionInfoApi", "SpiDevErrorDetect",
               "SpiSupportConcurrentSyncTransmit", "SpiMainFunctionPeriod"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)


    def __init__(self, gui, ar_cfg):
        self.gui = gui
        self.configs = []

        # Create config string for AUTOSAR configs on this tab
        self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}
        gen_dict["SpiLevelDelivered"]                  = "1"
        gen_dict["SpiChannelBuffersAllowed"]           = "IB"
        gen_dict["SpiInterruptibleSeqAllowed"]         = "FALSE"
        gen_dict["SpiHwStatusApi"]                     = "FALSE"
        gen_dict["SpiCancelApi"]                       = "FALSE"
        gen_dict["SpiVersionInfoApi"]                  = "FALSE"
        gen_dict["SpiDevErrorDetect"]                  = "FALSE"
        gen_dict["SpiSupportConcurrentSyncTransmit"]   = "FALSE"
        gen_dict["SpiMainFunctionPeriod"]              = "0.01" # secs = 100 ms
        return gen_dict



    def draw_dappas(self):
        spi_cmbsel = ("FALSE", "TRUE")

        # SpiLevelDelivered
        dappa.combo(self, "SpiLevelDelivered", 0, 0, 1, 20, ('0', '1', '2'))

        # SpiChannelBuffersAllowed
        values = ('IB (Internal Buffer)', 'EB (External Buffer)', 'IB / EB')
        dappa.combo(self, "SpiChannelBuffersAllowed", 0, 1, 1, 20, values)

        # SpiInterruptibleSeqAllowed
        dappa.combo(self, "SpiInterruptibleSeqAllowed", 0, 2, 1, 20, spi_cmbsel)

        # SpiHwStatusApi
        dappa.combo(self, "SpiHwStatusApi", 0, 3, 1, 20, spi_cmbsel)

        # SpiCancelApi
        dappa.combo(self, "SpiCancelApi", 0, 4, 1, 20, spi_cmbsel)

        # SpiVersionInfoApi
        dappa.combo(self, "SpiVersionInfoApi", 0, 5, 1, 20, spi_cmbsel)

        # SpiDevErrorDetect
        dappa.combo(self, "SpiDevErrorDetect", 0, 6, 1, 20, spi_cmbsel)

        # SpiSupportConcurrentSyncTransmit
        dappa.combo(self, "SpiSupportConcurrentSyncTransmit", 0, 7, 1, 20, spi_cmbsel)

        # SpiMainFunctionPeriod
        dappa.entry(self, "SpiMainFunctionPeriod", 0, 8, 1, 23, "normal")



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Place save button
        space = tk.Label(self.scrollw.mnf)
        space.grid(row=9, column=1)
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        saveb.grid(row=10, column=1)

        # Support scrollable view
        self.scrollw.scroll()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)
