#
# Created on Fri Oct 21 2022 8:23:05 AM
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



class SpiDriverTab:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SpiMaxChannel", "SpiMaxJob", "SpiMaxSequence", "SpiMaxHwUnit"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)


    def __init__(self, gui):
        self.gui = gui
        self.configs = []

        # Create config string for AUTOSAR configs on this tab
        self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))

        #spi_drv_dict = arxml_spi.parse_arxml(gui.arxml_file)
        spi_drv_dict = None
        if spi_drv_dict == None:
            return


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        spi_drv_dict = {}
        spi_drv_dict["SpiMaxChannel"]       = "0"
        spi_drv_dict["SpiMaxJob"]           = "0"
        spi_drv_dict["SpiMaxSequence"]      = "0"
        spi_drv_dict["SpiMaxHwUnit"]        = "0"
        return spi_drv_dict


    def draw_dappas(self):
        dappa.entry(self, "SpiMaxChannel",  0, 0, 1, 23, "readonly")
        dappa.entry(self, "SpiMaxJob",      0, 1, 1, 23, "readonly")
        dappa.entry(self, "SpiMaxSequence", 0, 2, 1, 23, "readonly")
        dappa.entry(self, "SpiMaxHwUnit",   0, 3, 1, 23, "readonly")


    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()



    def save_data(self):
        # self.backup_data()
        self.tab_struct.save_cb(self.gui)



    def spi_chan_list_changed(self, chn_configs):
        self.configs[0].set_var("SpiMaxChannel", len(chn_configs))


    def spi_job_list_changed(self, job_configs):
        self.configs[0].set_var("SpiMaxJob", len(job_configs))


    def spi_seq_list_changed(self, seq_configs):
        self.configs[0].set_var("SpiMaxSequence", len(seq_configs))


    def spi_extdrv_list_changed(self, exd_configs):
        self.configs[0].set_var("SpiMaxHwUnit", len(exd_configs))