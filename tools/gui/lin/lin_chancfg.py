#
# Created on Mon Dec 19 2022 9:59:45 AM
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



class LinChannelConfigChildView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["LinChannelId", "LinNodeType", "LinChannelBaudRate",
               "LinChannelWakeupSupport", "LinChannelEcuMWakeupSource", "LinClockRef"]

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
        
        gen_dict["LinChannelId"]                = str(index)
        gen_dict["LinNodeType"]                 = "MASTER"
        gen_dict["LinChannelBaudRate"]          = "1000"
        gen_dict["LinChannelWakeupSupport"]     = "FALSE"
        gen_dict["LinChannelEcuMWakeupSource"]  = ""
        gen_dict["LinClockRef"]                 = ""
        
        return gen_dict



    def draw_dappas(self):
        bool_cmbsel = ("FALSE", "TRUE")

        dappa.entry(self, "LinChannelId",               0, 0, 1, 33, "readonly")
        dappa.combo(self, "LinNodeType",                0, 1, 1, 30, ("MASTER", "SLAVE"))
        dappa.entry(self, "LinChannelBaudRate",         0, 2, 1, 33, "normal")
        dappa.combo(self, "LinChannelWakeupSupport",    0, 3, 1, 30, bool_cmbsel)
        dappa.entry(self, "LinChannelEcuMWakeupSource", 0, 4, 1, 33, "normal")
        dappa.entry(self, "LinClockRef",                0, 5, 1, 33, "normal")



    def draw(self, view):
        self.tab_struct = view
        self.scrollw = window.ScrollableWindow(view.frame, view.xsize, view.ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()
